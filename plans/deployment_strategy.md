# OCR Document Categorizer - Deployment Strategy

## Overview
This document outlines the deployment strategy for the OCR Document Categorizer application, focusing on reliable and cost-effective hosting solutions suitable for a student project.

## Platform Selection

### Backend: Render
- **Why Render**: Supports Python applications with native libraries like OpenCV and Tesseract
- **Pricing**: Free tier available with 100 hours/month (adequate for development/testing)
- **Benefits**: 
  - Native support for Tesseract OCR
  - Automatic deployments from GitHub
  - Environment variable management
  - Built-in SSL certificate

### Frontend: Vercel
- **Why Vercel**: Excellent for React applications, free tier generous
- **Pricing**: Hobby plan free forever
- **Benefits**:
  - Seamless integration with React/Vite
  - Global CDN distribution
  - Automatic deployments from Git
  - Custom domain support

## Backend Deployment (Render)

### Pre-deployment Checklist
- [ ] Test application locally with production settings
- [ ] Verify all dependencies in requirements.txt
- [ ] Confirm Tesseract installation works in container
- [ ] Optimize Dockerfile for faster builds
- [ ] Set up environment variables
- [ ] Test with sample documents

### Render Service Configuration
```yaml
services:
  - type: web
    name: ocr-backend
    env: python
    region: oregon
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: PYTHON_VERSION
        value: 3.11.6
      - key: ENABLE_TESSERACT
        value: true
```

### Build Process
1. Render clones the repository
2. Installs Python dependencies from requirements.txt
3. Sets up Tesseract OCR
4. Starts the FastAPI application on the assigned PORT

### Environment Variables
- `PORT`: Assigned by Render (don't set manually)
- `TESSERACT_PATH`: Path to Tesseract executable (if needed)

### Scaling Considerations
- Free tier: Limited to 100 build minutes/day
- Cold start times for free services
- Memory limit: 512MB for free tier
- Timeout: 30 seconds for API requests

## Frontend Deployment (Vercel)

### Pre-deployment Checklist
- [ ] Build application locally (`npm run build`)
- [ ] Verify all assets are correctly referenced
- [ ] Test production build locally
- [ ] Confirm API endpoints are correctly configured
- [ ] Optimize bundle size

### Vercel Configuration (vercel.json)
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
  ],
  "env": {
    "REACT_APP_API_URL": "https://your-render-app-name.onrender.com"
  }
}
```

### Build Process
1. Vercel clones the repository
2. Runs `npm install` in the frontend directory
3. Executes `npm run build`
4. Serves the static build files

## Deployment Steps

### Phase 1: Backend Deployment
1. Create Render account
2. Create new Web Service
3. Connect to GitHub repository
4. Configure build settings
5. Set environment variables
6. Deploy and verify

### Phase 2: Frontend Deployment
1. Create Vercel account
2. Import project from GitHub
3. Configure build settings
4. Set environment variables (API URL)
5. Deploy and verify

### Phase 3: Post-Deployment Verification
1. Test API endpoints directly
2. Verify frontend-backend communication
3. Test complete workflow
4. Check error handling

## Domain Configuration

### Custom Domain Setup
1. Purchase domain (optional, can use free subdomains)
2. Configure DNS records:
   - Frontend: Point to Vercel's assigned domain
   - Backend: Point to Render's assigned domain
3. Verify SSL certificates

### Default URLs
- Backend: `https://your-app-name.onrender.com`
- Frontend: `https://your-project.vercel.app`

## Monitoring and Maintenance

### Health Checks
- Backend: `/health` endpoint returning status
- Frontend: Monitor page load times
- Error tracking: Log errors to console/file

### Performance Monitoring
- Response times
- Memory usage
- Error rates
- User experience metrics

### Backup Strategy
- Code: Maintained in GitHub
- Configuration: Documented in this file
- No persistent data to backup (stateless application)

## Rollback Plan
1. Identify issue and stop new deployments
2. Revert to previous stable commit
3. Redeploy previous version
4. Verify functionality
5. Investigate root cause

## Cost Management
- Free tier usage: Monitor hours to stay within limits
- Upgrade criteria: If usage exceeds free tier consistently
- Optimization: Reduce processing time to minimize resource usage

## Security Considerations
- Input validation: Sanitize uploaded images
- Rate limiting: Prevent abuse of API
- File type validation: Accept only image formats
- API keys: Secure any third-party service credentials