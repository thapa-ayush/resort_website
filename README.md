# Diamond Hill Resort - Django Web Application

A professional, production-ready Django web application for **Diamond Hill Resort** in Nagarkot, Nepal. Deploy to **Railway, Heroku, or any Python hosting** in minutes.

**Tagline:** *"Own the Drip"* - Experience luxury, style, and comfort in the heart of Nepal's mountains.

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- pip (Python package manager)
- Git

### Local Setup (5 minutes)

```bash
# Clone and navigate
git clone <repository-url>
cd resort_website

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env

# Run migrations
python manage.py migrate

# Create superuser (admin)
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

**Visit:** `http://127.0.0.1:8000/` (site) | `http://127.0.0.1:8000/admin/` (admin)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Responsive Design** | Bootstrap 5 mobile-first responsive layout |
| **Room Management** | Add/edit rooms with images, amenities, multi-currency pricing |
| **Booking System** | Guest booking form with date validation and total calculation |
| **Admin Dashboard** | Professional Django admin with custom dashboard showing stats |
| **Content Management** | Database-driven content (hero slides, blog posts, about page) |
| **Gallery** | Photo gallery with captions for resort showcase |
| **Blog System** | Rich text editor (TinyMCE) for blog posts with publishing control |
| **Multi-Currency** | Automatic pricing in NPR, USD, EUR with exchange rate support |
| **Payment Ready** | Placeholder integrations for Stripe, eSewa, Khalti |
| **SEO Optimized** | Meta tags, slugs, semantic HTML, XML sitemap ready |
| **Email Notifications** | Automatic booking confirmation emails (configurable) |
| **Production Ready** | Security headers, HTTPS support, PostgreSQL ready |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|------------|
| **Backend** | Django 4.2.7 |
| **Database** | SQLite (dev), PostgreSQL (production) |
| **Frontend** | Bootstrap 5, HTML5, CSS3, JavaScript |
| **Images** | Pillow (image processing) |
| **Rich Text** | TinyMCE (blog editor) |
| **Server** | Gunicorn (WSGI), WhiteNoise (static files) |
| **Config** | python-decouple (environment variables) |
| **ORM** | Django ORM with migrations |

---

## 📁 Project Structure

```
resort_website/
├── manage.py                      Django CLI
├── Procfile                       Railway deployment config
├── requirements.txt               Python dependencies
├── .env.example                   Environment template
├── README.md                      This file
│
├── scripts/                       Utility scripts
│   ├── populate_sample_data.py   Load demo data
│   ├── check_db.py               Database inspection
│   └── verify_website.py         Feature verification
│
├── resort_website/                Django project settings
│   ├── settings.py               Configuration (env-aware)
│   ├── urls.py                   URL routing
│   ├── wsgi.py                   Production server config
│   └── asgi.py                   Async config
│
├── main/                          Django application
│   ├── models.py                 Database schema (12 migrations)
│   ├── views.py                  Business logic
│   ├── admin.py                  Admin customization
│   ├── forms.py                  Form validation
│   ├── urls.py                   App routing
│   │
│   ├── migrations/               Database migrations (0001-0012)
│   │
│   ├── templates/main/           HTML templates
│   │   ├── base.html            Base layout + navbar
│   │   ├── home.html            Homepage
│   │   ├── rooms.html           Room listing page
│   │   ├── room_detail.html     Individual room details
│   │   ├── booking.html         Booking form
│   │   ├── gallery.html         Photo gallery
│   │   ├── blog.html            Blog listing
│   │   ├── about.html           About page
│   │   ├── contact.html         Contact form
│   │   └── ...
│   │
│   ├── static/                  CSS, JS, images
│   │   ├── css/style.css        Main stylesheet
│   │   ├── js/main.js           Interactivity
│   │   └── images/              Static images
│   │
│   └── management/              Custom commands
│       └── commands/            Management scripts
│
├── media/                       User uploads
│   ├── rooms/                   Room images
│   ├── about/                   About section images
│   └── gallery/                 Gallery images
│
└── docs/                        Documentation
    └── DEPLOYMENT_RAILWAY.md    Railway deployment guide
```

---

## 📊 Database Models

