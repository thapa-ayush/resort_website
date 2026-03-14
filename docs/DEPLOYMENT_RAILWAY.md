# Railway Deployment Guide for Diamond Hill Resort

Deploy **Diamond Hill Resort** to Railway in **5-10 minutes**. Railway handles everything: GitHub integration, PostgreSQL database, SSL, and auto-deploys on git push.

---

## 📋 Prerequisites

- [x] GitHub account 
- [x] Railway.app account ([Sign up free](https://railway.app))
- [x] Project pushed to GitHub repository
- [x] `Procfile` (included ✓)
- [x] `requirements.txt` with `dj-database-url` (included ✓)
- [x] `settings.py` configured for environment variables (included ✓)

---

## 🚀 Step 1: Push Code to GitHub

If not already on GitHub:

```bash
git init
git add .
git commit -m "Initial commit: Diamond Hill Resort Django app"
git remote add origin https://github.com/YOUR_USERNAME/resort_website.git
git branch -M main
git push -u origin main
```

---

## 🔧 Step 2: Create Railway Project

1. **Sign in** to [railway.app](https://railway.app)
2. **Click** "New Project"
3. **Select** "Import from GitHub"
4. **Authorize** Railway to access your GitHub
5. **Select** `resort_website` repository
6. **Click** "Import"

✅ Railway will auto-detect `Procfile` and create app

---

## 🗄️ Step 3: Add PostgreSQL Database

1. In Railway dashboard, click **"+ New"** (add service)
2. **Select** "Database"
3. **Choose** "PostgreSQL"
4. **Wait** ~30 seconds for creation

✨ Railway **automatically sets** `DATABASE_URL` environment variable

---

## 🔐 Step 4: Configure Environment Variables

In Railway dashboard:

1. **Click** your project
2. **Click** the Django app service
3. **Go to** "Variables" tab
4. **Add** these variables:

| Variable | Value | Notes |
|----------|-------|-------|
| `DEBUG` | `False` | Disables debug mode for production |
| `SECRET_KEY` | `your-random-secret-key-here` | Use strong random string, e.g., `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'` |
| `ALLOWED_HOSTS` | `yourdomain.railway.app` | Railway's default domain, or your custom domain |
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS |
| `SESSION_COOKIE_SECURE` | `True` | Secure cookies over HTTPS |
| `CSRF_COOKIE_SECURE` | `True` | CSRF cookies over HTTPS |

### Generate Random Secret Key
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🛟 Step 5: Deploy!

### Option A: Auto-Deploy (Recommended)
- **Push** code to GitHub
- Railway **automatically** deploys
- No manual steps needed!

### Option B: Manual Deploy
1. In Railway dashboard, click your service
2. Click **"Deploy"** button
3. Watch logs in real-time

---

## ✅ Step 6: Verify Deployment

1. **Get URL**: Dashboard shows `your-app.railway.app`
2. **Visit homepage**: `https://your-app.railway.app/`
3. **Check admin**: `https://your-app.railway.app/admin/`
4. **Create superuser**:
   - Click your app → "Shell" tab
   - Run: `python manage.py createsuperuser`
   - Enter username, email, password

---

## 🌐 Step 7: Custom Domain (Optional)

To use custom domain like `diamondhillresort.com`:

1. In Railway dashboard, click your app
2. Go to **Settings → Domains**
3. **Click** "Add Domain"
4. **Enter** `diamondhillresort.com` (or subdomain)
5. **Get** DNS records from Railway
6. **Update** your domain registrar's DNS settings
7. **Wait** 5-10 minutes for DNS to propagate

---

## 📊 Deployment Checklist

- [x] Code pushed to GitHub
- [x] Railway project created
- [x] PostgreSQL database added
- [x] Environment variables set
- [x] `Procfile` present
- [x] `requirements.txt` includes `dj-database-url`
- [x] `settings.py` handles `DATABASE_URL`
- [x] Project deployed
- [x] Site accessible at railway.app
- [x] Admin panel set up with superuser
- [ ] Custom domain configured (optional)
- [ ] SSL certificate verified (auto-done by Railway)

---

## 🔍 Monitoring & Troubleshooting

### View Logs
1. Dashboard → Your service
2. Click **"Logs"** tab
3. Real-time deployment and runtime logs

### Common Issues

#### App won't start
**Problem:** Deployment fails or crashes
**Solution:**
1. Check logs for errors
2. Run locally: `python manage.py runserver`
3. Verify all dependencies in `requirements.txt`
4. Check `Procfile` syntax

#### Database connection error
**Problem:** `psycopg2` or database errors
**Solution:**
1. Verify PostgreSQL plugin added
2. Check `DATABASE_URL` is set in variables
3. Run in Railway shell: `python manage.py migrate`
4. Restart service

#### Static files not loading
**Problem:** CSS/JS broken or missing
**Solution:**
1. Verify `STATIC_ROOT` in `settings.py`
2. Verify `whitenoise` middleware added
3. Run: `python manage.py collectstatic --noinput`
4. Redeploy

#### 404 Page Not Found
**Problem:** Site returns 404 for all pages
**Solution:**
1. Check `ALLOWED_HOSTS` includes your domain
2. Verify `DEBUG=False` in production
3. Check app is listening on `0.0.0.0:$PORT`

### SSH into Railway
To run Django commands on production:
1. Dashboard → Your service
2. Click **"Shell"** tab
3. Run:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py collectstatic --noinput
   ```

---

## 📈 Scaling & Optimization

### Performance Monitoring
1. Dashboard → Your service → **"Metrics"**
2. Monitor: CPU, Memory, Requests/sec
3. Check response times

### Scale Up Resources
If site gets slow:
1. Dashboard → Your service → **"Settings"**
2. **Increase** RAM/CPU allocation
3. Pricing: On-demand (pay-as-you-go)

### Database Performance
Check database instance:
1. Dashboard → PostgreSQL service
2. Monitor: Connections, Query time
3. Consider: Backups, replication

---

## 💰 Pricing on Railway

| Item | Cost | Notes |
|------|------|-------|
| **Initial** | $5 free | Project credit |
| **App (vCPU)** | $0.065/hour | ~$50/month if always on |
| **App (RAM)** | $0.032/GB/hour | 512MB default |
| **Database (PostgreSQL)** | $5/month | Included with $5+ app spend |
| **Custom domain** | $1/month | Optional |
| **SSL/HTTPS** | Free | Automatic |

**Example monthly cost:**
- App: $50 (1 vCPU, 2GB RAM)
- Database: Included
- **Total: ~$50/month for production**

---

## 🔄 Continuous Deployment

Railway supports **auto-deploy on push**:

1. **Make** changes locally
2. **Commit** and **push** to GitHub
3. Railway **automatically** detects changes
4. Railway **rebuilds** and **deploys**
5. ~2-3 minutes later, site is updated

No manual deployment needed after setup!

**To disable auto-deploy:**
1. Dashboard → Service → Settings
2. Uncheck "Automatic Deploys"

---

## 🆙 Updating Django / Dependencies

1. Update `requirements.txt` locally
2. Test locally: `pip install -r requirements.txt`
3. Commit: `git add . && git commit -m "Update dependencies"`
4. Push: `git push`
5. Railway **auto-redeploys** with new packages

---

## 🗂️ Database Backups

Railway provides automated backups for PostgreSQL:

1. Dashboard → PostgreSQL service
2. Click **"Backups"** tab
3. Auto backups created daily
4. Manual backups available

---

## 🚨 Emergency: Rollback Deployment

If deployment breaks:

1. Git: `git log` → find good commit
2. Git: `git revert <commit-hash>` or `git reset --hard <commit-hash>`
3. Git: `git push`
4. Railway: Auto-detects and redeploys

---

## ✨ Next Steps

After deployment:

- [ ] Test all pages: `/`, `/rooms/`, `/booking/`, `/admin/`
- [ ] Create admin content: Rooms, hero slides, blog posts
- [ ] Enable email notifications (optional)
- [ ] Integrate payment gateways (optional)
- [ ] Set up monitoring & alerts (optional)
- [ ] Add custom domain (optional)
- [ ] Configure backup schedules (optional)

---

## 📞 Support & Resources

- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Django Docs:** [docs.djangoproject.com](https://docs.djangoproject.com)
- **Railway Community:** [Discord](https://discord.gg/railway)
- **Project README:** See [README.md](../README.md)

---

## 🎉 Congratulations!

Your Diamond Hill Resort website is now **live on Railway**! 🚀

**Your site URL:** `https://your-app.railway.app/`  
**Admin URL:** `https://your-app.railway.app/admin/`

Enjoy! 🏔️ *"Own the Drip"*
