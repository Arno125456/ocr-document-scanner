# Testing Guide for OCR Document Categorizer

This guide provides instructions on how to test the OCR Document Categorizer application locally.

## Prerequisites

- Python 3.8 or higher
- Node.js and npm (for frontend development)
- Tesseract OCR installed on your system (for full functionality)

### Installing Tesseract OCR

Before running the application, you need to install Tesseract OCR on your system:

#### Windows:
1. Download Tesseract from: https://github.com/UB-Mannheim/tesseract/wiki
2. Run the installer and follow the installation steps
3. Add the installation directory (typically `C:\Program Files\Tesseract-OCR`) to your system PATH

#### macOS:
```bash
brew install tesseract
```

#### Linux (Ubuntu/Debian):
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
```

## Setting Up for Testing

### Backend Setup

1. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the backend server:
```bash
cd backend
uvicorn main:app --reload
```
The backend will start on `http://localhost:8000`

### Frontend Setup (Alternative Method)

If you want to test the full React application:

1. Install frontend dependencies:
```bash
cd frontend
npm install
```

2. Start the development server:
```bash
cd frontend
npm run dev
```

The frontend will start on `http://localhost:5173`

## Testing Methods

### Method 1: Using the Simple HTML Interface (Recommended for Quick Testing)

Open the `test_frontend.html` file directly in your browser. This provides a simple interface to:

- Upload document images
- Send them to the backend for processing
- View categorized results

The interface is pre-configured to connect to `http://localhost:8000`.

### Method 2: Using the Full React Application

1. Ensure both backend and frontend servers are running
2. Open `http://localhost:5173` in your browser
3. Use the application as described below

## Testing Process

1. With the backend server running (`http://localhost:8000`), open your chosen interface
2. Upload a document image (JPG, PNG, etc.)
3. The application will process the image and return categorized results

## What to Test

### Core Functionality
- Document detection accuracy with various backgrounds
- OCR quality with different fonts and image qualities
- Text categorization accuracy
- Perspective correction for skewed documents
- Mobile responsiveness of the UI

### Categories to Verify
The application should categorize text into:
- **Title**: Document titles or headers
- **Date**: Various date formats
- **Name**: Names identified in the document
- **Email**: Email addresses
- **Phone**: Phone numbers in various formats
- **Amount**: Monetary amounts
- **Items**: Product names, service items, etc.
- **Other**: Remaining text that doesn't fit other categories

## Sample Test Images

Try the application with:
- Receipts
- Business cards
- Invoices
- Forms
- Documents with various backgrounds
- Documents with different orientations (to test perspective correction)

## API Testing

You can also test the backend API directly:

### Health Check
```
GET http://localhost:8000/health
```

### Document Upload
```
POST http://localhost:8000/upload
Content-Type: multipart/form-data

Form Data: file=<your-image-file>
```

### Upload with Export
```
POST http://localhost:8000/upload-with-export
Content-Type: multipart/form-data

Form Data: file=<your-image-file>
```

## Troubleshooting Common Issues

### Backend Not Starting
- Ensure all dependencies are installed
- Check that Tesseract is installed and accessible

### OCR Not Working
- Verify Tesseract is installed correctly
- Check that the image is clear and readable

### CORS Errors
- The backend allows all origins by default during development

### Slow Processing
- Large images take longer to process
- Consider resizing large images before processing

## Expected Results

After uploading an image, you should see:
- Processed results with categorized text
- Appropriate categorization of dates, names, amounts, etc.
- Perspective correction applied if the document was skewed

## Stopping the Applications

To stop the backend server:
- Press `Ctrl+C` in the terminal where it's running

To stop the frontend development server:
- Press `Ctrl+C` in the terminal where it's running
