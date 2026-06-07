# Campus Assignment Manager

Sistem manajemen tugas dan akademik mahasiswa berbasis FastAPI, PostgreSQL, dan Streamlit.

---

## Tech Stack

### Backend

* **FastAPI** — REST API framework
* **SQLAlchemy** — ORM
* **PostgreSQL** — Database relasional
* **python-jose** — JWT Authentication
* **passlib + bcrypt** — Password hashing
* **pydantic-settings** — Manajemen konfigurasi dari `.env`

### Frontend

* **Streamlit** — Web framework interaktif
* **Requests** — HTTP client untuk berkomunikasi dengan backend
* **streamlit-cookies-controller** — Persistensi sesi login via cookie browser

---

## Fitur

### Autentikasi & Multi-User

* Register dan login mahasiswa
* Password hashing (bcrypt)
* JWT Authentication dengan masa berlaku 60 menit
* Sesi login bertahan saat refresh (disimpan di cookie per-browser)
* Isolasi data per-user (setiap mahasiswa hanya melihat data miliknya)

### Mata Kuliah (Course)

* CRUD mata kuliah (tambah, lihat, edit, hapus)
* Validasi duplikat nama mata kuliah (case-insensitive)
* Input grade per mata kuliah

### GPA Tracker

* Memberi/mengubah nilai (grade) mata kuliah yang sudah ada
* Perhitungan IPK otomatis: bobot = poin grade × SKS, IPK = total bobot / total SKS
* Terhubung langsung ke data Course (satu sumber data, tidak terpisah)

### Jadwal (Schedule)

* CRUD jadwal perkuliahan
* Validasi bentrok jam antar jadwal pada hari yang sama
* Validasi jam selesai harus setelah jam mulai

### Tugas (Assignment)

* Tambah tugas dengan mata kuliah, deadline, dan prioritas
* Tandai tugas selesai / hapus tugas (dari Dashboard)
* Ringkasan tugas di Dashboard: metrik total, belum selesai, selesai
* Daftar tugas diurutkan berdasarkan deadline terdekat

### Dashboard

* Informasi profil user
* Ringkasan tugas (metrik + daftar interaktif dengan aksi Selesai/Hapus)
* Daftar mata kuliah (termasuk grade)
* Daftar jadwal
* Navigasi cepat ke semua fitur

### Performa

* HTTP connection pooling (`requests.Session`)
* Caching data baca (`st.cache_data` dengan TTL 30 detik, auto-invalidasi saat operasi tulis)
* Form input dibungkus `st.form` agar tidak memicu rerun berulang saat mengetik

---

## Instalasi

### 1. Clone Repository

```bash
git clone <repository-url>
cd FinalProject_CampusAssignmentManager
```

### 2. Membuat Virtual Environment

```bash
python -m venv venv
```

Aktivasi:

```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependency Backend

```bash
cd backend
pip install -r requirements.txt
```

### 4. Install Dependency Frontend

```bash
cd frontend
pip install -r requirements.txt
```

---

## Konfigurasi Database

### 1. Buat database PostgreSQL

```sql
CREATE DATABASE campus_assignment_db;
```

### 2. Konfigurasi file `.env`

Buat file `backend/.env` dengan isi:

```env
DATABASE_URL=postgresql://postgres:<password>@localhost:5432/campus_assignment_db

SECRET_KEY=<your-secret-key>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

Sesuaikan `<password>`, port, dan nama database sesuai konfigurasi PostgreSQL lokal.

### 3. Tabel otomatis dibuat

Tabel dibuat otomatis saat backend pertama kali dijalankan (`Base.metadata.create_all`). Jika menambahkan kolom baru pada model setelah tabel sudah terbuat, perlu migrasi manual, misalnya:

```sql
ALTER TABLE courses ADD COLUMN grade VARCHAR;
```

---

## Menjalankan Aplikasi

### Backend

```bash
cd backend
uvicorn app.main:app --reload
```

API berjalan di `http://127.0.0.1:8000`

Dokumentasi API (Swagger): `http://127.0.0.1:8000/docs`

### Frontend

```bash
cd frontend
streamlit run app.py
```

Aplikasi berjalan di `http://localhost:8501`

---

## Struktur Project