| Model | Purpose | Key Fields |
|-------|---------|-----------|
| **Room** | Accommodation types | title, slug, description, price (NPR/USD/EUR), amenities, image, capacity, size |
| **HeroSection** | Homepage slides | title, subtitle, image, order, is_active |
| **BlogPost** | Articles | title, content (TinyMCE), author, is_published, image, meta_tags |
| **About** | About page info | title, story, image, values_intro |
| **Review** | Guest testimonials | name, rating (1-5), location, text, visited_date, is_published |
| **Booking** | Guest bookings | room, guest_info, dates, total, payment_status |
| **GalleryImage** | Photo gallery | caption, image, upload_date |
| **RoomImage** | Room images | room_fk, image |
| **RoomInventory** | Availability | room_fk, booked_dates |

---

## 🎨 Admin Features

Access `/admin/` with superuser credentials.

### Room Management
- ✅ Add/edit/delete room types
- ✅ Multi-currency pricing (NPR/USD/EUR auto-convert)
- ✅ Image upload with thumbnail preview
- ✅ Amenities management
- ✅ Capacity and size tracking

### Content Management
- ✅ **Hero Slides**: Manage homepage slides with auto-cycling (6s)
- ✅ **Blog Posts**: Rich text editor (TinyMCE), draft/publish control
- ✅ **About Page**: Edit story, values, and featured image
- ✅ **Gallery**: Upload and caption photos

### Booking & Reviews
- ✅ View all bookings with guest details
- ✅ Filter by room, date, payment status
- ✅ Publish/unpublish customer reviews
- ✅ Track ratings and testimonials

### Dashboard
- Real-time stats: Total rooms (4), Hero slides (2), Blog posts, Reviews
- Quick-access admin links
- Room availability overview

---

## 🔧 Installation Detailed

### Step 1: Clone Repository
```bash
git clone <repository-url>
cd resort_website
```

### Step 2: Setup Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings (or leave defaults for local dev)
```

### Step 5: Database Setup
```bash
python manage.py migrate
python manage.py createsuperuser
```

### Step 6: Load Demo Data (Optional)
```bash
python scripts/populate_sample_data.py
```

### Step 7: Run Server
```bash
python manage.py runserver
```

Visit: `http://127.0.0.1:8000/`

---

## 📍 Available URLs

| URL | Purpose | Authenticated |
|-----|---------|---|
| `/` | Homepage | ✗ |
| `/rooms/` | Room listing | ✗ |
| `/rooms/<slug>/` | Room detail | ✗ |
| `/booking/` | Booking form | ✗ |
| `/booking/success/` | Confirmation | ✗ |
| `/gallery/` | Photo gallery | ✗ |
| `/blog/` | Blog listing | ✗ |
| `/blog/<slug>/` | Blog post | ✗ |
| `/about/` | About page | ✗ |
| `/contact/` | Contact form | ✗ |
| `/admin/` | Admin panel | ✓ |

---

## 🚢 Deployment

### Option 1: Railway (Recommended) ⭐
**Fastest:** Free demo ($5 credits), scales to production, PostgreSQL included.

