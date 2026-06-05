import streamlit as st

from services.api import (
    get_assignments,
    create_assignment,
    complete_assignment,
    delete_assignment,
    get_courses,
)
from utils.auth import go_to


PRIORITY_LABEL = {
    "high": "🔴 High",
    "medium": "🟡 Medium",
    "low": "🟢 Low",
}


def render_assignment():
    token = st.session_state.token

    # Header + tombol kembali ke dashboard
    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("Tugas")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    # Flash message setelah aksi
    flash = st.session_state.pop("assignment_flash", None)
    if flash:
        st.success(flash)

    # --- Daftar tugas ---
    st.subheader("Daftar Tugas")

    response = get_assignments(token)

    if response.status_code != 200:
        st.error("Gagal memuat data tugas.")
        return

    assignments = response.json()

    if not assignments:
        st.info("Belum ada tugas.")
    else:
        for item in assignments:
            with st.container(border=True):
                col_info, col_status, col_action = st.columns([4, 2, 2])

                with col_info:
                    st.markdown(f"**{item['title']}**")
                    st.write(
                        f"{item['course_name']} | "
                        f"Deadline: {item['due_date']}"
                    )
                    st.caption(
                        PRIORITY_LABEL.get(
                            item["priority"], item["priority"]
                        )
                    )

                with col_status:
                    if item["status"] == "completed":
                        st.success("Completed")
                    else:
                        st.warning("Pending")

                with col_action:
                    if item["status"] != "completed":
                        if st.button(
                            "Selesai",
                            key=f"done_{item['id']}",
                        ):
                            done_resp = complete_assignment(
                                token, item["id"]
                            )
                            if done_resp.status_code == 200:
                                st.session_state.assignment_flash = (
                                    "Tugas ditandai selesai."
                                )
                            else:
                                st.session_state.assignment_flash = (
                                    "Gagal memperbarui tugas."
                                )
                            st.rerun()

                    if st.button(
                        "Hapus",
                        key=f"del_{item['id']}",
                    ):
                        del_resp = delete_assignment(
                            token, item["id"]
                        )
                        if del_resp.status_code in (200, 204):
                            st.session_state.assignment_flash = (
                                "Tugas dihapus."
                            )
                        else:
                            st.session_state.assignment_flash = (
                                "Gagal menghapus tugas."
                            )
                        st.rerun()

    st.divider()

    # --- Tambah tugas ---
    st.subheader("Tambah Tugas")

    # Ambil daftar mata kuliah untuk dipilih
    course_resp = get_courses(token)
    courses = course_resp.json() if course_resp.status_code == 200 else []

    if not courses:
        st.warning(
            "Tambahkan mata kuliah terlebih dahulu "
            "sebelum membuat tugas."
        )
        return

    course_options = {c["course_name"]: c["id"] for c in courses}

    selected_course = st.selectbox(
        "Mata Kuliah",
        list(course_options.keys()),
    )
    title = st.text_input("Judul Tugas")
    due_date = st.date_input("Deadline")
    priority = st.selectbox("Priority", ["low", "medium", "high"])

    if st.button("Add Assignment", type="primary"):
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
