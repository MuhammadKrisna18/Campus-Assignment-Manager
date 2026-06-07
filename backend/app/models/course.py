from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    course_name = Column(
        String,
        nullable=False
    )

    credits = Column(
        Integer,
        nullable=False
    )

    class_name = Column(
        String,
        nullable=False
    )

    lecturer_name = Column(
        String,
        nullable=False
    )
    
    grade = Column(
        String,
        nullable=True
    )

    semester = Column(
        Integer,
        nullable=True
    )
