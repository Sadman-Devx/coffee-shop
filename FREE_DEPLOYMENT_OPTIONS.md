# 🆓 Free Deployment Options (Alternatives to Render)

Here are several **FREE** ways to deploy your coffee shop website:

---

## 🚂 Option 1: Railway (Easiest - Recommended)

### Why Railway?
- ✅ **100% Free** (with free credits monthly)
- ✅ **Auto-detects** Django/Python
- ✅ **Easiest setup** - almost automatic
- ✅ **No complex configuration needed**

### Steps:

1. **Go to Railway:**
   - Visit https://railway.app
   - Click **"Start a New Project"**
   - Sign up with **GitHub** (use same account)

2. **Deploy:**
   - Click **"New Project"**
   - Select **"Deploy from GitHub repo"**
   - Choose your `coffee-shop` repository
   - Railway **automatically detects** everything!

3. **That's it!** 
   - Railway will:
     - Install dependencies
     - Run migrations
     - Deploy your site
   - You'll get: `https://coffee-shop-production.up.railway.app`

4. **Add Environment Variables** (if needed):
   - Go to your project → **Variables** tab
   - Add:
     - `SECRET_KEY`: (generate one)
     - `DEBUG`: `False`
     - `ALLOWED_HOSTS`: `*.up.railway.app`

5. **Create Admin & Add Coffees:**
   - Click **"View Logs"** → **"Open Shell"**
   - Run:
     ```bash
     python manage.py createsuperuser
     python manage.py populate_coffees
     ```

**Your URL:** `https://coffee-shop-production.up.railway.app` ✅

---

## 🐍 Option 2: PythonAnywhere (Great for Beginners)

### Why PythonAnywhere?
- ✅ **Free tier** available
- ✅ **Simple web interface**
- ✅ **No command line needed** (mostly)
- ✅ **Good for learning**

### Steps:

1. **Sign Up:**
   - Go to https://www.pythonanywhere.com
   - Click **"Beginner"** (free account)
   - Sign up with email

2. **Upload Your Code:**
   - Go to **"Files"** tab
   - Click **"Upload a file"**
   - Or use **"Bash"** tab to clone from GitHub:
     ```bash
     git clone https://github.com/Sadman-Devx/coffee-shop.git
     ```

3. **Set Up Web App:**
   - Go to **"Web"** tab
   - Click **"Add a new web app"**
   - Choose **"Manual configuration"**
   - Select **Python 3.13** (or latest available)
   - Click **"Next"** → **"Finish"**

4. **Configure WSGI:**
   - In **"Web"** tab, click **"WSGI configuration file"**
   - Replace content with:
     ```python
     import os
     import sys
     
     path = '/home/YOUR_USERNAME/coffee-shop'
     if path not in sys.path:
         sys.path.append(path)
     
     os.environ['DJANGO_SETTINGS_MODULE'] = 'coffee_site.settings'
     
     from django.core.wsgi import get_wsgi_application
     application = get_wsgi_application()
     ```
   - Replace `YOUR_USERNAME` with your PythonAnywhere username

5. **Static Files:**
   - In **"Web"** tab, scroll to **"Static files"**
   - Add:
     - URL: `/static/`
     - Directory: `/home/YOUR_USERNAME/coffee-shop/staticfiles`

6. **Install Dependencies:**
   - Go to **"Bash"** tab
   - Run:
     ```bash
     cd coffee-shop
     pip3.13 install --user -r requirements.txt
     python3.13 manage.py migrate
     python3.13 manage.py collectstatic --noinput
     python3.13 manage.py createsuperuser
     python3.13 manage.py populate_coffees
     ```

7. **Reload Web App:**
   - Go to **"Web"** tab
   - Click **"Reload"** button

**Your URL:** `https://YOUR_USERNAME.pythonanywhere.com` ✅

---

## 🚀 Option 3: Fly.io (Free Tier)

### Why Fly.io?
- ✅ **Free tier** with generous limits
- ✅ **Fast deployment**
- ✅ **Global CDN**

### Steps:

1. **Install Fly CLI:**
   - Download from: https://fly.io/docs/getting-started/installing-flyctl/
   - Or use: `powershell -Command "iwr https://fly.io/install.ps1 -useb | iex"`

2. **Sign Up:**
   - Run: `fly auth signup`
   - Or visit: https://fly.io/app/sign-up

3. **Deploy:**
   - In your project folder:
     ```powershell
     fly launch
     ```
   - Follow prompts
   - It will auto-detect Django

4. **Your URL:** `https://coffee-shop.fly.dev` ✅

---

## 🌐 Option 4: Vercel (For Static/Django with Serverless)

### Note: Requires some configuration for Django

1. Go to https://vercel.com
2. Sign up with GitHub
3. Import your repository
4. Configure build settings

---

## 🎯 My Recommendation:

**Use Railway** - It's the easiest and most automatic!

### Quick Railway Setup:

1. Go to https://railway.app
2. Sign up with GitHub
3. New Project → Deploy from GitHub
4. Select `coffee-shop` repository
5. **Done!** Railway does everything automatically!

---

## 📊 Comparison:

| Platform | Difficulty | Free Tier | Auto-Setup |
|----------|-----------|-----------|------------|
| **Railway** | ⭐ Easy | ✅ Yes | ✅ Yes |
| **PythonAnywhere** | ⭐⭐ Medium | ✅ Yes | ❌ Manual |
| **Fly.io** | ⭐⭐ Medium | ✅ Yes | ⭐ Partial |
| **Render** | ⭐⭐ Medium | ✅ Yes | ⭐ Partial |

---

## 🚀 Quick Start with Railway (Recommended):

1. **Visit:** https://railway.app
2. **Sign up** with GitHub
3. **Click:** "New Project" → "Deploy from GitHub repo"
4. **Select:** `coffee-shop`
5. **Wait 2-3 minutes**
6. **Get your URL:** `https://coffee-shop-production.up.railway.app`

**That's it!** No complex setup needed! 🎉

---

Choose the one that sounds easiest to you! I recommend **Railway** for simplicity.

