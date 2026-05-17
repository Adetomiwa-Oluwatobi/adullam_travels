# Adullam Travels — Website

A premium travel agency website built with Django. Fully content-manageable via admin dashboard.

---

## Tech Stack
- Python 3 + Django 5
- SQLite (zero-config database)
- Vanilla JS + CSS (no frameworks needed)
- Font Awesome icons, Google Fonts

---

## Quick Start (Local)

```bash
# 1. Clone / unzip the project
cd adullam_travels

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install django pillow

# 4. Run migrations
python manage.py migrate

# 5. Load sample data (optional — only first time)
python manage.py loaddata initial_data.json   # if fixture exists

# 6. Create admin user (if not already created)
python manage.py createsuperuser

# 7. Start the server
python manage.py runserver

# Visit: http://127.0.0.1:8000
# Admin: http://127.0.0.1:8000/admin
```

---

## Admin Dashboard

URL: `/admin`  
Default credentials: **admin / adullam2025!**

> ⚠️ Change the password immediately after first login.

### What you can manage:
| Section | What it controls |
|---|---|
| **Site Content** | Hero text, taglines, about page copy |
| **Destinations** | Add/edit/remove destinations with images |
| **Services** | Edit service titles, descriptions, icons |
| **Testimonials** | Add client reviews |
| **Quote Requests** | View all form submissions from visitors |

---

## Deploying to Render (Free Hosting)

1. Push the project to a GitHub repo
2. Go to [render.com](https://render.com) → New Web Service
3. Connect your GitHub repo
4. Set these:
   - **Build command:** `pip install django pillow && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start command:** `gunicorn adullam_travels.wsgi`
5. Add environment variable: `SECRET_KEY` → generate a random string
6. Change `DEBUG = False` in `settings.py` for production
7. Add your domain to `ALLOWED_HOSTS`

Install gunicorn first:
```bash
pip install gunicorn
pip freeze > requirements.txt
```

---

## Deploying to Railway

1. Install Railway CLI: `npm install -g @railway/cli`
2. `railway login` → `railway init` → `railway up`
3. Set environment variables in the Railway dashboard

---

## Changing Images

All destination images use Unsplash URLs. To change them:
1. Go to [unsplash.com](https://unsplash.com)
2. Find your image → right-click → Copy Image Address
3. Paste the URL in the Admin → Destinations → image URL field

---

## Brand Colours

| Role | Hex |
|---|---|
| Orange Accent | `#D98A2B` |
| Main Text | `#1A1A1A` |
| Background | `#F7F7F5` |
| Light UI | `#EFEFEF` |
| Secondary Text | `#7A7A7A` |

---

## Instagram Integration

The contact form automatically pre-fills an Instagram DM with the user's travel details and redirects them to:
`https://www.instagram.com/adullamtravels`

To update the Instagram handle, search for `adullamtravels` in:
- `templates/core/base.html`
- `templates/core/contact.html`
- `templates/core/destinations.html`
- `core/views.py`

---

## Support

Website built by a freelance developer. For modifications or hosting support, reach out via the same channel this was delivered through.
