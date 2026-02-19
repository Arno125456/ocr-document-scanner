# 🚀 Instant Deployment Guide

## Quick Start (5 Minutes)

This guide will help you deploy the OCR Document Scanner in under 5 minutes using **Render (Backend)** + **Vercel (Frontend)** - both with **free tiers**.

---

## 📋 Prerequisites

- GitHub account (free)
- Render account (free - use GitHub login)
- Vercel account (free - use GitHub login)

---

## Step 1: Push to GitHub

```bash
# Initialize git (if not already done)
cd d:\Project-OCR
git init
git add .
git commit -m "Initial commit - OCR Document Scanner"

# Create a new repository on GitHub, then:
git remote add origin https://github.com/YOUR_USERNAME/ocr-document-scanner.git
git branch -M main
git push -u origin main
```

---

## Step 2: Deploy Backend on Render

### 2.1 Go to [Render.com](https://render.com)
1. Click **"Get Started for Free"**
2. Sign in with **GitHub**
3. Click **"New +"** → **"Blueprint"**

### 2.2 Connect Your Repository
1. Click **"Connect repository"**
2. Select your `ocr-document-scanner` repository
3. Render will auto-detect the `render.yaml` file

### 2.3 Configure Deployment
- **Name**: `ocr-document-scanner` (or your choice)
- **Region**: Choose closest to you (e.g., Oregon for US, Frankfurt for EU)
- **Branch**: `main`
- **Root Directory**: Leave blank
- **DockerfilePath**: `./Dockerfile` (auto-detected)

### 2.4 Deploy!
1. Click **"Apply"**
2. Wait 3-5 minutes for first deployment
3. Copy your backend URL (e.g., `https://ocr-document-scanner.onrender.com`)

**✅ Backend is live!**

---

## Step 3: Deploy Frontend on Vercel

### 3.1 Go to [Vercel.com](https://vercel.com)
1. Click **"Add New..."** → **"Project"**
2. Import your GitHub repository `ocr-document-scanner`

### 3.2 Configure Build Settings
- **Framework Preset**: Vite
- **Root Directory**: `frontend`
- **Build Command**: `npm run build`
- **Output Directory**: `dist`

### 3.3 Add Environment Variable
Click **"Environment Variables"** → **"Add"**:
- **Name**: `VITE_API_URL`
- **Value**: `https://YOUR-BACKEND-URL.onrender.com` (from Step 2)

### 3.4 Deploy!
1. Click **"Deploy"**
2. Wait 1-2 minutes

**✅ Frontend is live!**

---

## Step 4: Test Your App

1. Vercel will show your live URL (e.g., `https://ocr-document-scanner.vercel.app`)
2. Click to open
3. Upload a document image
4. Click "Scan for Text"
5. Click "Show Text" to see highlighted regions
6. Click any highlighted text to extract it!

---

## 🔧 Troubleshooting

### Backend Issues

**Problem**: Backend shows "Tesseract not found"
```bash
# Check Render logs for:
apt-get install tesseract-ocr
```

**Problem**: CORS errors
- Ensure backend URL in frontend `.env` is correct
- Check Render logs for CORS configuration

### Frontend Issues

**Problem**: "Failed to fetch" errors
- Update `VITE_API_URL` in Vercel environment variables
- Redeploy frontend after changing URL

**Problem**: Build fails
```bash
# Test locally first:
cd frontend
npm install
npm run build
```

---

## 📊 Monitoring

### Render Dashboard
- View logs: Render Dashboard → Your Service → Logs
- Check health: `https://YOUR-URL.onrender.com/health`

### Vercel Dashboard
- View deployments: Vercel Dashboard → Your Project → Deployments
- View analytics: Vercel Dashboard → Your Project → Analytics

---

## 💰 Cost (Free Tier Limits)

### Render Free Tier
- ✅ 750 hours/month (enough for 1 service always-on)
- ✅ 512 MB RAM
- ✅ 0.5 GB disk storage
- ⚠️ Backend sleeps after 15 min of inactivity

### Vercel Free Tier
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN

---

## 🔄 Updating Your App

```bash
# Make changes locally
git add .
git commit -m "Update feature"
git push

# Both Render and Vercel will auto-deploy!
```

---

## 🎯 Alternative: Deploy on Railway (Easier, $5/month)

If you want to avoid Render's sleep issue:

1. Go to [Railway.app](https://railway.app)
2. Click **"New Project"** → **"Deploy from GitHub"**
3. Select your repository
4. Add these environment variables:
   - `PYTHON_VERSION`: `3.11.0`
5. Deploy backend
6. Update `VITE_API_URL` in Vercel to Railway URL

**Cost**: ~$5/month for always-on backend

---

## 📱 Share Your App!

Your app is now:
- ✅ Live on the internet
- ✅ Accessible from any device
- ✅ Automatically HTTPS secured
- ✅ Globally distributed via CDN

**Share the Vercel URL with anyone!**

---

## 🆘 Need Help?

- **Render Support**: [community.render.com](https://community.render.com)
- **Vercel Support**: [vercel.com/docs](https://vercel.com/docs)
- **Tesseract Issues**: Check backend logs for OCR errors

---

**🎉 Congratulations! Your OCR Document Scanner is now live!**
