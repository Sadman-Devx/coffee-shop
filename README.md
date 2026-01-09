# ☕ Brew Bloom Coffee Shop

A modern, responsive coffee shop website built with Django 5.2.

## Features

- 🛒 Shopping cart functionality
- 📦 Order placement and tracking
- ⏱️ Estimated order ready time
- 📬 Order completion notifications
- 👤 Admin panel for order management
- 📱 Fully responsive design

## Tech Stack

- Django 5.2
- SQLite Database
- WhiteNoise (Static files)
- Gunicorn (WSGI server)

## Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

3. **Create admin user and populate coffee items:**
   ```bash
   python manage.py setup_site
   ```

4. **Run development server:**
   ```bash
   python manage.py runserver
   ```

5. **Access the site:**
   - Website: http://127.0.0.1:8000/
   - Admin: http://127.0.0.1:8000/admin/
     - Username: `admin`
     - Password: `admin123`

## Deployment

This project was originally configured for Railway deployment but is now set up for Netlify static deployment.

### Netlify (static front-end) Deployment

> Note: Netlify is ideal for static sites and front-ends. Django is a full backend framework, so only the static assets (CSS, images, etc.) will be hosted on Netlify with this setup. For a fully functional site (checkout, auth, admin, etc.), you still need a Python backend host (e.g. Render, Railway, Fly.io, etc.) and point your front-end to it.

1. Push code to GitHub (or another Git provider supported by Netlify)
2. In the Netlify dashboard, create a new site from Git
3. When asked for build settings, use:
   - **Build command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Publish directory**: `staticfiles`
4. Configure environment variables in Netlify:
   - `DJANGO_SECRET_KEY` (a long random string)
   - `DJANGO_DEBUG` = `False`
   - `DJANGO_ALLOWED_HOSTS` (e.g. your Netlify domain)
   - Any other settings your `coffee_site/settings.py` expects
5. Deploy the site in Netlify

The `start.sh` script is used for traditional server deployments (e.g. Railway/Render) and is not used directly by Netlify.

## Project Structure

```
coffee-shop/
├── coffee_site/          # Django project settings
├── menu/                 # Main app
│   ├── models.py        # Coffee, Order, OrderItem models
│   ├── views.py         # Views for cart, checkout, tracking
│   ├── urls.py          # URL routing
│   └── admin.py         # Admin configuration
├── templates/           # HTML templates
├── static/              # CSS and static files
├── requirements.txt     # Python dependencies
├── Procfile            # Process file for traditional hosts (optional)
└── start.sh            # Startup script for traditional hosts
```

## Admin Panel

Access the admin panel to:
- Manage coffee menu items
- View and update customer orders
- Change order status
- Send completion messages to customers

## License

This project is for educational purposes.
