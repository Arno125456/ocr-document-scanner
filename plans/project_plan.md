# OCR Document Categorizer - Project Plan

## Project Overview
Build a web application that takes photos of documents, detects and crops the document area, extracts text using OCR, and categorizes the text into structured fields.

## Technical Architecture

### Backend (Python/FastAPI)
- **Framework**: FastAPI for high-performance API
- **Document Processing**: OpenCV for document detection and cropping
- **OCR**: Tesseract via pytesseract
- **Image Processing**: Pillow and numpy
- **Dependencies**: opencv-python, pytesseract, pillow, numpy, fastapi, uvicorn

### Frontend (React)
- **Framework**: React with Vite
- **Styling**: Tailwind CSS
- **Features**: Drag & drop upload, camera capture, results display
- **State Management**: React hooks

### Deployment Strategy
- **Backend**: Deploy to Render (supports Tesseract)
- **Frontend**: Deploy to Vercel
- **Domain**: Custom domain or subdomains

## Implementation Timeline (3 Days)

### Day 1: Core Backend Development
- Set up FastAPI project structure
- Implement document detection and cropping with OpenCV
- Integrate Tesseract OCR functionality
- Create basic text categorization system
- Test backend API endpoints

### Day 2: Frontend and Integration
- Create React frontend with upload interface
- Implement image preview and processing flow
- Connect frontend to backend API
- Add responsive design with Tailwind CSS
- Test full pipeline integration

### Day 3: Polish and Deployment
- Add bonus features (perspective correction, text highlighting)
- Improve UI/UX and error handling
- Deploy backend to Render
- Deploy frontend to Vercel
- Final testing and documentation

## System Flow
```
Upload Image → Document Detection → Cropping → OCR → Text Extraction → Categorization → Structured Output
```

## Key Features

### MVP Requirements
- [ ] Document detection in cluttered backgrounds
- [ ] Automatic cropping of document area
- [ ] OCR text extraction
- [ ] Rule-based text categorization
- [ ] Web interface for uploading and viewing results
- [ ] Working deployment

### Bonus Features
- [ ] Perspective correction for skewed documents
- [ ] Visual highlighting of detected text regions
- [ ] Export functionality (JSON/PDF)
- [ ] Multiple document type recognition
- [ ] Mobile-friendly camera capture

## Backend API Endpoints
- `POST /upload` - Upload image and process document
- `GET /health` - Health check endpoint

## File Structure
```
project/
├── backend/
│   ├── main.py
│   ├── document_processor.py
│   ├── ocr_handler.py
│   ├── text_categorizer.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.jsx
│   ├── public/
│   ├── package.json
│   └── tailwind.config.js
├── plans/
│   └── project_plan.md
└── README.md
```

## Risk Mitigation
- **Tesseract deployment**: Use Render which supports native libraries
- **Document detection accuracy**: Implement fallback to basic contour detection
- **OCR quality**: Add image preprocessing to enhance quality before OCR
- **Time constraints**: Focus on core functionality first, add bonuses if time permits