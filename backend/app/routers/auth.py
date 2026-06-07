from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.user import User

from app.schemas.auth import (
    RegisterRequest,
    LoginRequest,
    LoginResponse,
    UserResponse,
    UpdateProfileRequest,
    ChangePasswordRequest,
)

from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)

from jose import jwt, JWTError
from fastapi.security import (
    HTTPBearer,
    HTTPAuthorizationCredentials
)

from app.core.config import settings

security = HTTPBearer()

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    token = credentials.credentials

    try:

        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )

    user = (
        db.query(User)
        .filter(User.id == int(user_id))
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User not found"
        )

    return user


@router.post("/register")
def register(
    payload: RegisterRequest,
    db: Session = Depends(get_db)
):

    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_user:

        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user = User(
        full_name=payload.full_name,
        email=payload.email,
        password_hash=hash_password(
            payload.password
        ),
        role="STUDENT"
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Register success"
    }


@router.post(
    "/login",
    response_model=LoginResponse
)
def login(
    payload: LoginRequest,
    db: Session = Depends(get_db)
):

    user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        payload.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": str(user.id),
            "role": user.role
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer",
        "user": user
    }


@router.get(
    "/me",
    response_model=UserResponse
)
def get_me(
    current_user: User = Depends(get_current_user)
):
    return current_user


@router.put(
    "/profile",
    response_model=UserResponse
)
def update_profile(
    payload: UpdateProfileRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not payload.full_name.strip():
        raise HTTPException(
            status_code=400,
            detail="Nama tidak boleh kosong"
        )

    current_user.full_name = payload.full_name.strip()
    db.commit()
    db.refresh(current_user)

    return current_user


@router.put("/change-password")
def change_password(
    payload: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not verify_password(
        payload.current_password,
        current_user.password_hash
    ):
        raise HTTPException(
            status_code=400,
            detail="Password lama tidak sesuai"
        )

    if len(payload.new_password) < 6:
        raise HTTPException(
            status_code=400,
            detail="Password baru minimal 6 karakter"
        )

    current_user.password_hash = hash_password(
        payload.new_password
    )
    db.commit()

    return {"message": "Password berhasil diubah"}