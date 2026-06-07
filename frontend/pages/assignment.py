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

PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

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
    # FETCH DATA
    # ============================================================

    try:
        assignments = fetch_assignments(token)
    except Exception:
        st.error("Gagal memuat data tugas.")
        return

    try:
        courses = fetch_courses(token)
    except Exception:
        courses = []

    # ============================================================
    # FILTER & SORT
    # ============================================================

    st.subheader("Daftar Tugas")

    col_f1, col_f2, col_f3 = st.columns(3)

    with col_f1:
        filter_status = st.selectbox(
            "Status",
            ["Semua", "Pending", "Completed"],
            key="filter_status"
        )

    with col_f2:
        filter_priority = st.selectbox(
            "Priority",
            ["Semua", "High", "Medium", "Low"],
            key="filter_priority"
        )

    with col_f3:
        # Daftar mata kuliah untuk filter
        course_names = ["Semua"] + sorted(
            list({a["course_name"] for a in assignments})
        )
        filter_course = st.selectbox(
            "Mata Kuliah",
            course_names,
            key="filter_course"
        )

    col_s1, col_s2 = st.columns([2, 2])

    with col_s1:
        sort_by = st.selectbox(
            "Urutkan",
            ["Deadline Terdekat", "Deadline Terjauh", "Priority Tertinggi"],
            key="sort_by"
        )

    # Terapkan filter
    filtered = assignments

    if filter_status == "Pending":
        filtered = [a for a in filtered if a["status"] == "pending"]
    elif filter_status == "Completed":
        filtered = [a for a in filtered if a["status"] == "completed"]

    if filter_priority != "Semua":
        filtered = [
            a for a in filtered
            if a["priority"] == filter_priority.lower()
        ]

    if filter_course != "Semua":
        filtered = [
            a for a in filtered
            if a["course_name"] == filter_course
        ]

    # Terapkan sort
    if sort_by == "Deadline Terdekat":
        filtered = sorted(filtered, key=lambda a: a["due_date"])
    elif sort_by == "Deadline Terjauh":
        filtered = sorted(
            filtered, key=lambda a: a["due_date"], reverse=True
        )
    elif sort_by == "Priority Tertinggi":
        filtered = sorted(
            filtered,
            key=lambda a: PRIORITY_ORDER.get(a["priority"], 99)
        )

    # Ringkasan hasil filter
    total = len(assignments)
    showing = len(filtered)
    pending_count = sum(1 for a in assignments if a["status"] == "pending")
    completed_count = total - pending_count

    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("Total", total)
    col_m2.metric("Pending", pending_count)
    col_m3.metric("Completed", completed_count)

    if showing != total:
        st.caption(f"Menampilkan {showing} dari {total} tugas")

    if not filtered:
        st.info("Tidak ada tugas yang sesuai filter.")
    else:
        for item in filtered:
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
                    if item.get("note"):
                        st.info(f"📝 {item['note']}")

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

                # Form edit hanya untuk tugas pending
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
                            edit_note = st.text_area(
                                "Catatan",
                                value=item.get("note") or "",
                                placeholder="Tulis catatan, progress, atau link referensi...",
                                key=f"edit_note_{item['id']}"
                            )
                            save = st.form_submit_button(
                                "Simpan Perubahan"
                            )

                        if save:
                            if not edit_title:
                                st.error("Judul tugas harus diisi.")
                            else:
                                resp = update_assignment(
                                    token,
                                    item["id"],
                                    {
                                        "title": edit_title,
                                        "due_date": edit_due.isoformat(),
                                        "priority": edit_priority,
                                        "note": edit_note or None,
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
                                        detail = "Gagal memperbarui tugas."
                                    st.error(detail)

    st.divider()

    # ============================================================
    # TAMBAH TUGAS
    # ============================================================

    st.subheader("Tambah Tugas")

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
        note = st.text_area(
            "Catatan (opsional)",
            placeholder="Tulis catatan, progress, atau link referensi..."
        )

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
                "note": note or None,
            }
            resp = create_assignment(token, data)

            if resp.status_code in (200, 201):
                st.session_state.assignment_flash = "Tugas ditambahkan."
                st.rerun()
            else:
                st.error("Gagal menambahkan tugas.")
