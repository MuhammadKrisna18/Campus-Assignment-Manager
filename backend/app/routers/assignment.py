from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.assignment import Assignment
from app.models.course import Course
from app.models.user import User

from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentResponse
)

from app.routers.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/assignments",
    tags=["Assignments"]
)

VALID_PRIORITIES = ["low", "medium", "high"]


def _to_response(assignment, course):
    return {
        "id": assignment.id,
        "course_id": assignment.course_id,
        "course_name": course.course_name,
        "title": assignment.title,
        "due_date": assignment.due_date,
        "priority": assignment.priority,
        "status": assignment.status
    }


@router.post(
    "/",
    response_model=AssignmentResponse
)
def create_assignment(
    payload: AssignmentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    # Pastikan mata kuliah milik user
    course = (
        db.query(Course)
        .filter(
            Course.id == payload.course_id,
            Course.user_id == current_user.id
        )
        .first()
    )

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

    if payload.priority not in VALID_PRIORITIES:
        raise HTTPException(
            status_code=400,
            detail="Priority tidak valid"
        )

    assignment = Assignment(
        user_id=current_user.id,
        course_id=payload.course_id,
        title=payload.title,
        due_date=payload.due_date,
        priority=payload.priority,
        status="pending"
    )

    db.add(assignment)
    db.commit()
    db.refresh(assignment)

    return _to_response(assignment, course)


@router.get(
    "/",
    response_model=list[AssignmentResponse]
)
def get_my_assignments(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    results = (
        db.query(Assignment, Course)
        .join(
            Course,
            Assignment.course_id == Course.id
        )
        .filter(
            Assignment.user_id == current_user.id
        )
        .all()
    )

    return [
        _to_response(assignment, course)
        for assignment, course in results
    ]


@router.patch(
    "/{assignment_id}/complete",
    response_model=AssignmentResponse
)
def mark_complete(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    assignment = (
        db.query(Assignment)
        .filter(
            Assignment.id == assignment_id,
            Assignment.user_id == current_user.id
        )
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    assignment.status = "completed"

    db.commit()
    db.refresh(assignment)

    course = (
        db.query(Course)
        .filter(
            Course.id == assignment.course_id
        )
        .first()
    )

    return _to_response(assignment, course)


@router.delete(
    "/{assignment_id}",
    status_code=204
)
def delete_assignment(
    assignment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    assignment = (
        db.query(Assignment)
        .filter(
            Assignment.id == assignment_id,
            Assignment.user_id == current_user.id
        )
        .first()
    )

    if not assignment:
        raise HTTPException(
            status_code=404,
            detail="Assignment not found"
        )

    db.delete(assignment)
    db.commit()

    return None
