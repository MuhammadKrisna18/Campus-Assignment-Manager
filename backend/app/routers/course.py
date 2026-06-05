from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session
from sqlalchemy import func

from app.core.database import get_db

from app.models.course import Course
from app.models.user import User

from app.schemas.course import (
    CourseCreate,
    CourseResponse,
    CourseUpdate
)

from app.routers.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/courses",
    tags=["Courses"]
)


@router.post(
    "/",
    response_model=CourseResponse
)
def create_course(
    payload: CourseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    # ==========================
    # VALIDASI DUPLIKAT
    # ==========================

    existing_course = (
        db.query(Course)
        .filter(
            Course.user_id == current_user.id,
            func.lower(Course.course_name)
            == payload.course_name.lower()
        )
        .first()
    )

    if existing_course:

        raise HTTPException(
            status_code=400,
            detail=(
                f"Mata kuliah "
                f"'{payload.course_name}' "
                f"sudah ada"
            )
        )

    course = Course(
        user_id=current_user.id,
        course_name=payload.course_name.strip(),
        credits=payload.credits,
        class_name=payload.class_name,
        lecturer_name=payload.lecturer_name,
        grade=payload.grade
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


@router.get(
    "/",
    response_model=list[CourseResponse]
)
def get_my_courses(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    courses = (
        db.query(Course)
        .filter(
            Course.user_id == current_user.id
        )
        .all()
    )

    return courses

@router.put(
    "/{course_id}",
    response_model=CourseResponse
)
def update_course(
    course_id: int,
    payload: CourseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.user_id == current_user.id
        )
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    existing_course = (
        db.query(Course)
        .filter(
            Course.user_id == current_user.id,
            func.lower(Course.course_name)
            == payload.course_name.lower(),
            Course.id != course_id
        )
        .first()
    )

    if existing_course:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Mata kuliah "
                f"'{payload.course_name}' "
                f"sudah ada"
            )
        )

    course.course_name = payload.course_name.strip()
    course.credits = payload.credits
    course.class_name = payload.class_name
    course.lecturer_name = payload.lecturer_name
    course.grade = payload.grade

    db.commit()
    db.refresh(course)

    return course

@router.delete(
    "/{course_id}",
    status_code=204
)
def delete_course(
    course_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    course = (
        db.query(Course)
        .filter(
            Course.id == course_id,
            Course.user_id == current_user.id
        )
        .first()
    )

    if not course:

        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    db.delete(course)
    db.commit()

    return None