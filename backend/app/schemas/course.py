from pydantic import BaseModel


class CourseCreate(BaseModel):
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str


class CourseResponse(BaseModel):
    id: int
    course_name: str
    credits: int
    class_name: str
    lecturer_name: str

    class Config:
        from_attributes = True
