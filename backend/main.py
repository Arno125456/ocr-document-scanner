from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import os
import logging
from pydantic import BaseModel
from utils import export_results_to_json
from document_processor import DocumentProcessor
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io
import numpy as np

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="OCR Document Categorizer")

# Add CORS middleware - allow all origins for production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (safe for frontend-only app)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_pdf_to_image(pdf_path):
    """
    Convert the first page of a PDF to an image
    """
    logger.info(f"Converting PDF to image: {pdf_path}")
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)

    # Convert to PIL Image
    img_data = pix.tobytes("ppm")
    img = Image.open(io.BytesIO(img_data))

    doc.close()
    logger.info("PDF converted successfully")
    return img

class CategorizedResult(BaseModel):
    title: list[str]
    date: list[str]
    name: list[str]
    email: list[str]
    phone: list[str]
    amount: list[str]
    address: list[str]
    tax_id: list[str]
    invoice_number: list[str]
    items: list[str]
    other: list[str]
    document_type: str

@app.get("/health")
async def health_check():
    logger.info("Health check requested")
    return {"status": "healthy"}

@app.post("/upload", response_model=CategorizedResult)
async def upload_document(file: UploadFile = File(...), lang: str = "eng", return_regions: bool = False):
    temp_filename = None
    try:
        logger.info(f"=== UPLOAD REQUEST START ===")
        logger.info(f"File: {file.filename}, Lang: {lang}, Regions: {return_regions}")
        
        # Determine if file is PDF or image
        file_extension = os.path.splitext(file.filename)[1].lower() if file.filename else ''
        logger.info(f"File extension: {file_extension}")

        # Save uploaded file temporarily
        temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
        logger.info(f"Saving to: {temp_filename}")
        
        with open(temp_filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)
        logger.info(f"File saved, size: {len(content)} bytes")

        # Process the document
        logger.info("Initializing DocumentProcessor...")
        processor = DocumentProcessor()
        logger.info("DocumentProcessor initialized")

        # Handle PDF files by converting to image
        if file_extension == '.pdf':
            logger.info("Processing PDF file...")
            image = convert_pdf_to_image(temp_filename)
            logger.info("Extracting text from PDF...")
            extracted_text, ocr_data, regions = processor.extract_text(image, lang=lang, return_regions=return_regions)
            categorized_result = processor.categorize_text(extracted_text)
        else:
            logger.info("Processing image file...")
            logger.info("Detecting and cropping document...")
            cropped_image = processor.detect_and_crop(temp_filename)
            logger.info(f"Cropped image type: {type(cropped_image)}")
            if hasattr(cropped_image, 'shape'):
                logger.info(f"Cropped image shape: {cropped_image.shape}")
            logger.info("Extracting text from image...")
            extracted_text, ocr_data, regions = processor.extract_text(cropped_image, lang=lang, return_regions=return_regions)
            logger.info(f"Extracted text length: {len(extracted_text) if extracted_text else 0}")
            logger.info(f"First 100 chars: {extracted_text[:100] if extracted_text else 'N/A'}")
            categorized_result = processor.categorize_text(extracted_text)

        # Add text regions to response if requested
        response_data = dict(categorized_result)
        if return_regions and regions:
            response_data['text_regions'] = regions
            logger.info(f"Added {len(regions)} text regions to response")

        logger.info(f"Response data keys: {list(response_data.keys())}")
        logger.info(f"=== UPLOAD REQUEST SUCCESS ===")
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"=== UPLOAD REQUEST ERROR ===")
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error message: {str(e)}")
        import traceback
        logger.error(f"Traceback: {traceback.format_exc()}")
        return JSONResponse(
            status_code=500,
            content={
                "title": [],
                "date": [],
                "name": [],
                "email": [],
                "phone": [],
                "amount": [],
                "address": [],
                "tax_id": [],
                "invoice_number": [],
                "items": [],
                "other": [f"Error: {str(e)}"],
                "document_type": "error"
            }
        )
    finally:
        # Clean up temporary file
        if temp_filename and os.path.exists(temp_filename):
            os.remove(temp_filename)
            logger.info(f"Cleaned up temp file: {temp_filename}")

@app.post("/upload-with-export")
async def upload_document_with_export(file: UploadFile = File(...), lang: str = "eng"):
    try:
        # Determine if file is PDF or image
        file_extension = os.path.splitext(file.filename)[1].lower() if file.filename else ''

        # Save uploaded file temporarily
        temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
        with open(temp_filename, "wb") as buffer:
            content = await file.read()
            buffer.write(content)

        # Process the document
        processor = DocumentProcessor()

        # Handle PDF files by converting to image
        if file_extension == '.pdf':
            image = convert_pdf_to_image(temp_filename)
            extracted_text, ocr_data, regions = processor.extract_text(image, lang=lang, return_regions=True)
            categorized_result = processor.categorize_text(extracted_text)
        else:
            cropped_image = processor.detect_and_crop(temp_filename)
            extracted_text, ocr_data, regions = processor.extract_text(cropped_image, lang=lang, return_regions=True)
            categorized_result = processor.categorize_text(extracted_text)

        # Export results to JSON
        export_filename = export_results_to_json(categorized_result)

        return {"result": categorized_result, "export_file": export_filename}
    except Exception as e:
        logger.error(f"Upload with export error: {str(e)}")
        return {"error": str(e), "result": None, "export_file": None}
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
