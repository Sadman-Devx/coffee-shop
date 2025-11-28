# 🎯 Easy Setup - No Shell Needed!

I've created an **automatic setup** that runs when you deploy! 

## ✅ What I Just Did:

1. Created an automatic setup script
2. Updated your Procfile to run it automatically
3. Now you don't need to find the shell!

---

## 🚀 How It Works:

When you deploy, the script will **automatically**:
- ✅ Create admin user (username: `admin`, password: `admin123`)
- ✅ Add all 6 coffee items to your menu

**You don't need to do anything!** Just deploy and it works!

---

## 📝 After Deployment:

1. **Visit your site:** `https://your-url.com`
2. **Login to admin:** `https://your-url.com/admin/`
   - Username: `admin`
   - Password: `admin123`

**That's it!** Everything is set up automatically! 🎉

---

## 🔍 If You Still Want to Find the Shell:

### Railway:
1. Go to your project dashboard
2. Click your **service**
3. Look for **"Logs"** tab
4. Scroll to the **bottom** - there's a command box there
5. Or look for **"Shell"** or **"Console"** button

### Visual Guide:
```
Railway Dashboard
  └── Your Project
      └── Your Service
          ├── [Metrics]
          ├── [Logs] ← Check here! Scroll to bottom
          ├── [Settings]
          └── [Variables]
```

---

## 🎨 Alternative: Use the Setup Command

If you find the shell later, you can run:

```bash
python manage.py setup_site
```

This will set up everything in one command!

---

## 🔄 To Change Admin Password:

If you want to change the default password later:

1. Find the shell (using guide above)
2. Run: `python manage.py changepassword admin`
3. Enter new password

Or login to admin panel and change it there!

---

**Your site will be ready to use immediately after deployment!** ☕✨

