import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

# Satu Session global -> koneksi TCP dipakai ulang (keep-alive),
# sehingga setiap request lebih cepat dibanding requests.get/post langsung.
_session = requests.Session()


def _auth_headers(token):
    return {"Authorization": f"Bearer {token}"}


# ============================================================
# AUTH (tidak di-cache)
# ============================================================

def register_user(full_name, email, password):
    return _session.post(
        f"{BASE_URL}/auth/register",
        json={
            "full_name": full_name,
            "email": email,
            "password": password,
        },
        timeout=5,
    )


def login_user(email, password):
    return _session.post(
        f"{BASE_URL}/auth/login",
        json={
            "email": email,
            "password": password,
        },
        timeout=5,
    )


def get_current_user(token):
    return _session.get(
        f"{BASE_URL}/auth/me",
        headers=_auth_headers(token),
        timeout=5,
    )


# ============================================================
# READ (di-cache dengan st.cache_data)
# ------------------------------------------------------------
# - Hasil disimpan per-token selama TTL, jadi interaksi UI yang
#   tidak mengubah data tidak memicu request HTTP baru.
# - raise_for_status() membuat error TIDAK ikut tersimpan di cache.
# - Pemanggil cukup membungkus dengan try/except.
# ============================================================

@st.cache_data(ttl=30, show_spinner=False)
def fetch_courses(token):
    resp = _session.get(
        f"{BASE_URL}/courses/",
        headers=_auth_headers(token),
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=30, show_spinner=False)
def fetch_schedules(token):
    resp = _session.get(
        f"{BASE_URL}/schedules/",
        headers=_auth_headers(token),
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()


@st.cache_data(ttl=30, show_spinner=False)
def fetch_assignments(token):
    resp = _session.get(
        f"{BASE_URL}/assignments/",
        headers=_auth_headers(token),
        timeout=5,
    )
    resp.raise_for_status()
    return resp.json()


def clear_cache():
    """Hapus cache data baca. Dipanggil setelah operasi tulis
    agar UI langsung menampilkan data terbaru."""
    fetch_courses.clear()
    fetch_schedules.clear()
    fetch_assignments.clear()


# ============================================================
# WRITE (otomatis invalidasi cache)
# ============================================================

def create_course(token, data):
    resp = _session.post(
        f"{BASE_URL}/courses/",
        json=data,
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def update_course(token, course_id, data):
    resp = _session.put(
        f"{BASE_URL}/courses/{course_id}",
        json=data,
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def delete_course(token, course_id):
    resp = _session.delete(
        f"{BASE_URL}/courses/{course_id}",
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def create_schedule(token, data):
    resp = _session.post(
        f"{BASE_URL}/schedules/",
        json=data,
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def update_schedule(token, schedule_id, data):
    resp = _session.put(
        f"{BASE_URL}/schedules/{schedule_id}",
        json=data,
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def create_assignment(token, data):
    resp = _session.post(
        f"{BASE_URL}/assignments/",
        json=data,
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def complete_assignment(token, assignment_id):
    resp = _session.patch(
        f"{BASE_URL}/assignments/{assignment_id}/complete",
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp


def delete_assignment(token, assignment_id):
    resp = _session.delete(
        f"{BASE_URL}/assignments/{assignment_id}",
        headers=_auth_headers(token),
        timeout=5,
    )
    clear_cache()
    return resp
