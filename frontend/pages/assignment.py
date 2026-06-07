import streamlit as st
from datetime import date

from services.api import (
    fetch_assignments,
    fetch_courses,
    create_assignment,
    update_assignment,
    complete_assignment,
    delete_assignment,
)
from utils.auth import go_to


PRIORITY_LABEL = {
    "high": "🔴 High",
    "medium": "🟡 Medium",
    "low": "🟢 Low",
}

PRIORITIES = ["low", "medium", "high"]


def render_assignment():
    token = st.session_state.token

    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("Tugas")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    flash = st.session_state.pop("assignment_flash", None)
    if flash:
        st.success(flash)

    # ============================================================
    # DAFTAR TUGAS
    # ============================================================

    st.subheader("Daftar Tugas")

    try:
        assignments = fetch_assignments(token)
    except Exception:
        st.error("Gagal memuat data tugas.")
        return

    if not assignments:
        st.info("Belum ada tugas.")
    else:
        for item in assignments:
            with st.container(border=True):
                col_info, col_status, col_action = st.columns(
                    [4, 2, 2]
                )

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
                            key=f"done_{item['id']}"
                        ):
                            resp = complete_assignment(
                                token, item["id"]
                            )
                            if resp.status_code == 200:
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
                        key=f"del_{item['id']}"
                    ):
                        resp = delete_assignment(
                            token, item["id"]
                        )
                        if resp.status_code in (200, 204):
                            st.session_state.assignment_flash = (
                                "Tugas dihapus."
                            )
                        else:
                            st.session_state.assignment_flash = (
                                "Gagal menghapus tugas."
                            )
                        st.rerun()

                # --- Form edit ---
                if item["status"] != "completed":
                    with st.expander("Edit"):
                        with st.form(
                            key=f"edit_form_{item['id']}"
                        ):
                            edit_title = st.text_input(
                                "Judul Tugas",
                                value=item["title"],
                                key=f"edit_title_{item['id']}"
                            )
                            edit_due = st.date_input(
                                "Deadline",
                                value=date.fromisoformat(
                                    item["due_date"]
                                ),
                                key=f"edit_due_{item['id']}"
                            )
                            edit_priority = st.selectbox(
                                "Priority",
                                PRIORITIES,
                                index=PRIORITIES.index(
                                    item["priority"]
                                ),
                                key=f"edit_prio_{item['id']}"
                            )
                            save = st.form_submit_button(
                                "Simpan Perubahan"
                            )

                        if save:
                            if not edit_title:
                                st.error(
                                    "Judul tugas harus diisi."
                                )
                            else:
                                resp = update_assignment(
                                    token,
                                    item["id"],
                                    {
                                        "title": edit_title,
                                        "due_date": edit_due.isoformat(),
                                        "priority": edit_priority,
                                    }
                                )
                                if resp.status_code == 200:
                                    st.session_state.assignment_flash = (
                                        "Tugas diperbarui."
                                    )
                                    st.rerun()
                                else:
                                    try:
                                        detail = resp.json().get(
                                            "detail",
                                            "Gagal memperbarui tugas."
                                        )
                                    except Exception:
                                        detail = (
                                            "Gagal memperbarui tugas."
                                        )
                                    st.error(detail)

    st.divider()

    # ============================================================
    # TAMBAH TUGAS
    # ============================================================

    st.subheader("Tambah Tugas")

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
        priority = st.selectbox("Priority", PRIORITIES)

        submit_add = st.form_submit_button(
            "Add Assignment",
            type="primary"
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
            resp = create_assignment(token, data)

            if resp.status_code in (200, 201):
                st.session_state.assignment_flash = (
                    "Tugas ditambahkan."
                )
                st.rerun()
            else:
                st.error("Gagal menambahkan tugas.")
