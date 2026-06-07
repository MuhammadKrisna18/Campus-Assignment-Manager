from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.profile import Profile
from app.models.user import User

from app.schemas.profile import (
    ProfileCreate,
    ProfileUpdate,
    ProfileResponse
)

from app.routers.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/profile",
    tags=["Profile"]
)


@router.post(
    "/",
    response_model=ProfileResponse
)
def create_profile(
    payload: ProfileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    # Cek apakah user sudah punya profile
    existing = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Profile sudah ada. Gunakan PUT untuk mengubah."
        )

    profile = Profile(
        user_id=current_user.id,
        full_name=payload.full_name,
        nickname=payload.nickname,
        nrp=payload.nrp,
        program=payload.program,
        department=payload.department,
        institution=payload.institution
    )

    db.add(profile)
    db.commit()
    db.refresh(profile)

    return profile


@router.get(
    "/",
    response_model=ProfileResponse
)
def get_my_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    profile = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile belum dibuat"
        )

    return profile


@router.put(
    "/",
    response_model=ProfileResponse
)
def update_profile(
    payload: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    profile = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile belum dibuat"
        )

    profile.full_name = payload.full_name
    profile.nickname = payload.nickname
    profile.nrp = payload.nrp
    profile.program = payload.program
    profile.department = payload.department
    profile.institution = payload.institution

    db.commit()
    db.refresh(profile)

    return profile


@router.delete(
    "/",
    status_code=204
)
def delete_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):
    profile = (
        db.query(Profile)
        .filter(
            Profile.user_id == current_user.id
        )
        .first()
    )

    if not profile:
        raise HTTPException(
            status_code=404,
            detail="Profile belum dibuat"
        )

    db.delete(profile)
    db.commit()

    return None
