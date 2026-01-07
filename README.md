Dayflow HRM – Localhost Setup (Virtual Environment)

Dayflow HRM is a web-based Human Resource Management System.This guide explains how to run the project on localhost using a Python Virtual Environment (venv).

🚀 Tech Stack

Backend: Python (Django / Flask)

Frontend: HTML / CSS / JS or React (optional)

Database: SQLite (default) or PostgreSQL

Environment: Python Virtual Environment (venv)

📦 Prerequisites

Make sure you have the following installed:

Python 3.10+

Git

pip (comes with Python)

Check versions:

python --version
pip --version

📁 Project Structure

dayflow-hrm/
├── backend/
│   ├── manage.py
│   ├── requirements.txt
│   └── dayflow/
├── venv/
└── README.md

🧪 Step 1: Clone the Repository

git clone https://github.com/your-username/dayflow-hrm.git
cd dayflow-hrm

🐍 Step 2: Create Virtual Environment

Windows

python -m venv venv
venv\Scripts\activate

macOS / Linux

python3 -m venv venv
source venv/bin/activate

You should see (venv) in your terminal.

📥 Step 3: Install Dependencies

cd backend
pip install -r requirements.txt

⚙️ Step 4: Environment Variables (Optional)

Create a .env file inside backend/:

DEBUG=True
SECRET_KEY=dev_secret_key
DATABASE_NAME=db.sqlite3

🗄️ Step 5: Database Setup

Run migrations

python manage.py migrate

Create admin user

python manage.py createsuperuser

▶️ Step 6: Run the Server

python manage.py runserver

🌐 Access the Application

Web App: http://127.0.0.1:8000/

Admin Panel: http://127.0.0.1:8000/admin

🛑 Stop the Server

Press:

CTRL + C

Deactivate virtual environment:

deactivate

🧹 Common Issues

venv not activating → Check Python installation path

Module not found → Reinstall requirements

Port already in use → Run:

python manage.py runserver 8080

🔒 Security Notes

Do NOT commit venv/

Keep SECRET_KEY private

This setup is for development only

📄 License

Educational / Internal use only.
