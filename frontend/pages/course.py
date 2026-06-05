import streamlit as st

from services.api import (
    get_courses,
    create_course,
    delete_course,
)
from utils.auth import go_to


DAYS = [
    "Senin",
    "Selasa",
    "Rabu",
    "Kamis",
    "Jumat",
    "Sabtu",
    "Minggu",
]


def render_course():
    token = st.session_state.token

    # Header + tombol kembali ke dashboard
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("Mata Kuliah")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    # Flash message setelah aksi
    flash = st.session_state.pop("course_flash", None)
    if flash:
        st.success(flash)

    # --- Daftar mata kuliah ---
    st.subheader("Daftar Mata Kuliah")

    response = get_courses(token)

    if response.status_code != 200:
        st.error("Gagal memuat data mata kuliah.")
        return

    courses = response.json()

    if not courses:
        st.info("Belum ada mata kuliah.")
    else:
        for course in courses:
            with st.container(border=True):
                col_info, col_action = st.columns([5, 1])

                with col_info:
                    st.markdown(f"**{course['course_name']}**")
                    st.write(
                        f"Dosen: {course['lecturer_name']} | "
                        f"Kelas: {course['class_name']} | "
                        f"SKS: {course['credits']}"
                    )
                    st.caption(
                        f"{course['day']}, "
                        f"{course['schedule_date']} "
                        f"jam {course['schedule_time']}"
                    )

                with col_action:
                    if st.button(
                        "Hapus",
                        key=f"del_{course['id']}",
                    ):
                        del_resp = delete_course(
                            token, course["id"]
                        )
                        if del_resp.status_code in (200, 204):
                            st.session_state.course_flash = (
                                "Mata kuliah dihapus."
                            )
                        else:
                            st.session_state.course_flash = (
                                "Gagal menghapus mata kuliah."
                            )
                        st.rerun()

    st.divider()

    # --- Tambah mata kuliah ---
    st.subheader("Tambah Mata Kuliah")

    course_name = st.text_input("Nama Mata Kuliah")
    lecturer_name = st.text_input("Nama Dosen")
    class_name = st.text_input("Kelas")
    credits = st.number_input("SKS", min_value=1, step=1)
    day = st.selectbox("Hari", DAYS)
    schedule_date = st.date_input("Tanggal")
    schedule_time = st.time_input("Jam")

    if st.button("Tambah", type="primary"):
        if not course_name or not lecturer_name or not class_name:
            st.error("Nama mata kuliah, dosen, dan kelas harus diisi.")
        else:
            data = {
                "course_name": course_name,
                "credits": int(credits),
                "class_name": class_name,
                "lecturer_name": lecturer_name,
                "day": day,
                "schedule_date": schedule_date.isoformat(),
                "schedule_time": schedule_time.strftime("%H:%M:%S"),
            }

            create_resp = create_course(token, data)

            if create_resp.status_code in (200, 201):
                st.session_state.course_flash = "Mata kuliah ditambahkan."
                st.rerun()
            else:
                st.error("Gagal menambahkan mata kuliah.")
