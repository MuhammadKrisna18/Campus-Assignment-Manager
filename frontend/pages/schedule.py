import streamlit as st

from datetime import time

from services.api import (
    fetch_schedules,
    create_schedule,
    fetch_courses,
    update_schedule,
)

from utils.auth import go_to


DAYS = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday",
]


def _parse_time(value):
    """Ubah string 'HH:MM:SS' dari API menjadi objek time."""
    try:
        parts = [int(p) for p in str(value).split(":")]
        return time(parts[0], parts[1])
    except Exception:
        return time(7, 0)


def render_schedule():

    token = st.session_state.token

    col_title, col_back = st.columns(
        [4, 1]
    )

    with col_title:
        st.title("Jadwal")

    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    flash = st.session_state.pop(
        "schedule_flash",
        None
    )

    if flash:
        st.success(flash)

    st.subheader(
        "Daftar Jadwal"
    )

    try:
        schedules = fetch_schedules(token)
    except Exception:
        st.error(
            "Gagal memuat data jadwal."
        )
        return

    if not schedules:

        st.info(
            "Belum ada jadwal."
        )

    else:

        for schedule in schedules:

            with st.container(
                border=True
            ):

                st.markdown(
                    f"**{schedule['course_name']}**"
                )

                st.write(
                    f"Hari: {schedule['day']} | "
                    f"Ruang: {schedule['room']}"
                )

                st.caption(
                    f"{schedule['start_time']} - "
                    f"{schedule['end_time']}"
                )

                # --- Form edit jadwal ---
                with st.expander("Edit"):

                    with st.form(
                        key=f"edit_form_{schedule['id']}"
                    ):

                        day_index = (
                            DAYS.index(schedule["day"])
                            if schedule["day"] in DAYS
                            else 0
                        )

                        edit_day = st.selectbox(
                            "Day",
                            DAYS,
                            index=day_index,
                            key=f"edit_day_{schedule['id']}"
                        )

                        edit_room = st.text_input(
                            "Room",
                            value=schedule["room"],
                            key=f"edit_room_{schedule['id']}"
                        )

                        edit_start = st.time_input(
                            "Start Time",
                            value=_parse_time(
                                schedule["start_time"]
                            ),
                            key=f"edit_start_{schedule['id']}"
                        )

                        edit_end = st.time_input(
                            "End Time",
                            value=_parse_time(
                                schedule["end_time"]
                            ),
                            key=f"edit_end_{schedule['id']}"
                        )

                        save_edit = st.form_submit_button(
                            "Simpan Perubahan"
                        )

                    if save_edit:

                        if not edit_room:

                            st.error(
                                "Room harus diisi."
                            )

                        elif edit_end <= edit_start:

                            st.error(
                                "Jam selesai harus setelah jam mulai."
                            )

                        else:

                            update_resp = update_schedule(
                                token,
                                schedule["id"],
                                {
                                    "day": edit_day,
                                    "room": edit_room,
                                    "start_time": edit_start.strftime(
                                        "%H:%M:%S"
                                    ),
                                    "end_time": edit_end.strftime(
                                        "%H:%M:%S"
                                    ),
                                }
                            )

                            if update_resp.status_code == 200:

                                st.session_state.schedule_flash = (
                                    "Jadwal diperbarui."
                                )

                                st.rerun()

                            else:

                                try:
                                    detail = (
                                        update_resp
                                        .json()
                                        .get(
                                            "detail",
                                            "Gagal memperbarui jadwal."
                                        )
                                    )
                                except Exception:
                                    detail = (
                                        "Gagal memperbarui jadwal."
                                    )

                                st.error(detail)

    st.divider()

    st.subheader(
        "Tambah Jadwal"
    )

    try:
        courses = fetch_courses(token)
    except Exception:
        courses = []

    if not courses:

        st.warning(
            "Tambahkan mata kuliah terlebih dahulu "
            "sebelum membuat jadwal."
        )

        return

    course_options = {
        c["course_name"]: c["id"]
        for c in courses
    }

    with st.form(key="add_schedule_form"):

        selected_course = st.selectbox(
            "Mata Kuliah",
            list(course_options.keys())
        )

        day = st.selectbox(
            "Day",
            DAYS
        )

        room = st.text_input(
            "Room"
        )

        start_time = st.time_input(
            "Start Time"
        )

        end_time = st.time_input(
            "End Time"
        )

        submit_add = st.form_submit_button(
            "Add Schedule",
            type="primary"
        )

    if submit_add:

        if not room:

            st.error(
                "Room harus diisi."
            )

        elif end_time <= start_time:

            st.error(
                "Jam selesai harus setelah jam mulai."
            )

        else:

            data = {
                "course_id": course_options[
                    selected_course
                ],
                "day": day,
                "room": room,
                "start_time": start_time.strftime(
                    "%H:%M:%S"
                ),
                "end_time": end_time.strftime(
                    "%H:%M:%S"
                ),
            }

            create_resp = create_schedule(
                token,
                data
            )

            if create_resp.status_code in (
                200,
                201
            ):

                st.session_state.schedule_flash = (
                    "Jadwal ditambahkan."
                )

                st.rerun()

            else:

                try:

                    detail = (
                        create_resp
                        .json()
                        .get(
                            "detail",
                            "Gagal menambahkan jadwal."
                        )
                    )

                except Exception:

                    detail = (
                        "Gagal menambahkan jadwal."
                    )

                st.error(detail)
