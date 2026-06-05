import streamlit as st
import pandas as pd

from utils.auth import go_to


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
    flash = st.session_state.pop(
        "gpa_flash",
        None
    )
    if flash:
        st.success(flash)

    st.subheader("Tambah Nilai")

    col1, col2, col3 = st.columns(3)

    with col1:
        course_name = st.text_input(
            "Nama Mata Kuliah"
        )

    with col2:
        credits = st.number_input(
            "SKS",
            min_value=1,
            step=1,
            value=3
        )

    with col3:
        grade = st.selectbox(
            "Grade",
            GRADES
        )

    if st.button(
        "Tambah Nilai",
        type="primary"
    ):

        if not course_name:
            st.error("Nama mata kuliah harus diisi.")
        else:
            st.session_state.gpa_flash = (
                f"Nilai untuk {course_name} "
                f"({grade}) berhasil ditambahkan."
            )
            st.rerun()

    st.divider()

    # --- GPA Summary ---
    st.subheader("Ringkasan GPA")

    # Mock data untuk demo
    gpa_data = {
        "Mata Kuliah": [
            "Matematika",
            "Fisika",
            "Kimia",
            "Biologi",
            "Bahasa Inggris",
        ],
        "SKS": [3, 4, 3, 3, 2],
        "Grade": ["A", "AB", "B", "A", "AB"],
        "Bobot": [
            GRADE_POINTS["A"] * 3,
            GRADE_POINTS["AB"] * 4,
            GRADE_POINTS["B"] * 3,
            GRADE_POINTS["A"] * 3,
            GRADE_POINTS["AB"] * 2,
        ],
    }

    df = pd.DataFrame(gpa_data)

    # Tampilkan tabel nilai
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Hitung GPA
    total_bobot = df["Bobot"].sum()
    total_sks = df["SKS"].sum()
    current_gpa = total_bobot / total_sks if total_sks > 0 else 0.0

    st.divider()

    # Metrik GPA
    col_gpa, col_target = st.columns(2)

    with col_gpa:
        st.metric(
            "Current GPA",
            f"{current_gpa:.2f}"
        )

    with col_target:
        st.metric(
            "Target GPA",
            "3.50"
        )

    st.divider()

    # --- Grafik Trend GPA ---
    st.subheader("Trend GPA")

    # Mock historical data
    gpa_history = pd.DataFrame({
        "Semester": [
            "Sem 1",
            "Sem 2",
            "Sem 3",
            "Sem 4",
            "Sem 5",
        ],
        "GPA": [3.2, 3.35, 3.40, 3.45, current_gpa],
    })

    st.line_chart(
        gpa_history.set_index("Semester")
    )

    st.divider()

    # --- Performa Per Semester ---
    st.subheader("Performa Per Semester")

    semester_data = pd.DataFrame({
        "Semester": [
            "Sem 1",
            "Sem 2",
            "Sem 3",
            "Sem 4",
            "Sem 5",
        ],
        "Mata Kuliah": [5, 5, 5, 6, 5],
        "IPK": [3.2, 3.35, 3.40, 3.45, 3.48],
    })

    st.bar_chart(
        semester_data.set_index("Semester")
    )
