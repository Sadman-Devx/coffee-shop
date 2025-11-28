# Coffee Shop Website - Deployment Guide

This guide will help you deploy your coffee shop website to make it accessible from anywhere on the internet.

## Quick Deployment Options

### Option 1: Render (Recommended - Free & Easy)

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up for a free account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository (or upload files)
   - Or use Render's GitHub integration

3. **Configure Settings:**
   - **Name:** coffee-shop (or any name you like)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command:** `gunicorn coffee_site.wsgi`
   - **Python Version:** 3.13.7

4. **Add Environment Variables:**
   - `SECRET_KEY`: Generate a new secret key (you can use: `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: `False` (for production)
   - `ALLOWED_HOSTS`: Your Render URL (e.g., `your-app.onrender.com`)

5. **Deploy!**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Your site will be live at: `https://your-app.onrender.com`

### Option 2: Railway (Free Tier Available)

1. **Create Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo" or "Empty Project"

3. **Configure:**
   - Add `requirements.txt` (already created)
   - Railway auto-detects Python projects
   - Add environment variables if needed

4. **Deploy**
   - Railway will automatically deploy
   - Get your URL: `https://your-app.up.railway.app`

### Option 3: PythonAnywhere (Free for Beginners)

1. **Sign up at https://www.pythonanywhere.com**

2. **Upload Files:**
   - Use Files tab to upload your project
   - Or use Git: `git clone your-repo-url`

3. **Configure Web App:**
   - Go to Web tab
   - Create new web app
   - Select "Manual configuration" → Python 3.13
   - Set source code directory
   - Set WSGI file: `/home/username/coffee_site/coffee_site/wsgi.py`

4. **Static Files:**
   - Add static files mapping in Web tab
   - URL: `/static/` → Directory: `/home/username/coffee_site/staticfiles`

5. **Reload Web App**
   - Your site will be at: `https://username.pythonanywhere.com`

## Before Deploying - Important Steps

1. **Install Gunicorn locally (for testing):**
   ```bash
   .\.venv\Scripts\python -m pip install gunicorn
   ```

2. **Update requirements.txt:**
   ```bash
   .\.venv\Scripts\python -m pip freeze > requirements.txt
   ```

3. **Collect Static Files:**
   ```bash
   .\.venv\Scripts\python manage.py collectstatic --noinput
   ```

4. **Create Superuser (if deploying fresh):**
   ```bash
   .\.venv\Scripts\python manage.py createsuperuser
   ```

## Environment Variables for Production

Set these in your hosting platform:

- `SECRET_KEY`: Your Django secret key
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: Your domain (e.g., `your-app.onrender.com`)

## Custom Domain (Optional)

Most platforms allow you to add a custom domain:
- Render: Settings → Custom Domain
- Railway: Settings → Domains
- PythonAnywhere: Web → Static files & domains

## Need Help?

- Render Docs: https://render.com/docs
- Railway Docs: https://docs.railway.app
- PythonAnywhere Docs: https://help.pythonanywhere.com

Your website will be accessible from anywhere in the world once deployed! 🌍

