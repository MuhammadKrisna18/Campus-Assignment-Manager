from pydantic import BaseModel
from datetime import date
from datetime import time

class CourseCreate(BaseModel):
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str
    day: str
    schedule_date: date
    schedule_time: time


class CourseResponse(BaseModel):
    id: int
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str
    day: str
    schedule_date: date
    schedule_time: time

    class Config:
        from_attributes = True