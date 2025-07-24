---
title: ✅ README.md
created: '2025-07-24T19:46:45.160Z'
modified: '2025-07-24T19:47:10.373Z'
---

### ✅ `README.md`

```markdown
# BLOG_APP

A simple blog application built with Django, Bootstrap, and SQLite.

## 🚀 Features

- User registration & login
- Create, edit, and delete blog posts
- Responsive UI using Bootstrap
- Admin panel for managing content
- SQLite for development database

## 🛠️ Tech Stack

- **Backend:** Django (Python)
- **Frontend:** HTML, CSS, Bootstrap
- **Database:** SQLite (default), can be switched to PostgreSQL
- **Deployment:** Local or cloud-ready

## 📁 Project Structure

```

BLOG\_APP/
│
├── myapp/              # Core Django app
│   ├── migrations/
│   ├── templates/
│   ├── static/
│   └── views.py
│
├── manage.py
├── db.sqlite3
├── requirements.txt
└── .gitignore

````

## ⚙️ Setup Instructions

1. **Clone the repository**

```bash
git clone https://github.com/Santhosh23s/BLOG_APP.git
cd BLOG_APP
````

2. **Create and activate virtual environment**

```bash
python -m venv env
source env/Scripts/activate      # On Windows
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run migrations**

```bash
python manage.py migrate
```

5. **Start the development server**

```bash
python manage.py runserver
```

6. **Open in your browser**

```
http://127.0.0.1:8000/
```

## 🧪 Superuser (Admin Login)

Create a superuser for admin access:

```bash
python manage.py createsuperuser
```

---

## 🙈 .gitignore Example

Make sure your `.gitignore` excludes:

```
env/
__pycache__/
*.pyc
*.pyo
*.sqlite3
*.log
media/
```

---

## 📌 License

This project is for educational/demo purposes.

---

Let me know if you want to add badges, screenshots, or instructions for deploying to a platform like **Render**, **Vercel**, or **PythonAnywhere**.

