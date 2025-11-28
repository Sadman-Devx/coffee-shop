# 🌐 Get Your Permanent URL - Step by Step

You want a URL like `https://healerboys.netlify.app/` that works from ANY device, anywhere!

## ✅ What You Need to Do:

### Step 1: Upload Your Code to GitHub (5 minutes)

1. **Create GitHub Account** (if you don't have one):
   - Go to https://github.com
   - Sign up (it's free)

2. **Create New Repository:**
   - Click the **"+"** icon → **"New repository"**
   - Name: `coffee-shop` (or any name)
   - Make it **Public**
   - Click **"Create repository"**

3. **Upload Your Code:**
   Open PowerShell in your project folder (`D:\coffe shop`) and run:

   ```powershell
   git init
   git add .
   git commit -m "Coffee shop website"
   git branch -M main
    git remote add origin https://github.com/Sadman-Devx/coffee-shop.git
   git push -u origin main
   ```
   
   *(Replace `YOUR_USERNAME` with your actual GitHub username)*

---

### Step 2: Deploy on Render (10 minutes)

1. **Go to Render:**
   - Visit https://render.com
   - Click **"Get Started for Free"**
   - Sign up with your GitHub account

2. **Create Web Service:**
   - Click **"New +"** → **"Web Service"**
   - Select your `coffee-shop` repository
   - Click **"Connect"**

3. **Configure Settings:**
   - **Name:** `coffee-shop` (or any name)
   - **Environment:** `Python 3`
   - **Build Command:** 
     ```
     pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput
     ```
   - **Start Command:**
     ```
     gunicorn coffee_site.wsgi
     ```

4. **Add Environment Variables:**
   Click **"Advanced"** → Add these:
   
   - **Name:** `SECRET_KEY`
   - **Value:** Run this in PowerShell to generate:
     ```powershell
     .\.venv\Scripts\python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
     ```
   
   - **Name:** `DEBUG`
   - **Value:** `False`
   
   - **Name:** `ALLOWED_HOSTS`
   - **Value:** `coffee-shop.onrender.com` (or your app name)

5. **Deploy:**
   - Click **"Create Web Service"**
   - Wait 5-10 minutes
   - **DONE!** ✅

---

## 🎉 Your Permanent URL:

After deployment, you'll get:
**`https://coffee-shop-xyz.onrender.com`**

This URL will work:
- ✅ From your phone
- ✅ From any computer
- ✅ From anywhere in the world
- ✅ 24/7 (always online)

---

## 📱 After Deployment:

1. **Create Admin User:**
   - In Render dashboard, click your service
   - Go to **"Shell"** tab
   - Run: `python manage.py createsuperuser`
   - Enter username and password

2. **Add Coffee Items:**
   - In the same shell, run: `python manage.py populate_coffees`

3. **Access Your Site:**
   - Visit your permanent URL
   - Admin: `https://your-url.onrender.com/admin/`

---

## 🆘 Quick Help:

**If Git commands don't work:**
- Make sure Git is installed: https://git-scm.com/download/win
- Or use GitHub Desktop app (easier!)

**If deployment fails:**
- Check the logs in Render dashboard
- Make sure `requirements.txt` and `Procfile` are in your repository

---

## 🎯 Result:

You'll have a permanent URL like:
- `https://coffee-shop-abc123.onrender.com`

Just like `https://healerboys.netlify.app/` - but for your coffee shop! ☕

**Your website will be accessible from ANYWHERE in the world!** 🌍✨

