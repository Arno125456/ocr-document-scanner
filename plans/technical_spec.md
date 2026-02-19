# OCR Document Categorizer - Technical Specification

## 1. Document Detection and Cropping Module

### 1.1 OpenCV Document Detection Algorithm
```python
def detect_document_contour(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply Canny edge detection
    edged = cv2.Canny(blurred, 75, 200)
    
    # Find contours
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    
    # Sort contours by area (largest first)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:5]
    
    # Loop over contours to find the document contour (rectangle)
    for contour in contours:
        # Approximate the contour
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        
        # If contour has 4 points, we found the document
        if len(approx) == 4:
            return approx
    
    # If no 4-point contour found, return largest contour
    return contours[0] if contours else None
```

### 1.2 Perspective Correction
```python
def perspective_transform(image, contour):
    # Get the four corner points
    points = contour.reshape(4, 2)
    
    # Order points: top-left, top-right, bottom-right, bottom-left
    rect = np.zeros((4, 2), dtype="float32")
    
    s = points.sum(axis=1)
    rect[0] = points[np.argmin(s)]  # top-left
    rect[2] = points[np.argmax(s)]  # bottom-right
    
    diff = np.diff(points, axis=1)
    rect[1] = points[np.argmin(diff)]  # top-right
    rect[3] = points[np.argmax(diff)]  # bottom-left
    
    # Calculate dimensions of the new image
    (tl, tr, br, bl) = rect
    
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    
    # Define destination points for the new image
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    
    # Calculate the perspective transform matrix and apply it
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    
    return warped
```

## 2. OCR Processing Module

### 2.1 Tesseract OCR Configuration
```python
import pytesseract
from PIL import Image
import cv2
import numpy as np

def preprocess_for_ocr(image):
    # Convert to grayscale if needed
    if len(image.shape) == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    else:
        gray = image
    
    # Apply threshold to get image with only black and white
    _, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Apply median blur to remove noise
    denoised = cv2.medianBlur(thresh, 3)
    
    # Convert to PIL Image for pytesseract
    pil_image = Image.fromarray(denoised)
    
    return pil_image

def extract_text_with_tesseract(image):
    # Preprocess image
    processed_img = preprocess_for_ocr(image)
    
    # Configure tesseract options for better accuracy
    config = '--oem 3 --psm 6'
    
    # Extract text
    text = pytesseract.image_to_string(processed_img, config=config)
    
    # Extract detailed data for potential highlighting
    data = pytesseract.image_to_data(processed_img, output_type=pytesseract.Output.DICT, config=config)
    
    return text.strip(), data
```

## 3. Text Categorization Module

### 3.1 Rule-Based Categorization System
```python
import re
from datetime import datetime

class TextCategorizer:
    def __init__(self):
        self.patterns = {
            'date': [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
                r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4}\b',
                r'\b\d{1,2} (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{4}\b'
            ],
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            'phone': [
                r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
                r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}\b'
            ],
            'amount': [
                r'\$\s*\d+(?:[,\.]\d{2,})?',
                r'\b\d+(?:[,\.]\d{2,})?\s*\$'
            ],
            'name': [
                r'(?:Name|Customer|Client):\s*([A-Z][a-z]+\s*[A-Z][a-z]*)',
                r'^([A-Z][a-z]+\s+[A-Z][a-z]+)$'
            ]
        }
        
    def categorize_text(self, text):
        lines = text.split('\n')
        categories = {
            'title': [],
            'date': [],
            'name': [],
            'email': [],
            'phone': [],
            'amount': [],
            'items': [],
            'other': []
        }
        
        # Extract title (usually first significant line)
        for line in lines[:5]:  # Check first 5 lines for title
            line = line.strip()
            if len(line) > 3 and not any(keyword in line.lower() for keyword in ['total', 'amount', 'date', 'email']):
                categories['title'].append(line)
                break
        
        # Process each line for categorization
        for line in lines:
            line = line.strip()
            if not line or len(line) < 3:
                continue
                
            categorized = False
            
            # Check against patterns
            for category, patterns in self.patterns.items():
                for pattern in patterns:
                    matches = re.findall(pattern, line, re.IGNORECASE)
                    if matches:
                        categories[category].extend(matches)
                        categorized = True
                        break
                if categorized:
                    break
            
            # If not categorized by patterns, classify as item or other
            if not categorized:
                if any(word in line.lower() for word in ['item', 'product', 'service', 'qty', 'quantity']):
                    categories['items'].append(line)
                else:
                    categories['other'].append(line)
        
        # Remove duplicates while preserving order
        for category in categories:
            unique_items = []
            for item in categories[category]:
                if item not in unique_items:
                    unique_items.append(item)
            categories[category] = unique_items
            
        return categories
```

