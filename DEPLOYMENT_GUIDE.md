# Deployment Guide for OCR Document Categorizer

This guide provides step-by-step instructions for deploying the OCR Document Categorizer application to production environments.

## Prerequisites

- GitHub account
- Render account (for backend)
- Vercel account (for frontend)

## Backend Deployment (to Render)

### Step 1: Prepare Your Repository
1. Push your code to a GitHub repository
2. Make sure the `render.yaml` file is in the root of your repository

### Step 2: Create Render Web Service
1. Go to https://dashboard.render.com
2. Click "New +" and select "Web Service"
3. Connect to your GitHub repository
4. Select your OCR Document Categorizer repository
5. Render will automatically detect it's a Python project
6. Use the following settings:
   - Environment: Python
   - Branch: main (or your default branch)
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
7. Add environment variables:
   - `PYTHON_VERSION`: 3.11.6
   - `ENABLE_TESSERACT`: true
8. Click "Create Web Service"

### Step 3: Note Your Backend URL
- After deployment completes, note the URL assigned to your backend service (e.g., `https://your-app-name.onrender.com`)

## Frontend Deployment (to Vercel)

### Step 1: Prepare Frontend
1. Ensure your frontend is build-ready by running `npm run build` in the `frontend` directory
2. The build output should appear in a `dist` folder

### Step 2: Deploy to Vercel
1. Go to https://vercel.com
2. Sign in with your GitHub account
3. Click "New Project"
4. Import your OCR Document Categorizer repository
5. Vercel will detect it's a static site
6. In the configuration:
   - Build Command: `cd frontend && npm install && npm run build`
   - Output Directory: `frontend/dist`
   - Root Directory: `.`
7. Add environment variable:
   - `REACT_APP_API_URL`: Your Render backend URL from Step 3 above
8. Click "Deploy"

## Configuration Notes

### Environment Variables
- Backend (Render): 
  - `PYTHON_VERSION`: 3.11.6
  - `ENABLE_TESSERACT`: true
- Frontend (Vercel):
  - `REACT_APP_API_URL`: Your Render backend URL

### Important Files
- `render.yaml`: Configuration for Render deployment
- `vercel.json`: Configuration for Vercel deployment

## Post-Deployment Testing

1. Visit your frontend URL provided by Vercel
2. Test document upload functionality
3. Verify that results are displayed correctly
4. Test with various document types and images
5. Verify export functionality works

## Troubleshooting

### Common Issues
- **Tesseract not found**: Ensure the Render environment supports native libraries
- **CORS errors**: Verify that your frontend domain is allowed in the backend CORS configuration
- **Slow processing**: Large images may take longer to process; consider adding image size limitations

### Logs
- Check logs in Render dashboard for backend issues
- Check browser console for frontend issues
- Use Vercel dashboard for frontend logs

## Updating Deployments

### Backend Updates
Changes pushed to your GitHub repository will automatically trigger a new deployment on Render (if you enabled auto-deploy).

### Frontend Updates
Changes pushed to your GitHub repository will automatically trigger a new deployment on Vercel (if you enabled auto-deploy).

## Custom Domains (Optional)

Both Render and Vercel support custom domain setup:
1. In Render dashboard: Go to your web service → Settings → Domains
2. In Vercel dashboard: Go to your project → Settings → Domains
3. Follow the instructions to add and verify your custom domain

## Performance Considerations

- The OCR processing can take several seconds depending on the image size and complexity
- Consider optimizing images before processing
- Monitor your Render service for timeout issues (default is 30 seconds for free tier)
- For production use, consider upgrading to paid tiers for better performance and longer timeouts