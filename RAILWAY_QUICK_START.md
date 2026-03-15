# 🚀 Railway Deployment Guide - Complete & Working

**Status:** ✅ **Tested and Working** - Last verified: March 15, 2026

Deploy this Django application to Railway with PostgreSQL in **10-15 minutes**. No coding needed!

**Final Production URL:** https://resortwebsite-production.up.railway.app/

---

## ✅ Pre-Deployment Checklist

Before starting, ensure you have:

- [ ] **GitHub Account** - Code must be on GitHub
- [ ] **Railway Account** - Sign up at [railway.app](https://railway.app)
- [ ] **Code Pushed** - All changes committed and pushed to GitHub
- [ ] **Dockerfile** - Already included in repo ✓
- [ ] **entrypoint.sh** - Already included in repo ✓
- [ ] **requirements.txt** - All dependencies listed ✓

---

## 🎯 3-Step Deployment Process

### Step 1: Push Code to GitHub 📤

If not already done, push your code:

```bash
git add .
git commit -m "Production ready for Railway deployment"
git push origin main
```

**Repo:** https://github.com/thapa-ayush/resort_website

---

### Step 2: Create Railway Project 🔧

1. **Go to [railway.app](https://railway.app)**
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Authorize Railway to access your GitHub account
5. Select **`resort_website`** repository
6. Click **"Deploy Now"**
7. **Wait 3-5 minutes** for build to complete

Railway will automatically:
- ✅ Detect the Dockerfile
- ✅ Build Docker image with all dependencies
- ✅ Install system packages (libpq-dev, build-essential, etc.)
- ✅ Install Python packages (Django, Pillow, psycopg, gunicorn, etc.)
- ✅ Collect static files
- ✅ Start gunicorn on the assigned port

**Status Check:** Watch the "Build Logs" tab. You should see:
```
Running migrations...
Starting gunicorn on port 8000...
```

---

### Step 3: Add PostgreSQL Database 🗄️

1. In the Railway dashboard for your project, click **"+ Add"**
2. Select **"PostgreSQL"**
3. Click **"Create"**
4. Wait for database to initialize (~1 minute)

Railway automatically:
- ✅ Creates the database
- ✅ Sets `DATABASE_URL` environment variable
- ✅ Links it to your application

**Your app will automatically use PostgreSQL** - Django settings detect `DATABASE_URL` and configure itself.

### Step 4: Setup Persistent Volume for Media Files 📁

Uploaded images need persistent storage (Railway filesystem is ephemeral).

1. In Railway dashboard, **select "resort_website" service**
2. Go to **"Settings"** tab
3. Scroll to **"Volumes"** section
4. Click **"+ Create Volume"**
5. Set **Mount Path** to `/app/media`
6. Click **"Create"**
7. Redeploy (usually automatic)

Now uploaded images will persist across redeployments! ✅

---

## 🎉 Verification & Next Steps

### Verify Deployment is Live

1. **Check Status**: Railway dashboard should show a green deployment status
2. **Visit the Site**: Click the public URL or go to:
   ```
   https://resortwebsite-production.up.railway.app/
   ```
3. **Should see**: Resort website homepage loading

### Access Admin Panel

1. Visit: `https://resortwebsite-production.up.railway.app/admin/`

2. **Create Admin Account** (superuser):
   
   **Option A - Via Railway Web Terminal (Recommended):**
   - In Railway dashboard, select "resort_website" service
   - Look for "Terminal" button/tab
   - Run: `python manage.py createsuperuser`
   - Enter: username, email, password
   
   **Option B - Via Local CLI:**
   - Run locally: `python manage.py createsuperuser`
   - Commit and push to GitHub
   - Railway redeploys and user is synced to PostgreSQL

3. Login with your superuser credentials

4. **Test Image Upload:**
   - Go to admin → Rooms → Add/Edit Room
   - Upload an image
   - Check front-end - image should display
   - Image persists after redeployments (thanks to volume!) ✅

### Monitor Logs

In Railway dashboard:
1. Go to **"Deployments"** tab
2. Select latest deployment
3. View **"Build Logs"** and **"Deploy Logs"** to see startup output

---

## ⚠️ Important Configuration Notes

### Environment Variables

Railway automatically provides:
- `DATABASE_URL` - PostgreSQL connection string (automatically detected by Django)
- `PORT` - Server port (automatically used by entrypoint.sh)

Optional environment variables you can set in Railway dashboard:
- `DEBUG=False` - Keep disabled in production
- `SECRET_KEY` - Django secret key (uses safe default)

### Static Files

- Django collects static files **during Docker build** (not runtime)
- Served by WhiteNoise middleware
- Automatically cached and compressed

### Migrations

- Run automatically at **container startup** via `entrypoint.sh`
- Only applies new/unapplied migrations
- Doesn't block app startup

### Media Files (Image Uploads)

- **Configuration:** Django MEDIA_ROOT points to `/app/media` in production (persistent volume)
- **Development:** Images stored in local `/media/` folder
- **Persistence:** Images survive redeployments thanks to Railway volume ✅
- **Serving:** Configured in `urls.py` to serve media files in both dev and production
- **Setup:** Requires Step 4 (Create Persistent Volume) to work properly

### CSRF Protection

- ✅ **Configured for Railway:** Django trusts domains:
  - `resortwebsite-production.up.railway.app`
  - `*.railway.app` (wildcard)
  - `*.up.railway.app` (wildcard)
- **Cookies:** Set to insecure mode for Railway's reverse proxy compatibility
- **If you get 403 error:** Clear browser cookies and hard-refresh

---

## 🔧 Troubleshooting

### Admin Login Failed (403 CSRF Error)

**Cause:** CSRF (Cross-Site Request Forgery) protection blocking login
**Solution:**
1. Clear browser cookies: `Ctrl+Shift+Delete` (select "All time")
2. Hard refresh browser: `Ctrl+Shift+R`
3. Try logging in again
4. If still failing, check that domain is in `CSRF_TRUSTED_ORIGINS` in settings.py

### Uploaded Images Not Showing

**Cause:** Media files not stored persistently
**Solution:**
1. Create a persistent volume in Railway (Step 4 above)
2. Set mount path to `/app/media`
3. Redeploy application
4. Re-upload images through admin panel
5. Images should now persist after redeployments ✅

### 502 Bad Gateway Error

**Cause:** App not responding within timeout
**Solution:** 
1. Check Railway logs for errors
2. Ensure custom start command is **EMPTY** (remove any pre-deploy commands)
3. Redeploy with clean URL in browser

### Database Connection Failed

**Cause:** Database not initialized or not linked
**Solution:**
1. Ensure PostgreSQL service is added (Step 3)
2. Check that `DATABASE_URL` environment variable is set
3. Redeploy application

### Static Files Not Loading (404 errors)

**Solution:**
1. Verify WhiteNoise is installed: `pip list | grep whitenoise`
2. Check Django collects during build (should see "Collecting static files..." in build logs)
3. Visit `/admin/` - if CSS loads, static files are working

### Import Errors (Pillow, psycopg, etc.)

**Cause:** System dependencies not installed
**Solution:**
1. Dockerfile includes all required packages
2. If error persists, redeploy (fresh build)
3. Check build logs for package installation

---

## 🚀 Post-Deployment Tasks

### 1. Create Admin Account (if not already done)

```bash
# Local development
python manage.py createsuperuser

# OR via Django shell on Railway (advanced)
# Use Django admin panel to create superuser
```

### 2. Configure Site Settings

1. Go to `/admin/`
2. Add pages, blog posts, room listings, etc.
3. Upload images (Pillow support verified ✓)
4. Check frontend for proper display

### 3. Domain Setup (Optional)

1. In Railway settings, go to **"Domains"**
2. Add custom domain (requires DNS configuration)
3. SSL certificate automatically generated

---

## 📋 Architecture Overview

### Docker Build Process

```
Dockerfile
├─ Python 3.12 slim base image
├─ Install system dependencies (libpq-dev, build-essential, etc.)
├─ Install Python packages from requirements.txt
├─ Copy project files
├─ Make entrypoint.sh executable
├─ Collect static files (build time)
└─ Set up for container startup

Startup (entrypoint.sh)
├─ Run Django migrations
└─ Start gunicorn with 4 workers
```

### Technology Stack

- **Runtime:** Python 3.12
- **Framework:** Django 4.2.7
- **Database:** PostgreSQL (Railway managed)
- **Web Server:** Gunicorn 21.2.0
- **Static Files:** WhiteNoise 6.6.0
- **Images:** Pillow 11.1.0
- **Database Driver:** psycopg 3.1.18

---

## ✅ Deployment Checklist - Final Review

- [x] Code on GitHub
- [x] Dockerfile included
- [x] entrypoint.sh included  
- [x] requirements.txt updated with all packages
- [x] Django settings configured for production
- [x] Database migrations ready
- [x] Static files collection working
- [x] No custom start command in Railway settings
- [x] PostgreSQL database linked
- [x] App responding to HTTP requests

---

## 🎯 Summary

**You have successfully deployed a production-ready Django application to Railway!**

The application is now:
- ✅ Running on Railway's cloud infrastructure
- ✅ Connected to PostgreSQL database
- ✅ Serving static files (CSS, JavaScript, images)
- ✅ Handling image uploads with Pillow
- ✅ Running migrations automatically
- ✅ Accessible globally over HTTPS

**Estimated Deployment Time:** 10-15 minutes total
**Monthly Cost:** ~$7/month (2 services: app + database)

---

## 📞 Support & Resources

- **Railway Docs:** https://docs.railway.app/
- **Django Docs:** https://docs.djangoproject.com/
- **Issue:** Check Railway logs first, then review Django error messages

**Last Tested & Verified:** March 15, 2026
2. Select **"Database"**
3. Choose **"PostgreSQL"**
4. Wait ~30 seconds for creation

✨ Railway automatically sets `DATABASE_URL`

**Time: 1 minute**

---

### Step 4: Set Environment Variables 🔐
**In Railway Dashboard → Your App → Variables tab:**

Copy & paste these (one per line):

```
DEBUG=False
SECRET_KEY=<GENERATE_THIS>
ALLOWED_HOSTS=yourdomain.railway.app
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

**Generate random SECRET_KEY:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

Or just make one up: `django-insecure-a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0`

**Time: 2-3 minutes**

---

### Step 5: Deploy & Verify 🚀
1. In Railway dashboard, click **"Deploy"** (or auto-deploys on push)
2. Watch logs in real-time
3. Wait for deployment status: **"Success"** ✓
4. Your app URL appears: `https://your-app.railway.app/`

**Create Admin User:**
1. Click your app → **"Shell"** tab
2. Run command:
   ```bash
   python manage.py createsuperuser
   ```
3. Enter username, email, password
4. Done!

**Verify:**
- Visit: `https://your-app.railway.app/` (site)
- Visit: `https://your-app.railway.app/admin/` (admin panel)

**Time: 2-3 minutes**

---

## 🎊 You're Done!

Your Diamond Hill Resort website is **LIVE** on Railway! 🎉

| URL | Purpose |
|-----|---------|
| `https://your-app.railway.app/` | Public website |
| `https://your-app.railway.app/admin/` | Admin panel |
| `https://your-app.railway.app/rooms/` | Room listings |
| `https://your-app.railway.app/booking/` | Booking form |

---

## 🔧 Next Steps (Optional)

### Add Custom Domain (~2 minutes)
1. Dashboard → Your app → Settings
2. Click **"Domains"**
3. Add your domain
4. Update domain registrar's DNS records
5. Done!

### Monitor Your Site
1. Dashboard → Your app → "Metrics"
2. View: CPU, Memory, Requests, Response time

### Make Changes
1. Edit content in `/admin/`
2. OR: Edit code locally → `git push` → Railway auto-deploys

---

## 🆘 Troubleshooting

### Site shows 404
- Check `ALLOWED_HOSTS` includes your domain
- Restart app in Railway dashboard

### Admin CSS broken
- In Railway Shell: `python manage.py collectstatic --noinput`
- Restart app

### Can't create superuser
- In Railway Shell:
  ```bash
  python manage.py migrate
  python manage.py createsuperuser
  ```

### Database errors
- Verify PostgreSQL plugin added
- Check `DATABASE_URL` set in variables
- Restart app

**More help:** See `docs/DEPLOYMENT_RAILWAY.md`

---

## 📖 Documentation

- **Full Guide:** `docs/DEPLOYMENT_RAILWAY.md`
- **Project Info:** `README.md`
- **Config Example:** `.env.example`

---

## 💰 Pricing

- **First $5**: Free credit (arrives after 48 hours)
- **App**: $0.065/hour (~$48/month for 1 vCPU)
- **Database**: $5/month (PostgreSQL included)
- **Custom Domain**: $1/month (optional)
- **SSL/HTTPS**: Free (automatic)

**Example: Production setup ~$50-60/month**

---

## ✨ Key Features Ready on Railway

✅ **Auto-Deploy**: Push to GitHub → auto-deploy  
✅ **PostgreSQL**: Premium database included  
✅ **SSL/HTTPS**: Free, automatic  
✅ **Monitoring**: Real-time logs & metrics  
✅ **Scaling**: Increase resources on demand  
✅ **Backups**: Automatic daily backups  
✅ **Support**: Community & docs  

---

**Total Time: 5-10 minutes from here to live site** ⏱️

**Good luck! 🚀** *"Own the Drip"* 🏔️