```text
FinalProject_CampusAssignmentManager/
│
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py          # Konfigurasi dari .env
│   │   │   ├── database.py        # SQLAlchemy engine & session
│   │   │   └── security.py        # Hashing & JWT
│   │   │
│   │   ├── models/
│   │   │   ├── user.py            # Model User
│   │   │   ├── course.py          # Model Course (+ grade)
│   │   │   ├── schedule.py        # Model Schedule
│   │   │   └── assignment.py      # Model Assignment
│   │   │
│   │   ├── schemas/
│   │   │   ├── auth.py            # Schema register/login/user
│   │   │   ├── course.py          # Schema CRUD course
│   │   │   ├── schedule.py        # Schema CRUD schedule
│   │   │   └── assignment.py      # Schema CRUD assignment
│   │   │
│   │   ├── routers/
│   │   │   ├── auth.py            # Endpoint register/login/me
│   │   │   ├── course.py          # Endpoint CRUD course
│   │   │   ├── schedule.py        # Endpoint CRUD schedule
│   │   │   └── assignment.py      # Endpoint CRUD assignment
│   │   │
│   │   ├── dependencies/
│   │   │   └── auth.py            # Role-based guard (placeholder)
│   │   │
│   │   └── main.py                # FastAPI app entry point
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── pages/
│   │   ├── login.py               # Halaman login
│   │   ├── register.py            # Halaman register
│   │   ├── dashboard.py           # Dashboard + ringkasan tugas
│   │   ├── course.py              # CRUD mata kuliah
│   │   ├── schedule.py            # CRUD jadwal
│   │   ├── assignment.py          # Tambah tugas
│   │   └── gpa_tracker.py         # GPA Tracker
│   │
│   ├── services/
│   │   └── api.py                 # HTTP client (Session + caching)
│   │
│   ├── utils/
│   │   └── auth.py                # Session state + cookie management
│   │
│   ├── app.py                     # Entry point + routing
│   └── requirements.txt
│
├── .gitignore
└── readme.MD
```

---

## API Endpoints

### Authentication

| Method | Endpoint          | Deskripsi              |
| ------ | ----------------- | ---------------------- |
| POST   | `/auth/register`  | Register mahasiswa     |
| POST   | `/auth/login`     | Login, mendapat JWT    |
| GET    | `/auth/me`        | Data user yang login   |

### Course

| Method | Endpoint            | Deskripsi               |
| ------ | ------------------- | ----------------------- |
| GET    | `/courses/`         | Daftar mata kuliah user |
| POST   | `/courses/`         | Tambah mata kuliah      |
| PUT    | `/courses/{id}`     | Edit mata kuliah        |
| DELETE | `/courses/{id}`     | Hapus mata kuliah       |

### Schedule

| Method | Endpoint              | Deskripsi          |
| ------ | --------------------- | ------------------ |
| GET    | `/schedules/`         | Daftar jadwal user |
| POST   | `/schedules/`         | Tambah jadwal      |
| PUT    | `/schedules/{id}`     | Edit jadwal        |

### Assignment

| Method | Endpoint                         | Deskripsi                   |
| ------ | -------------------------------- | --------------------------- |
| GET    | `/assignments/`                  | Daftar tugas user           |
| POST   | `/assignments/`                  | Tambah tugas                |
| PATCH  | `/assignments/{id}/complete`     | Tandai tugas selesai        |
| DELETE | `/assignments/{id}`              | Hapus tugas                 |

---

## Grade System

| Grade | Poin |
| ----- | ---- |
| A     | 4.0  |
| AB    | 3.5  |
| B     | 3.0  |
| BC    | 2.5  |
| C     | 2.0  |
| D     | 1.0  |
| E     | 0.0  |

IPK dihitung: `Σ (poin grade × SKS) / Σ SKS`

---

## Catatan

* Backend harus berjalan terlebih dahulu sebelum frontend agar API tersedia.
* Pastikan PostgreSQL aktif dan database sudah dibuat sebelum menjalankan backend.
* File `.env` berisi credential dan tidak boleh di-commit ke repository (sudah termasuk di `.gitignore`).
* Cookie sesi login berlaku 60 menit, sinkron dengan masa hidup JWT.
