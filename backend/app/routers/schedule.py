from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.schedule import Schedule
from app.models.course import Course
from app.models.user import User

from app.schemas.schedule import (
    ScheduleCreate,
    ScheduleResponse
)

from app.routers.auth import (
    get_current_user
)

router = APIRouter(
    prefix="/schedules",
    tags=["Schedules"]
)


def _to_response(schedule, course):
    return {
        "id": schedule.id,
        "course_id": schedule.course_id,
        "course_name": course.course_name,
        "day": schedule.day,
        "room": schedule.room,
        "start_time": schedule.start_time,
        "end_time": schedule.end_time
    }


@router.post(
    "/",
    response_model=ScheduleResponse
)
def create_schedule(
    payload: ScheduleCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    # Pastikan course milik user yang login
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

    schedule = Schedule(
        user_id=current_user.id,
        course_id=payload.course_id,
        day=payload.day,
        room=payload.room,
        start_time=payload.start_time,
        end_time=payload.end_time
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return _to_response(schedule, course)


@router.get(
    "/",
    response_model=list[ScheduleResponse]
)
def get_my_schedules(
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    results = (
        db.query(Schedule, Course)
        .join(
            Course,
            Schedule.course_id == Course.id
        )
        .filter(
            Schedule.user_id == current_user.id
        )
        .all()
    )

    return [
        _to_response(schedule, course)
        for schedule, course in results
    ]
