import streamlit as st

from services.api import (
    create_assignment,
    fetch_courses,
)
from utils.auth import go_to


def render_assignment():
    token = st.session_state.token

    # Header + tombol kembali ke dashboard
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("Tambah Tugas")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    # Flash message setelah aksi
    flash = st.session_state.pop("assignment_flash", None)
    if flash:
        st.success(flash)

    st.caption(
        "Daftar tugas beserta aksi Selesai dan Hapus "
        "ada di halaman Dashboard."
    )

    st.divider()

    # --- Tambah tugas ---
    st.subheader("Tambah Tugas")

    # Ambil daftar mata kuliah untuk dipilih
    try:
        courses = fetch_courses(token)
    except Exception:
        courses = []

    if not courses:
        st.warning(
            "Tambahkan mata kuliah terlebih dahulu "
            "sebelum membuat tugas."
        )
        return

    course_options = {c["course_name"]: c["id"] for c in courses}

    with st.form(key="add_assignment_form"):
        selected_course = st.selectbox(
            "Mata Kuliah",
            list(course_options.keys()),
        )
        title = st.text_input("Judul Tugas")
        due_date = st.date_input("Deadline")
        priority = st.selectbox("Priority", ["low", "medium", "high"])

        submit_add = st.form_submit_button(
            "Add Assignment", type="primary"
        )

    if submit_add:
        if not title:
            st.error("Judul tugas harus diisi.")
        else:
            data = {
                "course_id": course_options[selected_course],
                "title": title,
                "due_date": due_date.isoformat(),
                "priority": priority,
            }

            create_resp = create_assignment(token, data)

            if create_resp.status_code in (200, 201):
                st.session_state.assignment_flash = "Tugas ditambahkan."
                st.rerun()
            else:
                st.error("Gagal menambahkan tugas.")