**Steps:**
1. Push code to GitHub
2. Sign up at [Railway.app](https://railway.app)
3. Create new project → GitHub integration
4. Add PostgreSQL plugin
5. Deploy (2 minutes)

👉 **Detailed guide:** See [docs/DEPLOYMENT_RAILWAY.md](docs/DEPLOYMENT_RAILWAY.md)

For production with Railway:
- Free demo tier ($5 credits)
- Production tier: $10-20/month (includes PostgreSQL)
- Custom domain: $1/month (optional)
- Automatic SSL/HTTPS

### Option 2: Heroku
1. Create Procfile ✓ (already included)
2. Install Heroku CLI
3. `heroku login` → `heroku create` → `heroku config:set`
4. `git push heroku main`

### Option 3: PythonAnywhere
1. Fork repo to GitHub
2. Dashboard → Add new web app
3. Configure Python 3.10, requirements.txt
4. Set `WSGI configuration file`
5. Reload

### Option 4: DigitalOcean App Platform
1. Connect GitHub repo
2. Settings: Python runtime, `gunicorn resort_website.wsgi`
3. Add PostgreSQL database
4. Deploy

---

## 🔐 Security Checklist

Before production deployment:

- [x] CSRF protection enabled
- [x] SQL injection prevention (Django ORM)
- [x] XSS protection (template escaping)
- [x] Secure password hashing (Django auth)
- [x] HTTPS ready (`SECURE_SSL_REDIRECT`)
- [x] Secure cookies (`SESSION_COOKIE_SECURE`)
- [x] Content Security Policy headers
- [x] Clickjacking protection (`X_FRAME_OPTIONS`)

**Production checklist:**
```python
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')  # Strong random value
ALLOWED_HOSTS = ['.yourdomain.com']
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

## 📧 Email Configuration (Optional)

For booking confirmations, enable SMTP in `.env`:

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

**Gmail setup:**
1. Enable 2FA
2. Generate [App Password](https://myaccount.google.com/apppasswords)
3. Use app password in `EMAIL_HOST_PASSWORD`

---

## 💳 Payment Integration

Placeholder endpoints ready for integration:

```python
# Stripe: /payment/callback/stripe/
# Khalti: /payment/callback/khalti/
# eSewa: /payment/callback/esewa/
```

### Test Cards:
- **Stripe:** `4242 4242 4242 4242` (any future date, any CVC)
- **Khalti:** Use test account at [test.khalti.com](https://test.khalti.com)
- **eSewa:** Sandbox environment

---

## 🧪 Testing

Run all tests:
```bash
python manage.py test
```

Run specific app tests:
```bash
python manage.py test main
```

With verbosity:
```bash
python manage.py test --verbosity=2
```

---

## 🔄 Updating Content

### Add a Room
1. Go to `/admin/main/room/`
2. Click "Add Room"
3. Fill title, description, price, amenities, upload image
4. Save

### Publish Blog Post
1. Go to `/admin/main/blogpost/`
2. Create/edit post (TinyMCE editor)
3. Check "Is Published"
4. Save

### Edit Homepage
1. **Hero slides:** `/admin/main/herosection/`
2. **About section:** `/admin/main/about/` (upload image)
3. **Reviews:** `/admin/main/review/` (check "Is Published")

---

## 📝 Configuration

All settings use environment variables. No hardcoding!

Key variables:
- `DEBUG` - Development mode (True/False)
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Allowed domain names
- `DATABASE_URL` - PostgreSQL connection (Railway sets this)
- `SECURE_SSL_REDIRECT` - Force HTTPS

See `.env.example` for all variables.

---

## 🐛 Troubleshooting

### Static files not loading in production
```bash
python manage.py collectstatic --noinput
```
Check: WhiteNoise middleware is added to `MIDDLEWARE` in settings.py

### Database errors on Railway
- Check PostgreSQL is added as plugin
- Verify `DATABASE_URL` is set in environment variables
- Run: `python manage.py migrate` in Railway shell

### Media files not showing
- Ensure `MEDIA_URL` and `MEDIA_ROOT` are configured in settings.py
- In production, serve media via cloud storage (S3, etc.)

### Admin CSS broken
```bash
python manage.py collectstatic --noinput
```

---

## 📚 Documentation

- **Deployment:** [docs/DEPLOYMENT_RAILWAY.md](docs/DEPLOYMENT_RAILWAY.md)
- **Models:** See `main/models.py` for database schema
- **Admin Customization:** See `main/admin.py` for admin configuration
- **Templates:** See `main/templates/main/` for HTML templates

---

## 🌐 Browser Support

| Browser | Support | Version |
|---------|---------|---------|
| Chrome | ✅ | Latest |
| Firefox | ✅ | Latest |
| Safari | ✅ | Latest |
| Edge | ✅ | Latest |
| Mobile Safari | ✅ | iOS 12+ |
| Chrome Android | ✅ | Latest |

---

## 📞 Contact & Support

**Diamond Hill Resort**
- 📍 Cherry Hill Road, Nagarkot, Kavrepalanchok, Nepal
- 📞 +977-1-1234567
- 📧 info@diamondhillresort.com.np
- 🌐 [Facebook](https://www.facebook.com/diamondhillresort.com.np/)

---

## 📄 License

This project is proprietary software for Diamond Hill Resort. All rights reserved.

---

## 🎉 Version History

| Version | Date | Notes |
|---------|------|-------|
| **1.0.0** | 2026-03-14 | Initial release with full features |
| | | Room management, booking system, admin dashboard |
| | | Multi-currency pricing, SEO optimization |
| | | Railway deployment ready |

---

**Built with ❤️ for Diamond Hill Resort**

*"Own the Drip" - Where luxury meets Nepal's natural beauty* 🏔️
