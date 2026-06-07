import streamlit as st
import pandas as pd

from utils.auth import go_to
from services.api import fetch_courses, update_course


GRADES = ["A", "AB", "B", "BC", "C", "D", "E"]

GRADE_POINTS = {
    "A": 4.0,
    "AB": 3.5,
    "B": 3.0,
    "BC": 2.5,
    "C": 2.0,
    "D": 1.0,
    "E": 0.0,
}


def render_gpa_tracker():
    token = st.session_state.token

    # Header + tombol kembali ke dashboard
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("GPA Tracker")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    # Flash message setelah aksi
    flash = st.session_state.pop("gpa_flash", None)
    if flash:
        st.success(flash)

    # Ambil data mata kuliah dari backend
    try:
        courses = fetch_courses(token)
    except Exception:
        st.error("Gagal memuat data mata kuliah.")
        return

    # --- Beri / Ubah Nilai Mata Kuliah ---
    st.subheader("Beri Nilai Mata Kuliah")

    if not courses:
        st.info(
            "Belum ada mata kuliah. "
            "Tambahkan mata kuliah terlebih dahulu di halaman Mata Kuliah."
        )
    else:
        course_options = {
            f"{c['course_name']} ({c['credits']} SKS)": c
            for c in courses
        }

        col1, col2 = st.columns([3, 1])

        with col1:
            selected_label = st.selectbox(
                "Mata Kuliah",
                list(course_options.keys())
            )

        selected_course = course_options[selected_label]

        with col2:
            current_grade = selected_course.get("grade")
            grade = st.selectbox(
                "Grade",
                GRADES,
                index=(
                    GRADES.index(current_grade)
                    if current_grade in GRADES
                    else 0
                )
            )

        if st.button("Simpan Nilai", type="primary"):
            update_resp = update_course(
                token,
                selected_course["id"],
                {
                    "course_name": selected_course["course_name"],
                    "credits": selected_course["credits"],
                    "class_name": selected_course["class_name"],
                    "lecturer_name": selected_course["lecturer_name"],
                    "grade": grade,
                }
            )

            if update_resp.status_code == 200:
                st.session_state.gpa_flash = (
                    f"Nilai untuk {selected_course['course_name']} "
                    f"({grade}) berhasil disimpan."
                )
                st.rerun()
            else:
                try:
                    detail = update_resp.json().get(
                        "detail", "Gagal menyimpan nilai."
                    )
                except Exception:
                    detail = "Gagal menyimpan nilai."
                st.error(detail)

    st.divider()

    # --- GPA Summary ---
    st.subheader("Ringkasan GPA")

    rows = []

    for course in courses:
        grade = course.get("grade")

        if not grade or grade not in GRADE_POINTS:
            continue

        sks = course["credits"]
        bobot = GRADE_POINTS[grade] * sks

        rows.append({
            "Mata Kuliah": course["course_name"],
            "SKS": sks,
            "Grade": grade,
            "Bobot": bobot,
        })

    if not rows:
        st.info("Belum ada nilai yang dimasukkan.")
        return

    df = pd.DataFrame(rows)

    # Tampilkan tabel nilai
    st.dataframe(
        df,
        width='stretch',
        hide_index=True
    )

    # Hitung GPA
    total_bobot = df["Bobot"].sum()
    total_sks = df["SKS"].sum()
    current_gpa = total_bobot / total_sks if total_sks > 0 else 0.0

    st.divider()

    # Metrik GPA
    col_gpa, col_sks = st.columns(2)

    with col_gpa:
        st.metric("Current GPA", f"{current_gpa:.2f}")

    with col_sks:
        st.metric("Total SKS Dinilai", int(total_sks))
