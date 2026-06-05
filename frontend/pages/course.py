import streamlit as st

from services.api import (
    get_courses,
    create_course,
    delete_course,
    update_course
)
from utils.auth import go_to


def render_course():
    token = st.session_state.token

    col_title, col_back = st.columns([4, 1])

    with col_title:
        st.title("Mata Kuliah")

    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    flash = st.session_state.pop(
        "course_flash",
        None
    )

    if flash:
        st.success(flash)

    st.subheader(
        "Daftar Mata Kuliah"
    )

    response = get_courses(token)

    if response.status_code != 200:
        st.error(
            "Gagal memuat data mata kuliah."
        )
        return

    courses = response.json()

    if not courses:

        st.info(
            "Belum ada mata kuliah."
        )

    else:

        for course in courses:

            with st.container(
                border=True
            ):

                col_info, col_action = st.columns(
                    [5, 1]
                )

                with col_info:

                    st.markdown(
                        f"**{course['course_name']}**"
                    )

                    st.write(
                        f"Dosen: {course['lecturer_name']} | "
                        f"Kelas: {course['class_name']} | "
                        f"SKS: {course['credits']}"
                    )

                with col_action:

                    if st.button(
                        "Hapus",
                        key=f"del_{course['id']}"
                    ):

                        del_resp = delete_course(
                            token,
                            course["id"]
                        )

                        if del_resp.status_code in (
                            200,
                            204
                        ):
                            st.session_state.course_flash = (
                                "Mata kuliah dihapus."
                            )
                        else:
                            st.session_state.course_flash = (
                                "Gagal menghapus mata kuliah."
                            )

                        st.rerun()

                # --- Form edit mata kuliah ---
                with st.expander("Edit"):

                    edit_name = st.text_input(
                        "Nama Mata Kuliah",
                        value=course["course_name"],
                        key=f"edit_name_{course['id']}"
                    )

                    edit_lecturer = st.text_input(
                        "Nama Dosen",
                        value=course["lecturer_name"],
                        key=f"edit_lecturer_{course['id']}"
                    )

                    edit_class = st.text_input(
                        "Kelas",
                        value=course["class_name"],
                        key=f"edit_class_{course['id']}"
                    )

                    edit_credits = st.number_input(
                        "SKS",
                        min_value=1,
                        step=1,
                        value=int(course["credits"]),
                        key=f"edit_credits_{course['id']}"
                    )

                    if st.button(
                        "Simpan Perubahan",
                        key=f"save_{course['id']}"
                    ):

                        if (
                            not edit_name
                            or not edit_lecturer
                            or not edit_class
                        ):

                            st.error(
                                "Semua field harus diisi."
                            )

                        else:

                            update_resp = update_course(
                                token,
                                course["id"],
                                {
                                    "course_name": edit_name,
                                    "credits": int(edit_credits),
                                    "class_name": edit_class,
                                    "lecturer_name": edit_lecturer,
                                }
                            )

                            if update_resp.status_code == 200:

                                st.session_state.course_flash = (
                                    "Mata kuliah diperbarui."
                                )

                                st.rerun()

                            else:

                                try:
                                    detail = (
                                        update_resp
                                        .json()
                                        .get(
                                            "detail",
                                            "Gagal memperbarui mata kuliah."
                                        )
                                    )
                                except Exception:
                                    detail = (
                                        "Gagal memperbarui mata kuliah."
                                    )

                                st.error(detail)

    st.divider()

    st.subheader(
        "Tambah Mata Kuliah"
    )

    course_name = st.text_input(
        "Nama Mata Kuliah"
    )

    lecturer_name = st.text_input(
        "Nama Dosen"
    )

    class_name = st.text_input(
        "Kelas"
    )

    credits = st.number_input(
        "SKS",
        min_value=1,
        step=1
    )

    if st.button(
        "Tambah",
        type="primary"
    ):

        if (
            not course_name
            or not lecturer_name
            or not class_name
        ):

            st.error(
                "Nama mata kuliah, dosen, dan kelas harus diisi."
            )

        else:

            data = {
                "course_name": course_name,
                "credits": int(credits),
                "class_name": class_name,
                "lecturer_name": lecturer_name,
            }

            create_resp = create_course(
                token,
                data
            )

            if create_resp.status_code in (
                200,
                201
            ):

                st.session_state.course_flash = (
                    "Mata kuliah ditambahkan."
                )

                st.rerun()

            else:

                try:

                    detail = (
                        create_resp
                        .json()
                        .get(
                            "detail",
                            "Gagal menambahkan mata kuliah."
                        )
                    )

                except Exception:

                    detail = (
                        "Gagal menambahkan mata kuliah."
                    )

                st.error(detail)