## 4. API Endpoint Design

### 4.1 FastAPI Backend Structure
```python
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import uuid
import os
from pydantic import BaseModel

app = FastAPI(title="OCR Document Categorizer")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CategorizedResult(BaseModel):
    title: list[str]
    date: list[str]
    name: list[str]
    email: list[str]
    phone: list[str]
    amount: list[str]
    items: list[str]
    other: list[str]

@app.post("/upload", response_model=CategorizedResult)
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file temporarily
    temp_filename = f"temp_{uuid.uuid4()}_{file.filename}"
    with open(temp_filename, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    try:
        # Process the document
        processor = DocumentProcessor()
        cropped_image = processor.detect_and_crop(temp_filename)
        extracted_text, ocr_data = processor.extract_text(cropped_image)
        categorized_result = processor.categorize_text(extracted_text)
        
        return categorized_result
    finally:
        # Clean up temporary file
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
```

## 5. Frontend Component Structure

### 5.1 Main Upload Component (React)
```jsx
import React, { useState } from 'react';

const DocumentUpload = () => {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const data = await response.json();
      setResult(data);
    } catch (err) {
      setError(err.message || 'An error occurred during processing');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">OCR Document Categorizer</h1>
      
      <form onSubmit={handleSubmit} className="mb-6">
        <div className="mb-4">
          <label className="block text-gray-700 mb-2" htmlFor="file-upload">
            Upload Document Image
          </label>
          <input
            id="file-upload"
            type="file"
            accept="image/*"
            onChange={handleFileChange}
            className="w-full px-3 py-2 border border-gray-300 rounded-md"
          />
        </div>
        
        <button
          type="submit"
          disabled={loading}
          className={`px-4 py-2 rounded-md ${
            loading ? 'bg-gray-400' : 'bg-blue-500 hover:bg-blue-600'
          } text-white`}
        >
          {loading ? 'Processing...' : 'Process Document'}
        </button>
      </form>

      {error && (
        <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
          {error}
        </div>
      )}

      {result && (
        <div className="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
          <h2 className="text-xl font-semibold mb-4">Processed Results</h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <ResultSection title="Title" items={result.title} />
            <ResultSection title="Dates" items={result.date} />
            <ResultSection title="Names" items={result.name} />
            <ResultSection title="Emails" items={result.email} />
            <ResultSection title="Phones" items={result.phone} />
            <ResultSection title="Amounts" items={result.amount} />
            <div className="col-span-2">
              <ResultSection title="Items" items={result.items} />
            </div>
            <div className="col-span-2">
              <ResultSection title="Other" items={result.other} />
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

const ResultSection = ({ title, items }) => {
  if (!items || items.length === 0) return null;

  return (
    <div className="mb-4">
      <h3 className="font-medium text-gray-700 mb-1">{title}</h3>
      <ul className="list-disc pl-5 space-y-1">
        {items.map((item, index) => (
          <li key={index} className="text-sm text-gray-600">{item}</li>
        ))}
      </ul>
    </div>
  );
};
```

## 6. Dependencies

### 6.1 Backend requirements.txt
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
opencv-python==4.8.1.78
pytesseract==0.3.10
Pillow==10.1.0
numpy==1.24.3
python-multipart==0.0.6
```

### 6.2 Frontend package.json
```
{
  "name": "ocr-frontend",
  "version": "0.1.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.1.0",
    "autoprefixer": "^10.4.16",
    "postcss": "^8.4.31",
    "tailwindcss": "^3.3.5"
  },
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview"
  }
}
```

## 7. Deployment Configuration

### 7.1 Render Backend YAML
```yaml
services:
  - type: web
    name: ocr-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.6
```

### 7.2 Vercel Frontend Configuration
```json
{
  "version": 2,
  "builds": [
    {
      "src": "frontend/package.json",
      "use": "@vercel/static-build",
      "config": {
        "distDir": "dist"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "frontend/dist/$1"
    }
  ]
}