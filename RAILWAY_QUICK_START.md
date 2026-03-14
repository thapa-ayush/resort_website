# 🚀 Quick Railway Deployment Checklist

**Complete in 5-10 minutes. No coding needed!**

---

## ✅ Pre-Deployment Checklist

- [ ] **GitHub Account**: Have GitHub account ready
- [ ] **Railway Account**: Sign up at [railway.app](https://railway.app)
- [ ] **Code Pushed**: Push your code to GitHub repo
- [ ] **Procfile**: Verify exists in root directory ✓
- [ ] **requirements.txt**: Includes `dj-database-url` ✓
- [ ] **.env.example**: Updated with variables ✓

---

## 🎯 5-Step Deployment Process

### Step 1: Push to GitHub 📤
```bash
cd /path/to/resort_website
git init
git add .
git commit -m "Railway deployment ready"
git remote add origin https://github.com/YOUR_USERNAME/resort_website.git
git branch -M main
git push -u origin main
```
**Time: 1-2 minutes**

---

### Step 2: Create Railway Project 🔧
1. Go to [railway.app](https://railway.app)
2. Click **"New Project"**
3. Select **"Import from GitHub"**
4. Authorize Railway
5. Select `resort_website` repo
6. Click **"Import"**
7. Wait for build to complete (~1-2 minutes)

✅ Success: Railway auto-detects `Procfile`

**Time: 2-3 minutes**

---

### Step 3: Add PostgreSQL Database 🗄️
1. In Railway dashboard, click **"+ New"**
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
