# 📄 OCR Document Scanner

A production-ready web application that scans documents, detects text with interactive highlighting, and extracts information with AI-powered categorization.

## ✨ Features

- **📸 Document Upload** - Support for images (PNG, JPG, GIF) and PDFs
- **🔍 Smart Text Detection** - Automatically detects and highlights all text regions
- **👆 Interactive Selection** - Click any highlighted text to extract it (like Google Translate)
- **🌐 Multi-Language** - English and Thai OCR support
- **📊 Smart Categorization** - Auto-detects document type and categorizes extracted text
- **📋 Copy to Clipboard** - One-click copy for selected text
- **📱 Mobile Responsive** - Works on all devices
- **☁️ Cloud Ready** - Deploy instantly to Render + Vercel

## 🚀 Quick Deploy (5 Minutes)

Your app is **production-ready**! Deploy instantly:

### Option 1: One-Click Deploy (Recommended)

**Backend**: [Render](https://render.com) (Free tier)  
**Frontend**: [Vercel](https://vercel.com) (Free tier)

**Steps:**
1. Run `quick-deploy.bat` to prepare Git
2. Push to GitHub
3. Deploy on Render (connect GitHub, auto-deploys)
4. Deploy on Vercel (connect GitHub, auto-deploys)

📖 **Full instructions**: See [DEPLOYMENT.md](DEPLOYMENT.md)

### Option 2: Local Testing

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

Open http://localhost:5173

## 📦 What's Included

```
project/
├── backend/              # FastAPI backend
│   ├── main.py          # API endpoints
│   ├── document_processor.py  # Document detection & cropping
│   ├── ocr_handler.py   # Tesseract OCR with region detection
│   └── text_categorizer.py  # AI text categorization
├── frontend/            # React + Vite frontend
│   ├── src/
│   │   ├── App.jsx     # Main application
│   │   └── App.css     # Styling
│   └── .env.example    # Environment variables template
├── Dockerfile          # Production Docker config
├── render.yaml         # Render deployment config
├── vercel.json         # Vercel deployment config
├── quick-deploy.bat    # Windows quick setup script
└── DEPLOYMENT.md       # Detailed deployment guide
```

## 🎯 Use Cases

- **Invoices & Receipts** - Extract amounts, dates, vendor info
- **ID Cards & Documents** - Extract names, ID numbers, addresses
- **Letters & Contracts** - Extract parties, dates, terms
- **Bank Statements** - Extract transactions, balances
- **Any Document** - Universal text extraction with smart categorization

## 🔧 Tech Stack

**Backend:**
- Python 3.11 + FastAPI
- OpenCV (document detection)
- Tesseract OCR (text extraction)
- Pytesseract (OCR wrapper)

**Frontend:**
- React 18 + Vite
- Tailwind CSS
- React-PDF (PDF support)

**Deployment:**
- Docker (containerization)
- Render (backend hosting)
- Vercel (frontend CDN)

## 📊 API Endpoints

### POST /upload
Upload document for processing

**Parameters:**
- `file`: Image or PDF file
- `lang`: OCR language (eng, tha, eng+tha)
- `return_regions`: true/false (for text highlighting)

**Response:**
```json
{
  "title": ["Document Title"],
  "date": ["2024-01-15"],
  "amount": ["$1,234.56"],
  "document_type": "invoice",
  "text_regions": [
    {
      "text": "Line of text",
      "bbox": {
        "x_percent": 10.5,
        "y_percent": 20.3,
        "width_percent": 45.2,
        "height_percent": 3.1
      }
    }
  ]
}
```

### GET /health
Health check endpoint

## 🌍 Deployment Platforms

| Platform | Purpose | Cost |
|----------|---------|------|
| Render | Backend | Free (sleeps after 15min) |
| Vercel | Frontend | Free (always on) |
| Railway | Alternative Backend | $5/month (no sleep) |

## 📝 Environment Variables

### Frontend (.env)
```env
VITE_API_URL=https://your-backend.onrender.com
```

### Backend (auto-configured in Docker)
```env
TESSDATA_PREFIX=/usr/share/tesseract-ocr/4.00/tessdata
```

## 🔐 Security

- ✅ CORS configured for production
- ✅ Input validation on all endpoints
- ✅ Temporary file cleanup
- ✅ HTTPS enforced by platforms
- ✅ No sensitive data logged

## 📈 Performance

- **OCR Speed**: ~2-5 seconds per page
- **Document Detection**: <1 second
- **Text Region Overlay**: Instant (client-side)
- **Global CDN**: Vercel edge network

## 🐛 Troubleshooting

**Backend not responding?**
- Check Render logs
- Verify Tesseract installation
- Check /health endpoint

**Text regions not showing?**
- Ensure `return_regions=true` in API call
- Check browser console for errors
- Verify image format (use PNG/JPG, not PDF for regions)

**CORS errors?**
- Update VITE_API_URL in Vercel env vars
- Redeploy frontend after changes

## 📞 Support

- **Deployment Issues**: See [DEPLOYMENT.md](DEPLOYMENT.md)
- **OCR Accuracy**: Try clearer images, adjust language setting
- **Build Errors**: Check Node.js (v16+) and Python (v3.8+) versions

## 🎉 Ready to Deploy!

1. Run `quick-deploy.bat`
2. Push to GitHub
3. Deploy on Render + Vercel
4. Share your live URL!

**Your production-ready OCR app is just minutes away!** 🚀

---

**License**: MIT  
**Author**: Your Name  
**Built with**: FastAPI + React + Tesseract OCR
