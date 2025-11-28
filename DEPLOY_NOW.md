# 🚀 Deploy Your Coffee Shop Website - Quick Start

Your website is ready to deploy! Follow these simple steps to get a permanent URL.

## ⚡ Fastest Method: Render (5 minutes)

### Step 1: Create Account
1. Go to **https://render.com**
2. Click **"Get Started for Free"**
3. Sign up with GitHub, Google, or email

### Step 2: Deploy Your Site
1. Click **"New +"** → **"Web Service"**
2. Choose one:
   - **Option A:** Connect GitHub repo (if you have one)
   - **Option B:** Use "Public Git repository" and paste your repo URL
   - **Option C:** Use "Manual Deploy" and upload your project folder

### Step 3: Configure Settings
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

### Step 4: Add Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:
- `SECRET_KEY`: Run this command to generate one:
  ```bash
  python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
  ```
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: `your-app-name.onrender.com` (replace with your actual app name)

### Step 5: Deploy!
1. Click **"Create Web Service"**
2. Wait 5-10 minutes for deployment
3. Your site will be live at: **https://your-app-name.onrender.com** 🎉

---

## 📋 Alternative: Railway (Also Free)

1. Go to **https://railway.app**
2. Sign up with GitHub
3. Click **"New Project"** → **"Deploy from GitHub repo"**
4. Select your repository
5. Railway auto-detects Python - it will work automatically!
6. Your site: **https://your-app.up.railway.app**

---

## 🔧 Before Deploying - Run These Commands

```bash
# 1. Collect static files
.\.venv\Scripts\python manage.py collectstatic --noinput

# 2. Test locally (optional)
.\.venv\Scripts\python manage.py runserver
```

---

## 📝 Important Notes

1. **Database:** Your SQLite database will be created automatically on first deployment
2. **Admin Access:** After deployment, create superuser:
   - Use Render's shell: `python manage.py createsuperuser`
   - Or run locally and sync database
3. **Coffee Items:** Run this after first deployment:
   ```bash
   python manage.py populate_coffees
   ```

---

## 🌐 Your Permanent URL

Once deployed, you'll get a URL like:
- **Render:** `https://coffee-shop-xyz.onrender.com`
- **Railway:** `https://coffee-shop-production.up.railway.app`

This URL will work from **anywhere in the world**! 🌍

---

## ❓ Need Help?

- Render Support: https://render.com/docs
- Check deployment logs if something goes wrong
- Make sure all files are uploaded (especially `requirements.txt`, `Procfile`)

**Your coffee shop website will be live in minutes!** ☕✨

