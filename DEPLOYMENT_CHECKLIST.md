# ✅ Deployment Checklist

## Pre-Deployment (Do This First)

- [ ] Run `quick-deploy.bat` to prepare Git
- [ ] Create GitHub account (if you don't have one)
- [ ] Create Render account (use GitHub login)
- [ ] Create Vercel account (use GitHub login)

## Deployment Steps

### 1. GitHub Repository
- [ ] Create new repository on GitHub
- [ ] Copy repository URL
- [ ] Run commands from quick-deploy.bat output
- [ ] Verify code is on GitHub

### 2. Backend (Render)
- [ ] Go to https://render.com
- [ ] Click "New +" → "Blueprint"
- [ ] Connect your GitHub repository
- [ ] Verify render.yaml is detected
- [ ] Click "Apply"
- [ ] Wait 3-5 minutes for deployment
- [ ] Copy your backend URL (e.g., https://xxx.onrender.com)
- [ ] Test health endpoint: https://YOUR-URL.onrender.com/health

### 3. Frontend (Vercel)
- [ ] Go to https://vercel.com
- [ ] Click "Add New..." → "Project"
- [ ] Import GitHub repository
- [ ] Set Root Directory: `frontend`
- [ ] Add Environment Variable:
  - Name: `VITE_API_URL`
  - Value: Your Render backend URL from step 2
- [ ] Click "Deploy"
- [ ] Wait 1-2 minutes

### 4. Testing
- [ ] Open your Vercel URL
- [ ] Upload a test image
- [ ] Click "Scan for Text"
- [ ] Click "Show Text" button
- [ ] Verify blue boxes appear on text
- [ ] Click a text box
- [ ] Verify text appears in "Selected Text" box
- [ ] Click "Copy Text" button
- [ ] Verify text copies to clipboard

## Post-Deployment

- [ ] Share your Vercel URL
- [ ] Test on mobile device
- [ ] Test with different document types
- [ ] Monitor Render logs for errors
- [ ] Monitor Vercel analytics

## Troubleshooting

### Backend Issues
- Check Render logs: Dashboard → Logs
- Test API directly: https://YOUR-URL.onrender.com/health
- Verify Tesseract: Check logs for "tesseract" errors

### Frontend Issues
- Check Vercel logs: Dashboard → Your Project → Deployments
- Open browser console (F12) for errors
- Verify VITE_API_URL is set correctly

### Common Problems

**"Failed to fetch" error:**
- Update VITE_API_URL in Vercel
- Redeploy frontend

**No text regions:**
- Use clear images with good contrast
- Try English language first
- Check backend logs for OCR errors

**CORS errors:**
- Wait 2 minutes after backend deployment
- Clear browser cache
- Redeploy frontend

## Success Criteria

✅ Backend health check returns: `{"status": "healthy"}`  
✅ Frontend loads without errors  
✅ Image upload works  
✅ Text scanning detects regions  
✅ Clicking text boxes shows selected text  
✅ Copy to clipboard works  

## Next Steps

1. Share your live URL with users
2. Monitor usage on Render/Vercel dashboards
3. Consider upgrading if you hit free tier limits
4. Add custom domain (optional)

---

**🎉 Congratulations! Your OCR app is live and ready to use!**
