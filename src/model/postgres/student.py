from datetime import date, datetime
from sqlalchemy import String, Date, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class Student(Base):
    __tablename__ = "student"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    card_id: Mapped[str | None] = mapped_column(String(20))
    edu_id: Mapped[str | None] = mapped_column(String(20))
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    gender: Mapped[str] = mapped_column(String(10), nullable=False)
    ethnicity: Mapped[str] = mapped_column(String(20), nullable=False)
    status: Mapped[str | None] = mapped_column(String(30))
    phone: Mapped[str | None] = mapped_column(String(15))
    nationality: Mapped[str] = mapped_column(String(50), nullable=False)
    address: Mapped[str | None] = mapped_column(Text)
    father_name: Mapped[str | None] = mapped_column(String(100))
    father_job: Mapped[str | None] = mapped_column(String(50))
    father_phone: Mapped[str | None] = mapped_column(String(15))
    father_card_id: Mapped[str | None] = mapped_column(String(20))
    mother_name: Mapped[str | None] = mapped_column(String(100))
    mother_job: Mapped[str | None] = mapped_column(String(50))
    mother_phone: Mapped[str | None] = mapped_column(String(15))
    mother_card_id: Mapped[str | None] = mapped_column(String(20))
    guardian_name: Mapped[str | None] = mapped_column(String(100))
    guardian_job: Mapped[str | None] = mapped_column(String(50))
    guardian_phone: Mapped[str | None] = mapped_column(String(15))
    guardian_card_id: Mapped[str | None] = mapped_column(String(20))
    place_of_birth: Mapped[str | None] = mapped_column(Text)

@event.listens_for(Student, "before_insert")
@event.listens_for(Student, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("student's code cannot be empty")
    if not target.name:
        raise ValueError("student's name cannot be empty")
    if not target.date_of_birth:
        raise ValueError("student's date of birth cannot be empty")
    try:
        if not isinstance(target.date_of_birth, date):
            datetime.strptime(target.date_of_birth, "%Y-%m-%d")
    except ValueError:
        raise ValueError("student's date of birth must be in format YYYY-MM-DD")
    if not target.gender:
        raise ValueError("student's gender cannot be empty")
    if not target.ethnicity:
        raise ValueError("student's ethnicity cannot be empty")
    if not target.nationality:
        raise ValueError("student's nationality cannot be empty")