# 🥤 Drinker Web App

A Django-powered web application for user authentication, email delivery, and Google OAuth integration. Built with PostgreSQL and secured using environment variables via `python-decouple`.

---

## 🚀 Features

- Django 5.2.5 with PostgreSQL backend
- Google OAuth2 login via `social-auth-app-django`
- Gmail SMTP email delivery (password reset, notifications)
- Secure `.env` configuration using `python-decouple`
- Modular app structure with custom templates
- Ready for deployment on PythonAnywhere

---

## 🛠️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Sangamthapa2892/drinker.git
cd drinker
```
### 2. Create and activate a virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure environment variables
Copy the example file and fill in your secrets
```bash
cp .env.example .env
```
### 5. Apply migrations
```bash
python manage.py makemigrations
python manage.py migrate
```
### 6. Run the development server
```bash
python manage.py runserver
```
🔐 Environment Variable
Your .env file should include:
```
SECRET_KEY=your-secret-key
DEBUG=True

DB_NAME=your-db-name
DB_USER=your-db-user
DB_PASSWORD=your-db-password
DB_HOST=localhost
DB_PORT=5432

EMAIL_HOST_USER=your-email@example.com
EMAIL_HOST_PASSWORD=your-app-password

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY=your-google-client-id
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET=your-google-client-secret
SOCIAL_AUTH_GOOGLE_OAUTH2_REDIRECT_URI=http://127.0.0.1:8000/social-auth/complete/google-oauth2/
```

📧 Email Setup
- Uses Gmail SMTP (smtp.gmail.com)
- Requires an App Password
- Supports password reset and notifications

## 🌐 Live Demo

Check out the live version of the Drinker Web App:

🔗 [Drinker Web App on PythonAnywhere](https://drinkerwebapp.pythonanywhere.com)

> You can test Google OAuth login, email delivery, and explore the core features in action.


🌐 Deployment Notes
- Add your domain to ALLOWED_HOSTS in settings.py
- Use PostgreSQL for production
- Host on PythonAnywhere or similar platforms

📄 License
This project is licensed under the MIT License.

👤 Author<br>
Sangam Thapa<br>
Kathmandu, Nepal<br>
📧 sangamthapa2892@gmail.com

