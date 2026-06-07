import streamlit as st

from datetime import time

from services.api import (
    fetch_schedules,
    create_schedule,
    fetch_courses,
    update_schedule,
    delete_schedule,
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


def _parse_time_input(raw: str):
    """
    Format input teks bebas menjadi objek time.
    Contoh:
      "9"     -> time(9, 0)   -> "09:00"
      "930"   -> time(9, 30)  -> "09:30"
      "9:30"  -> time(9, 30)  -> "09:30"
      "14:45" -> time(14, 45) -> "14:45"
    Mengembalikan None jika tidak valid.
    """
    raw = raw.strip().replace(".", ":")
    try:
        if ":" in raw:
            h, m = raw.split(":", 1)
            return time(int(h), int(m))
        elif len(raw) <= 2:
            return time(int(raw), 0)
        elif len(raw) == 3:
            return time(int(raw[0]), int(raw[1:]))
        elif len(raw) == 4:
            return time(int(raw[:2]), int(raw[2:]))
        else:
            return None
    except Exception:
        return None


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

                col_head, col_del = st.columns([5, 1])

                with col_head:
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

                with col_del:
                    if st.button(
                        "Hapus",
                        key=f"del_{schedule['id']}"
                    ):
                        del_resp = delete_schedule(
                            token, schedule["id"]
                        )
                        if del_resp.status_code in (200, 204):
                            st.session_state.schedule_flash = (
                                "Jadwal dihapus."
                            )
                        else:
                            st.session_state.schedule_flash = (
                                "Gagal menghapus jadwal."
                            )
                        st.rerun()

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

                        edit_start = st.text_input(
                            "Start Time (cth: 9 → 09:00, 930 → 09:30)",
                            value=_parse_time(
                                schedule["start_time"]
                            ).strftime("%H:%M"),
                            key=f"edit_start_{schedule['id']}"
                        )

                        edit_end = st.text_input(
                            "End Time (cth: 1045 → 10:45)",
                            value=_parse_time(
                                schedule["end_time"]
                            ).strftime("%H:%M"),
                            key=f"edit_end_{schedule['id']}"
                        )

                        save_edit = st.form_submit_button(
                            "Simpan Perubahan"
                        )

                    if save_edit:

                        parsed_start = _parse_time_input(edit_start)
                        parsed_end = _parse_time_input(edit_end)

                        if not edit_room:
                            st.error("Room harus diisi.")
                        elif parsed_start is None:
                            st.error(
                                "Format Start Time tidak valid. "
                                "Contoh: 9, 930, 09:30"
                            )
                        elif parsed_end is None:
                            st.error(
                                "Format End Time tidak valid. "
                                "Contoh: 9, 930, 09:30"
                            )
                        elif parsed_end <= parsed_start:
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
                                    "start_time": parsed_start.strftime(
                                        "%H:%M:%S"
                                    ),
                                    "end_time": parsed_end.strftime(
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
                                        update_resp.json().get(
                                            "detail",
                                            "Gagal memperbarui jadwal."
                                        )
                                    )
                                except Exception:
                                    detail = "Gagal memperbarui jadwal."
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

        start_time = st.text_input(
            "Start Time (cth: 9 → 09:00, 930 → 09:30)"
        )

        end_time = st.text_input(
            "End Time (cth: 1045 → 10:45)"
        )

        submit_add = st.form_submit_button(
            "Add Schedule",
            type="primary"
        )

    if submit_add:

        parsed_start = _parse_time_input(start_time)
        parsed_end = _parse_time_input(end_time)

        if not room:
            st.error("Room harus diisi.")
        elif parsed_start is None:
            st.error(
                "Format Start Time tidak valid. "
                "Contoh: 9, 930, 09:30"
            )
        elif parsed_end is None:
            st.error(
                "Format End Time tidak valid. "
                "Contoh: 9, 930, 09:30"
            )
        elif parsed_end <= parsed_start:

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
                "start_time": parsed_start.strftime(
                    "%H:%M:%S"
                ),
                "end_time": parsed_end.strftime(
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
