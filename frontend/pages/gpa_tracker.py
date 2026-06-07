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


def _calc_gpa(rows):
    """Hitung GPA dari list dict {SKS, Bobot}."""
    total_sks = sum(r["SKS"] for r in rows)
    total_bobot = sum(r["Bobot"] for r in rows)
    return round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0


def render_gpa_tracker():
    token = st.session_state.token

    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("GPA Tracker")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    flash = st.session_state.pop("gpa_flash", None)
    if flash:
        st.success(flash)

    try:
        courses = fetch_courses(token)
    except Exception:
        st.error("Gagal memuat data mata kuliah.")
        return

    # ============================================================
    # BERI NILAI
    # ============================================================

    st.subheader("Beri Nilai Mata Kuliah")

    if not courses:
        st.info(
            "Belum ada mata kuliah. "
            "Tambahkan di halaman Mata Kuliah terlebih dahulu."
        )
    else:
        course_options = {
            f"Sem {c.get('semester') or '?'} — "
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
                    "semester": selected_course.get("semester"),
                    "grade": grade,
                }
            )
            if update_resp.status_code == 200:
                st.session_state.gpa_flash = (
                    f"Nilai {selected_course['course_name']} "
                    f"({grade}) disimpan."
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

    # ============================================================
    # KUMPULKAN DATA NILAI
    # ============================================================

    rows = []
    for course in courses:
        g = course.get("grade")
        if not g or g not in GRADE_POINTS:
            continue
        sks = course["credits"]
        rows.append({
            "Semester": course.get("semester") or 0,
            "Mata Kuliah": course["course_name"],
            "SKS": sks,
            "Grade": g,
            "Bobot": GRADE_POINTS[g] * sks,
        })

    if not rows:
        st.info("Belum ada nilai yang dimasukkan.")
        return

    df = pd.DataFrame(rows)

    # ============================================================
    # RINGKASAN KESELURUHAN
    # ============================================================

    st.subheader("Ringkasan GPA")

    current_gpa = _calc_gpa(rows)
    total_sks = df["SKS"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("IPK Kumulatif", f"{current_gpa:.2f}")
    col2.metric("Total SKS", int(total_sks))
    col3.metric("Mata Kuliah Dinilai", len(rows))

    st.divider()

    # ============================================================
    # TABEL NILAI PER SEMESTER
    # ============================================================

    st.subheader("Tabel Nilai")

    # Filter semester
    semesters = sorted(df["Semester"].unique())
    sem_options = ["Semua"] + [
        f"Semester {s}" if s > 0 else "Tanpa Semester"
        for s in semesters
    ]
    selected_sem = st.selectbox("Filter Semester", sem_options)

    if selected_sem == "Semua":
        display_df = df.drop(columns=["Bobot"])
    else:
        if selected_sem == "Tanpa Semester":
            sem_val = 0
        else:
            sem_val = int(selected_sem.split()[-1])
        display_df = df[df["Semester"] == sem_val].drop(
            columns=["Bobot"]
        )

    st.dataframe(
        display_df.reset_index(drop=True),
        width="stretch",
        hide_index=True
    )

    st.divider()

    # ============================================================
    # GRAFIK IPK PER SEMESTER
    # ============================================================

    st.subheader("Grafik IPK per Semester")

    # Hitung IPK per semester (hanya semester bernomor)
    df_sem = df[df["Semester"] > 0].copy()

    if df_sem.empty:
        st.info(
            "Tambahkan semester pada mata kuliah "
            "untuk melihat grafik IPK per semester."
        )
    else:
        sem_gpa = []
        for sem in sorted(df_sem["Semester"].unique()):
            sem_rows = df_sem[df_sem["Semester"] == sem]
            sem_sks = sem_rows["SKS"].sum()
            sem_bobot = sem_rows["Bobot"].sum()
            sem_gpa.append({
                "Semester": f"Sem {sem}",
                "IPS": round(sem_bobot / sem_sks, 2)
            })

        df_chart = pd.DataFrame(sem_gpa).set_index("Semester")

        st.line_chart(df_chart)

        # Tabel IPS per semester
        st.caption("IPS (Indeks Prestasi Semester) tiap semester")
        st.dataframe(
            df_chart.reset_index(),
            width="stretch",
            hide_index=True
        )
