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
    ScheduleResponse,
    ScheduleUpdate
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

    # Validasi jam
    if payload.end_time <= payload.start_time:
        raise HTTPException(
            status_code=400,
            detail="Jam selesai harus setelah jam mulai"
        )

    # ==========================
    # VALIDASI BENTROK JADWAL
    # ==========================

    existing_schedules = (
        db.query(Schedule)
        .filter(
            Schedule.user_id == current_user.id,
            Schedule.day == payload.day,
        )
        .all()
    )

    for existing in existing_schedules:

        overlap = (
            payload.start_time < existing.end_time
            and payload.end_time > existing.start_time
        )

        if overlap:

            existing_course = (
                db.query(Course)
                .filter(
                    Course.id == existing.course_id
                )
                .first()
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Jadwal bentrok dengan "
                    f"{existing_course.course_name} "
                    f"({existing.start_time} - "
                    f"{existing.end_time})"
                )
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

    return _to_response(
        schedule,
        course
    )

@router.put(
    "/{schedule_id}",
    response_model=ScheduleResponse
)
def update_schedule(
    schedule_id: int,
    payload: ScheduleUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id,
            Schedule.user_id == current_user.id
        )
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )

    if payload.end_time <= payload.start_time:
        raise HTTPException(
            status_code=400,
            detail="Jam selesai harus setelah jam mulai"
        )

    existing_schedules = (
        db.query(Schedule)
        .filter(
            Schedule.user_id == current_user.id,
            Schedule.day == payload.day,
            Schedule.id != schedule_id
        )
        .all()
    )

    for existing in existing_schedules:

        overlap = (
            payload.start_time < existing.end_time
            and payload.end_time > existing.start_time
        )

        if overlap:

            existing_course = (
                db.query(Course)
                .filter(
                    Course.id == existing.course_id
                )
                .first()
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    f"Jadwal bentrok dengan "
                    f"{existing_course.course_name} "
                    f"({existing.start_time} - "
                    f"{existing.end_time})"
                )
            )

    schedule.day = payload.day
    schedule.room = payload.room
    schedule.start_time = payload.start_time
    schedule.end_time = payload.end_time

    db.commit()
    db.refresh(schedule)

    course = (
        db.query(Course)
        .filter(
            Course.id == schedule.course_id
        )
        .first()
    )

    return _to_response(
        schedule,
        course
    )

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


@router.delete(
    "/{schedule_id}",
    status_code=204
)
def delete_schedule(
    schedule_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(
        get_current_user
    )
):

    schedule = (
        db.query(Schedule)
        .filter(
            Schedule.id == schedule_id,
            Schedule.user_id == current_user.id
        )
        .first()
    )

    if not schedule:
        raise HTTPException(
            status_code=404,
            detail="Schedule not found"
        )

    db.delete(schedule)
    db.commit()

    return None