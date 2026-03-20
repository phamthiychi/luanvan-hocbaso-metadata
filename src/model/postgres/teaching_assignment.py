from sqlalchemy import String, Integer, ForeignKey, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class TeachingAssignment(Base):
    __tablename__ = "teaching_assignment"
    teacher_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("teacher.code"),
        primary_key=True
    )
    class_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("class_room.code"),
        primary_key=True
    )
    subject_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("subject.code"),
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
    role: Mapped[str] = mapped_column(String(30), nullable=False)
    periods_per_week: Mapped[int] = mapped_column(Integer, nullable=False)
    note: Mapped[str | None] = mapped_column(Text)

@event.listens_for(TeachingAssignment, "before_insert")
@event.listens_for(TeachingAssignment, "before_update")
def validate(mapper, connection, target):
    if not target.teacher_id:
        raise ValueError("teaching assignment's teacher id cannot be empty")
    if not target.class_id:
        raise ValueError("teaching assignment's class id cannot be empty")
    if not target.subject_id:
        raise ValueError("teaching assignment's subject id cannot be empty")
    if not target.academic_year_id:
        raise ValueError("teaching assignment's academic year id cannot be empty")
    if not target.semester_id:
        raise ValueError("teaching assignment's semester id cannot be empty")
    if not target.role:
        raise ValueError("teaching assignment's role cannot be empty")
    if not target.periods_per_week:
        raise ValueError("teaching assignment's periods per week cannot be empty")
    if target.periods_per_week <= 0:
        print(target.periods_per_week)
        raise ValueError("teaching assignment's periods per week must be greater than 0")