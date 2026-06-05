from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import ForeignKey

from app.core.database import Base


class Schedule(Base):
    __tablename__ = "schedules"

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

    subject = Column(
        String,
        nullable=False
    )

    day = Column(
        String,
        nullable=False
    )

    room = Column(
        String,
        nullable=False
    )

    start_time = Column(
        Time,
        nullable=False
    )

    end_time = Column(
        Time,
        nullable=False
    )
