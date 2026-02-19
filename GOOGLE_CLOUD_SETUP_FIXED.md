# 🔑 Google Cloud Credentials Setup - FIXED

## ⚠️ **IMPORTANT: Environment Variables Don't Work Well for JSON**

Render's environment variables corrupt complex JSON with newlines. Use **File Upload** instead!

---

## ✅ **Method 1: Upload File Directly (RECOMMENDED)**

### **Step 1: Go to Render Dashboard**
https://dashboard.render.com

### **Step 2: Click Your Service**
Click: **`ocr-scanner-xvib`**

### **Step 3: Click "Files" Tab**
(Not Environment!)

### **Step 4: Add New File**
Click **"Add File"** or **"New File"**

### **Step 5: Fill In:**
- **File Path**: `/app/service-account-key.json`
- **Content**: Paste your **ENTIRE** `service-account-key.json` content
  - Make sure it includes `-----BEGIN PRIVATE KEY-----` and `-----END PRIVATE KEY-----`
  - Keep ALL the `\n` characters AS-IS (don't change them)

### **Step 6: Save**
Click **"Save"**

### **Step 7: Add Environment Variable**
1. Go to **"Environment"** tab
2. Click **"Add Environment Variable"**
3. Fill in:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS`
   - **Value**: `/app/service-account-key.json`
4. Click **"Save Changes"**

### **Step 8: Redeploy**
1. Go to **"Overview"** or **"Logs"**
2. Click **"Manual Deploy"** or **"Redeploy"**
3. Wait 2-3 minutes

---

## 🎯 **Method 2: Use Base64 Encoding (Alternative)**

If Method 1 doesn't work:

### **Step 1: Encode Your JSON**
Go to: https://www.base64encode.org/

Paste your entire `service-account-key.json` content and click **ENCODE**

Copy the base64 string (it will be very long)

### **Step 2: Add to Render**
1. Go to Render → Your service → **Environment**
2. Add variable:
   - **Name**: `GOOGLE_APPLICATION_CREDENTIALS_BASE64`
   - **Value**: *(Paste the base64 string)*
3. Save and redeploy

The code will automatically decode it!

---

## ✅ **After Setup:**

Upload an image and scan - should complete in **1-2 seconds!** ⚡

---

**Use Method 1 (File Upload) - it's the most reliable!** 🚀
