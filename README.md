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

This project is configured for Railway deployment.

### Railway Deployment

1. Push code to GitHub
2. Connect repository to Railway
3. Railway auto-detects and deploys
4. Your site will be live at: `https://your-app.up.railway.app`

The `start.sh` script automatically:
- Runs database migrations
- Sets up admin user and coffee items
- Collects static files
- Starts the server

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
├── Procfile            # Railway process file
├── railway.json        # Railway configuration
└── start.sh            # Startup script
```

## Admin Panel

Access the admin panel to:
- Manage coffee menu items
- View and update customer orders
- Change order status
- Send completion messages to customers

## License

This project is for educational purposes.
