# 🚀 Deployment Guide for Arno125456

## Your Personalized Quick Start

**GitHub Username**: Arno125456  
**Repository**: ocr-document-scanner

---

## ⚡ Super Quick Deploy (5 Minutes)

### Step 1: Run Deploy Script
```bash
# Double-click this file:
quick-deploy.bat
```

### Step 2: Create GitHub Repository
1. Go to: **https://github.com/new**
2. Repository name: `ocr-document-scanner`
3. Public or Private (your choice)
4. Click **"Create repository"**

### Step 3: Push Code to GitHub
```bash
# Run these commands in your terminal:
cd d:\Project-OCR
git remote add origin https://github.com/Arno125456/ocr-document-scanner.git
git branch -M main
git push -u origin main
```

### Step 4: Deploy Backend on Render
1. Go to: **https://render.com**
2. Sign in with **GitHub**
3. Click **"New +"** → **"Blueprint"**
4. Select repository: **Arno125456/ocr-document-scanner**
5. Render will auto-detect `render.yaml`
6. Click **"Apply"**
7. Wait 3-5 minutes
8. **Copy your backend URL** (e.g., `https://ocr-document-scanner-xyz.onrender.com`)

### Step 5: Deploy Frontend on Vercel
1. Go to: **https://vercel.com**
2. Sign in with **GitHub**
3. Click **"Add New..."** → **"Project"**
4. Import: **Arno125456/ocr-document-scanner**
5. **Root Directory**: `frontend`
6. **Environment Variable**:
   - Name: `VITE_API_URL`
   - Value: Your Render backend URL from Step 4
7. Click **"Deploy"**
8. Wait 1-2 minutes

### Step 6: Test Your App!
1. Vercel shows your live URL
2. Click to open
3. Upload a document
4. Click "Scan for Text"
5. Click "Show Text"
6. Click highlighted text to extract!

---

## 🔗 Your Links

| Service | URL | Status |
|---------|-----|--------|
| **GitHub** | https://github.com/Arno125456/ocr-document-scanner | ✅ Code Repository |
| **Render** | https://dashboard.render.com | 🔄 Deploy Backend |
| **Vercel** | https://vercel.com/dashboard | 🔄 Deploy Frontend |

---

## 📋 Deployment Checklist

- [ ] Run `quick-deploy.bat`
- [ ] Create GitHub repository
- [ ] Push code to GitHub
- [ ] Deploy on Render (backend)
- [ ] Copy Render backend URL
- [ ] Deploy on Vercel (frontend)
- [ ] Add `VITE_API_URL` to Vercel
- [ ] Test the live app
- [ ] Share your Vercel URL!

---

## 🎯 What Gets Deployed

### Backend (Render)
- FastAPI server
- Tesseract OCR (English + Thai)
- OpenCV document detection
- Text categorization AI
- **URL**: `https://YOUR-APP.onrender.com`

### Frontend (Vercel)
- React + Vite
- Interactive text highlighting
- Copy to clipboard
- Mobile responsive
- **URL**: `https://ocr-document-scanner.vercel.app`

---

## 💰 Cost: $0/month

| Service | Plan | Cost |
|---------|------|------|
| GitHub | Free | $0 |
| Render | Free (750 hrs/mo) | $0 |
| Vercel | Free | $0 |
| **Total** | | **$0** 🎉 |

---

## 🔧 Troubleshooting

### Backend Issues
**Render shows "Build Failed"**
- Check logs: Render Dashboard → Logs
- Verify `Dockerfile` is in root directory
- Ensure `render.yaml` exists

**Backend sleeps after 15 min**
- This is normal on free tier
- Visit URL to wake it up (takes 30 sec)
- Or upgrade to paid plan ($7/mo)

### Frontend Issues
**"Failed to fetch" error**
- Update `VITE_API_URL` in Vercel settings
- Must use full URL: `https://xxx.onrender.com`
- Redeploy after changing

**Build fails**
- Check Vercel logs: Dashboard → Deployments
- Verify Node.js version (v16+)
- Test locally: `npm run build`

---

## 📱 After Deployment

Your app will be:
- ✅ Live on the internet
- ✅ Accessible from any device
- ✅ HTTPS secured automatically
- ✅ Globally distributed via CDN

**Share your Vercel URL with anyone!**

---

## 🎉 Success Criteria

✅ Backend health check works:  
`https://YOUR-RENDER-URL.onrender.com/health`  
Returns: `{"status":"healthy"}`

✅ Frontend loads:  
`https://ocr-document-scanner.vercel.app`

✅ You can upload images  
✅ Text scanning works  
✅ Clicking text extracts it  
✅ Copy to clipboard works  

---

## 🆘 Need Help?

**Deployment Guide**: See `DEPLOYMENT.md`  
**Checklist**: See `DEPLOYMENT_CHECKLIST.md`  
**Render Support**: https://community.render.com  
**Vercel Support**: https://vercel.com/docs  

---

**Good luck, Arno125456! Your OCR app is ready to go live! 🚀**
