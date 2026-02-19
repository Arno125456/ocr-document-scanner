from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uuid
import os
from pydantic import BaseModel
from utils import export_results_to_json
from document_processor import DocumentProcessor
import fitz  # PyMuPDF for PDF handling
from PIL import Image
import io
import numpy as np

app = FastAPI(title="OCR Document Categorizer")

# Add CORS middleware - allow frontend on any port during development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def convert_pdf_to_image(pdf_path):
    """
    Convert the first page of a PDF to an image
    """
    doc = fitz.open(pdf_path)
    page = doc.load_page(0)
    mat = fitz.Matrix(2.0, 2.0)
    pix = page.get_pixmap(matrix=mat)

    # Convert to PIL Image
    img_data = pix.tobytes("ppm")
    img = Image.open(io.BytesIO(img_data))

    doc.close()
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
    return {"status": "healthy"}

@app.post("/upload", response_model=CategorizedResult)
async def upload_document(file: UploadFile = File(...), lang: str = "eng", return_regions: bool = False):
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
            # Convert PDF to image
            image = convert_pdf_to_image(temp_filename)
            # Skip document detection for PDFs since they're already clean images
            # Just run OCR directly on the PDF-converted image
            extracted_text, ocr_data, regions = processor.extract_text(image, lang=lang, return_regions=return_regions)
            categorized_result = processor.categorize_text(extracted_text)
        else:
            # For image files, use the full pipeline
            cropped_image = processor.detect_and_crop(temp_filename)
            extracted_text, ocr_data, regions = processor.extract_text(cropped_image, lang=lang, return_regions=return_regions)
            categorized_result = processor.categorize_text(extracted_text)

        # Add text regions to response if requested
        response_data = dict(categorized_result)
        print(f"Return regions flag: {return_regions}")
        print(f"Regions found: {len(regions) if regions else 0}")
        
        if return_regions and regions:
            response_data['text_regions'] = regions
            print(f"Added {len(regions)} text regions to response")
        else:
            print("Not adding text regions to response")

        print(f"Response data keys: {list(response_data.keys())}")
        return JSONResponse(content=response_data)
    except Exception as e:
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
                "document_type": "unknown"
            }
        )
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)

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
            # Convert PDF to image
            image = convert_pdf_to_image(temp_filename)
            # Skip document detection for PDFs since they're already clean images
            # Just run OCR directly on the PDF-converted image
            extracted_text, ocr_data = processor.extract_text(image, lang=lang)
            categorized_result = processor.categorize_text(extracted_text)
        else:
            # For image files, use the full pipeline
            cropped_image = processor.detect_and_crop(temp_filename)
            extracted_text, ocr_data = processor.extract_text(cropped_image, lang=lang)
            categorized_result = processor.categorize_text(extracted_text)

        # Export results to JSON
        export_filename = export_results_to_json(categorized_result)

        return {"result": categorized_result, "export_file": export_filename}
    except Exception as e:
        return {"error": str(e), "result": None, "export_file": None}
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
