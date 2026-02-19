# 🔑 Google Cloud Vision API Setup Guide

## Step 1: Create Google Cloud Account

1. Go to: **https://console.cloud.google.com**
2. Sign in with your Google account
3. Create a new project (or use existing)

---

## Step 2: Enable Vision API

1. In Google Cloud Console, go to: **APIs & Services** → **Library**
2. Search for: **"Cloud Vision API"**
3. Click on it and press **"Enable"**

---

## Step 3: Create Service Account

1. Go to: **APIs & Services** → **Credentials**
2. Click **"Create Credentials"** → **"Service Account"**
3. Fill in:
   - **Service account name**: `ocr-scanner`
   - **Service account ID**: auto-generated
   - **Description**: `OCR Document Scanner API access`
4. Click **"Create and Continue"**
5. Skip role selection (optional)
6. Click **"Done"**

---

## Step 4: Download JSON Key

1. Click on your newly created service account
2. Go to **"Keys"** tab
3. Click **"Add Key"** → **"Create new key"**
4. Select **JSON** format
5. Click **"Create"**
6. **Download the JSON file** (automatically downloads)
7. Rename it to: `service-account-key.json`

---

## Step 5: Add to Render

### Option A: Upload via Render Dashboard (Easiest)

1. Go to: **https://dashboard.render.com**
2. Click your service: `ocr-scanner`
3. Click **"Environment"** tab
4. Click **"Add File"** → **"Upload File"**
5. Upload your `service-account-key.json`
6. Set mount path to: `/app/service-account-key.json`
7. Click **"Save"**
8. **Redeploy** your service

### Option B: Add as Environment Variable

1. Copy the **entire content** of `service-account-key.json`
2. Go to Render dashboard → **Environment**
3. Add new variable:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS_CONTENT`
   - **Value**: Paste the JSON content
4. Click **"Save"**
5. **Redeploy**

---

## Step 6: Test

1. Wait for Render to redeploy (2-3 minutes)
2. Go to your Vercel frontend
3. Upload an image
4. Click "Scan for Text"
5. **Should complete in 1-2 seconds!** ⚡

---

## 📊 Free Tier Limits

| Feature | Limit |
|---------|-------|
| **Free requests** | 1,000 per month |
| **Per day** | ~33 requests |
| **Overage cost** | $1.50 per 1,000 images |

---

## 🔒 Security Notes

- ✅ Service account key is **encrypted** on Render
- ✅ Never commit `service-account-key.json` to GitHub
- ✅ Key only works for your Google Cloud project
- ✅ You can revoke/regenerate keys anytime

---

## 🆘 Troubleshooting

### "Permission denied" error
- Make sure Vision API is **enabled** in Google Cloud Console
- Check service account has **Vision API User** role

### "File not found" error
- Upload `service-account-key.json` to Render
- Or set `GOOGLE_APPLICATION_CREDENTIALS` env variable

### "Quota exceeded" error
- You've used 1,000 free requests
- Wait until next month or add billing

---

## ✅ After Setup:

Your app will:
- ⚡ Scan images in **1-2 seconds** (not 30+ seconds)
- 🎯 Have **better accuracy** (especially for Thai)
- 🚀 **No more timeout errors**
- 💰 Stay **free** for up to 1,000 scans/month

---

**Follow the steps above and your OCR will be BLAZING fast!** 🚀
