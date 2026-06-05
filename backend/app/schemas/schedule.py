from pydantic import BaseModel
from datetime import time


class ScheduleCreate(BaseModel):
    course_id: int
    day: str
    room: str
    start_time: time
    end_time: time


class ScheduleResponse(BaseModel):
    id: int
    course_id: int
    course_name: str
    day: str
    room: str
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

class ScheduleUpdate(BaseModel):
    day: str
    room: str
    start_time: time
    end_time: time