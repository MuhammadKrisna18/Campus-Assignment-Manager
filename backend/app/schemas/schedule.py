from pydantic import BaseModel
from datetime import time


class ScheduleCreate(BaseModel):
    subject: str
    day: str
    room: str
    start_time: time
    end_time: time


class ScheduleResponse(BaseModel):
    id: int
    subject: str
    day: str
    room: str
    start_time: time
    end_time: time

    class Config:
        from_attributes = True
