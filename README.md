> WEBSITE LIVE LINK : https://cepv-visualizer.onrender.com/

> DESKTOP APP EXE FILE SHARE ON DRIVE : https://drive.google.com/file/d/1603yFZSnbDfFOPfP0M2fZQkt469dVgdG/view?usp=sharing 

(DESKTOP APP READY IS TO RUN)

> BACKEND IS DEPLOYED ON RENDER (COLD START) : https://cepv-chemical-equipment-parameter.onrender.com 
PLEASE WAIT IF LOADING...............

> DEMO VIDEOS SHARED ON DRIVE : https://drive.google.com/drive/folders/1P-1cWwsF_UEeQFpAcyK7nK2NngdPItKP?usp=sharing




# CEPV – Chemical Equipment Parameter Visualizer

CEPV is a **full-stack data analytics platform** for chemical equipment datasets.  
It allows users to upload CSV files, analyze parameters, visualize trends, and generate PDF reports.

The project is built as **three connected applications**:

- 🌐 **Web App** – React + Tailwind (User interface)
- ⚙️ **Backend API** – Django + DRF (Data processing & storage)
- 🖥️ **Desktop App** – PyQt5 (Offline / native desktop client)

---

## 🚀 Features

### Core
- CSV upload with **strict format validation**
- Dataset naming & history tracking
- Summary statistics (avg flowrate, pressure, temperature)
- Interactive analytics charts
- CSV preview (first 10 rows)
- Auto-generated **PDF reports**
- Authentication (Login / Signup)

### Web
- Responsive dashboard
- Professional UI (Tailwind CSS)
- Dataset history & re-analysis
- Sample CSV download

### Desktop
- Native PyQt5 UI
- Same features as web dashboard
- Scrollable analytics & previews
- PDF download
- Ready for `.exe` packaging

---

## 📁 Repository Structure


---

# 🌐 FRONTEND (React)

## Tech Stack
- React (Vite)
- Tailwind CSS
- Axios
- React Router
- Chart.js

---

## 1️⃣ Frontend Setup

### Create project
```bash
npm create vite@latest cepv-frontend
cd cepv-frontend
npm install

Install dependencies
npm install axios react-router-dom chart.js react-chartjs-2
npm install -D tailwindcss postcss autoprefixer

Tailwind setup
npx tailwindcss init -p


Configure tailwind.config.js

content: ["./index.html", "./src/**/*.{js,jsx}"]

2️⃣ Environment Variables

Create .env

VITE_API_URL=http://127.0.0.1:8000

3️⃣ Run Frontend
npm run dev

⚙️ BACKEND (Django)
Tech Stack

Django

Django REST Framework

Token Authentication

Pandas

ReportLab (PDF)

SQLite (dev) / PostgreSQL (prod)

CORS Headers

1️⃣ Backend Setup
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers pandas reportlab python-dotenv
python -m venv venv

source venv/bin/activate   # Windows: venv\Scripts\activate
pip install django djangorestframework django-cors-headers pandas reportlab python-dotenv

2️⃣ Create Django Project
django-admin startproject cepv_backend
cd cepv_backend
python manage.py startapp equipment
python manage.py startapp reports

3️⃣ Environment Variables

Create .env inside backend root:

SECRET_KEY=your-secret-key
DEBUG=True
FRONTEND_URL=http://localhost:5173
DATABASE_URL=sqlite:///db.sqlite3

4️⃣ Settings Configuration
Installed Apps
INSTALLED_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework.authtoken",
    "equipment",
    "reports",
]

CORS
CORS_ALLOWED_ORIGINS = [FRONTEND_URL]
CORS_ALLOW_CREDENTIALS = True

Auth
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ]
}

5️⃣ Database
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser

6️⃣ Run Backend
python manage.py runserver

7️⃣ API Endpoints
| Method | Endpoint                     | Description     |
| ------ | ---------------------------- | --------------- |
| POST   | `/api/auth/signup/`          | Signup          |
| POST   | `/api/auth/login/`           | Login           |
| POST   | `/api/upload/`               | Upload CSV      |
| GET    | `/api/history/`              | Last 5 datasets |
| GET    | `/api/dataset/<id>/analyze/` | Analyze dataset |
| GET    | `/api/report/<id>/`          | Download PDF    |

🖥️ DESKTOP APP (PyQt5)
Tech Stack

PyQt5
Matplotlib
Requests
Same backend API

1️⃣ Desktop Setup
python -m venv venv
source venv/bin/activate
pip install PyQt5 requests matplotlib

2️⃣ Project Structure
desktop/
├── app/
│   ├── pages/        # login, signup, dashboard, history
│   ├── widgets/      # navbar, charts, tables
│   ├── services/     # api.py
│   ├── state.py      # global AppState
│   └── main.py

3️⃣ Run Desktop App
python app/main.py

4️⃣ Backend URL (Desktop)

Edit app/services/api.py:

BASE_URL = "http://127.0.0.1:8000/api"
For production, replace with deployed backend URL.

5️⃣ Package Desktop App (.exe)

Install PyInstaller:

pip install pyinstaller

Build:
pyinstaller --onefile --windowed app/main.py

Output:
dist/main.exe

🚀 DEPLOYMENT
Backend

Render
PostgreSQL recommended for production
Use gunicorn for production server

Frontend
Vercel
Update VITE_API_URL

Desktop

Share .exe via:
Google Drive
GitHub Releases

📄 CSV Format

Required columns (case-insensitive):

Equipment Name, Type, Flowrate, Pressure, Temperature

👩‍💻 Author

Manjiri Gawali
VIT Bhopal
Chemical Equipment Analytics Project

