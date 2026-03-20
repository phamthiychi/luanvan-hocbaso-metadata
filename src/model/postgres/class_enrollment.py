from datetime import date, datetime
from sqlalchemy import String, Date, ForeignKey, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class ClassEnrollment(Base):
    __tablename__ = "class_enrollment"
    student_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("student.code"),
        primary_key=True
    )
    grade_level_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("grade_level.code"),
        primary_key=True
    )
    class_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("class_room.code"),
        primary_key=True
    )
    academic_year_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("academic_year.code"),
        primary_key=True
    )
    semester_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("semester.code"),
        primary_key=True
    )
    enrollment_date: Mapped[date] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(Text)

@event.listens_for(ClassEnrollment, "before_insert")
@event.listens_for(ClassEnrollment, "before_update")
def validate(mapper, connection, target):
    if not target.student_id:
        raise ValueError("class enrollment's student id cannot be empty")
    if not target.grade_level_id:
        raise ValueError("class enrollment's grade level id cannot be empty")
    if not target.class_id:
        raise ValueError("class enrollment's class id cannot be empty")
    if not target.academic_year_id:
        raise ValueError("class enrollment's academic year id cannot be empty")
    if not target.semester_id:
        raise ValueError("class enrollment's semester id cannot be empty")
    if not target.enrollment_date:
        raise ValueError("class enrollment's enrollment date cannot be empty")
    try:
        if not isinstance(target.enrollment_date, date):
            datetime.strptime(target.enrollment_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("class enrollment's enrollment date must be in format YYYY-MM-DD")