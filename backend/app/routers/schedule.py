from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.schedule import Schedule
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

    schedule = Schedule(
        user_id=current_user.id,
        subject=payload.subject,
        day=payload.day,
        room=payload.room,
        start_time=payload.start_time,
        end_time=payload.end_time
    )

    db.add(schedule)
    db.commit()
    db.refresh(schedule)

    return schedule


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

    schedules = (
        db.query(Schedule)
        .filter(
            Schedule.user_id == current_user.id
        )
        .all()
    )

    return schedules
