import streamlit as st

from services.api import (
    get_profile,
    create_profile,
    update_profile_detail,
    change_password,
)
from utils.auth import go_to


def render_profile():
    token = st.session_state.token
    user = st.session_state.user

    col_title, col_back = st.columns([4, 1])
    with col_title:
        st.title("Profil")
    with col_back:
        if st.button("Dashboard"):
            go_to("dashboard")
            st.rerun()

    flash = st.session_state.pop("profile_flash", None)
    if flash:
        st.success(flash)

    # ============================================================
    # INFO AKUN (dari tabel users — read only)
    # ============================================================

    st.subheader("Informasi Akun")

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.write("**Nama**")
            st.write("**Email**")
            st.write("**Role**")
            st.write("**Bergabung**")
        with col2:
            st.write(user["full_name"])
            st.write(user["email"])
            st.write(user["role"])
            created = str(user.get("created_at", "-"))[:10]
            st.write(created)

    st.divider()

    # ============================================================
    # FETCH PROFILE DETAIL
    # ============================================================

    resp = get_profile(token)
    profile_exists = resp.status_code == 200
    profile = resp.json() if profile_exists else None

    # ============================================================
    # FORM PROFILE DETAIL (buat / edit)
    # ============================================================

    st.subheader(
        "Edit Profil" if profile_exists else "Lengkapi Profil"
    )

    if not profile_exists:
        st.info(
            "Profil belum dibuat. "
            "Isi form di bawah untuk melengkapi data akademik."
        )

    with st.form("form_profile_detail"):
        full_name = st.text_input(
            "Nama Lengkap",
            value=profile["full_name"] if profile else user["full_name"]
        )
        nickname = st.text_input(
            "Nama Panggilan (opsional)",
            value=profile["nickname"] or "" if profile else ""
        )
        nrp = st.text_input(
            "NRP / NIM",
            value=profile["nrp"] if profile else ""
        )
        program = st.text_input(
            "Program Studi",
            value=profile["program"] if profile else ""
        )
        department = st.text_input(
            "Departemen / Jurusan",
            value=profile["department"] if profile else ""
        )
        institution = st.text_input(
            "Institusi / Universitas",
            value=profile["institution"] if profile else ""
        )

        submit_label = (
            "Simpan Perubahan" if profile_exists else "Buat Profil"
        )
        submit = st.form_submit_button(submit_label, type="primary")

    if submit:
        if not full_name.strip() or not nrp.strip() \
                or not program.strip() or not department.strip() \
                or not institution.strip():
            st.error(
                "Nama, NRP, program studi, departemen, "
                "dan institusi harus diisi."
            )
        else:
            data = {
                "full_name": full_name.strip(),
                "nickname": nickname.strip() or None,
                "nrp": nrp.strip(),
                "program": program.strip(),
                "department": department.strip(),
                "institution": institution.strip(),
            }

            if profile_exists:
                save_resp = update_profile_detail(token, data)
                ok_status = 200
                msg = "Profil berhasil diperbarui."
            else:
                save_resp = create_profile(token, data)
                ok_status = 200
                msg = "Profil berhasil dibuat."

            if save_resp.status_code in (ok_status, 201):
                st.session_state.profile_flash = msg
                st.rerun()
            else:
                try:
                    detail = save_resp.json().get(
                        "detail", "Gagal menyimpan profil."
                    )
                except Exception:
                    detail = "Gagal menyimpan profil."
                st.error(detail)

    st.divider()

    # ============================================================
    # GANTI PASSWORD
    # ============================================================

    st.subheader("Ganti Password")

    with st.form("form_change_password"):
        current_pw = st.text_input(
            "Password Lama",
            type="password"
        )
        new_pw = st.text_input(
            "Password Baru",
            type="password",
            placeholder="Minimal 6 karakter"
        )
        confirm_pw = st.text_input(
            "Konfirmasi Password Baru",
            type="password"
        )
        submit_pw = st.form_submit_button("Ganti Password")

    if submit_pw:
        if not current_pw or not new_pw or not confirm_pw:
            st.error("Semua field harus diisi.")
        elif len(new_pw) < 6:
            st.error("Password baru minimal 6 karakter.")
        elif new_pw != confirm_pw:
            st.error("Konfirmasi password tidak cocok.")
        else:
            pw_resp = change_password(
                token,
                {
                    "current_password": current_pw,
                    "new_password": new_pw,
                }
            )
            if pw_resp.status_code == 200:
                st.session_state.profile_flash = (
                    "Password berhasil diubah."
                )
                st.rerun()
            else:
                try:
                    detail = pw_resp.json().get(
                        "detail", "Gagal mengganti password."
                    )
                except Exception:
                    detail = "Gagal mengganti password."
                st.error(detail)
