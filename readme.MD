# Campus Assignment Manager

Sistem manajemen tugas mahasiswa berbasis FastAPI, PostgreSQL, dan Streamlit.

## Tech Stack

### Backend

* FastAPI
* SQLAlchemy
* PostgreSQL

### Frontend

* Streamlit
* Requests

## Instalasi

### 1. Membuat Virtual Environment

```bash
python -m venv venv
```

Aktivasi virtual environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

---

### 2. Install Dependency Backend

```bash
pip install fastapi
pip install uvicorn
pip install sqlalchemy
pip install psycopg2-binary
pip install alembic
pip install python-dotenv
pip install pydantic-settings
pip install python-jose[cryptography]
pip install passlib[bcrypt]
pip install bcrypt==4.0.1
pip install python-multipart
pip install email-validator
```

Atau:

```bash
pip install -r requirements.txt
```

---

### 3. Install Dependency Frontend

```bash
pip install streamlit
pip install requests
```

---

## Database

---

## Menjalankan Backend

Masuk ke folder backend:

```bash
cd backend
```

Jalankan FastAPI:

```bash
uvicorn app.main:app --reload
```

Dokumentasi API:

```text
http://127.0.0.1:8000/docs
```

---

## Fitur yang Sudah Selesai

### Step 1

* Setup FastAPI
* Setup PostgreSQL
* Setup SQLAlchemy
* Setup Streamlit
* Konfigurasi Environment

### Step 2

* Register Mahasiswa
* Login Mahasiswa
* Password Hashing (Bcrypt)
* JWT Authentication
* RBAC Foundation
* Multi User Support

---

## Struktur Project

```text
campus-assignment-manager/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── routers/
│   │   ├── dependencies/
│   │   └── main.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   └── app.py
│
└── README.md
```
