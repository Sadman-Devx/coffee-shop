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

2. **Set environment variables (recommended):**
   - Copy `env.example` to `.env` in the project root (same folder as `manage.py`)
   - Update at least `DJANGO_SECRET_KEY`

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

This is a standard Django project. To deploy it publicly you need a server that can run Python (Django + a WSGI server like Gunicorn) and a database.

The included `start.sh` script is intended for traditional server deployments and typically:
- Runs database migrations
- Sets up initial data (if applicable)
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
