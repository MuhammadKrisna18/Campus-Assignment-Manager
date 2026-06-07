from pydantic import BaseModel
from datetime import date


class AssignmentCreate(BaseModel):
    course_id: int
    title: str
    due_date: date
    priority: str


class AssignmentUpdate(BaseModel):
    title: str
    due_date: date
    priority: str


class AssignmentResponse(BaseModel):
    id: int
    course_id: int
    course_name: str
    title: str
    due_date: date
    priority: str
    status: str

    class Config:
        from_attributes = True
