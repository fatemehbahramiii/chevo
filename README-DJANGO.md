# CHEVO Django backend (initial scaffold)

This backend is added on branch `feature/django-backend`; the existing static HTML website is preserved.

## Local setup (Windows)
1. Install Python 3.11+.
2. In the repository folder run:
   ```powershell
   py -m venv .venv
   .\.venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   Copy-Item .env.example .env
   py manage.py migrate
   py manage.py createsuperuser
   py manage.py runserver
   ```
3. Open `http://127.0.0.1:8000/admin/`, create package records, and visit `/payments/packages/`.

## Included
- Django configuration, SQLite for local development and optional DATABASE_URL for deployment.
- Built-in Django authentication with registration, login, logout and protected dashboard.
- Contact form stores submissions in the database and attempts email delivery.
- Admin pages for contact messages, packages and payments.
- Package and payment records plus an intentionally incomplete provider adapter.

## Important before production
- This is an initial scaffold, not a production-ready payment integration.
- The exact BitPay API URL, request schema, redirect URL and server-to-server verification depend on the specific Iranian BitPay merchant API documentation. Configure those from the official merchant documentation. A browser callback alone never marks a payment paid.
- Configure real SMTP settings, a strong DJANGO_SECRET_KEY, production ALLOWED_HOSTS, CSRF_TRUSTED_ORIGINS, HTTPS and a production database.
- The current `index.html` still submits to the old `forms/contact.php`; to use Django contact handling, update its form action to `/contact/` and keep `method="post"`. Include Django's CSRF token in a Django-rendered template. The existing static HTML is not yet converted into a Django template.
- Run `python manage.py check` and `python manage.py test` before deployment.
