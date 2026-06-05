from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.course import Course
from app.models.user import User

from app.schemas.course import (
    CourseCreate,
    CourseResponse
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

    course = Course(
        user_id=current_user.id,
        course_name=payload.course_name,
        credits=payload.credits,
        class_name=payload.class_name,
        lecturer_name=payload.lecturer_name
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