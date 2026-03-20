from datetime import date, datetime
from decimal import Decimal
from sqlalchemy import String, Numeric, Date, ForeignKey, Text, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class LearningResult(Base):
    __tablename__ = "learning_result"
    student_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("student.code"),
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
    subject_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("subject.code"),
        primary_key=True
    )

    score_id: Mapped[str] = mapped_column(
        String(20),
        ForeignKey("score.code"),
        primary_key=True
    )
    score_value: Mapped[Decimal] = mapped_column(Numeric(4, 2), nullable=False)
    comment: Mapped[str | None] = mapped_column(String(256))
    test_date: Mapped[date] = mapped_column(Date, nullable=False)
    note: Mapped[str | None] = mapped_column(Text)

@event.listens_for(LearningResult, "before_insert")
@event.listens_for(LearningResult, "before_update")
def validate(mapper, connection, target):
    if not target.student_id:
        raise ValueError("learning result's student id cannot be empty")
    if not target.class_id:
        raise ValueError("learning result's class id cannot be empty")
    if not target.academic_year_id:
        raise ValueError("learning result's academic year id cannot be empty")
    if not target.semester_id:
        raise ValueError("learning result's semester id cannot be empty")
    if not target.subject_id:
        raise ValueError("learning result's subject id cannot be empty")
    if not target.score_id:
        raise ValueError("learning result's score id cannot be empty")
    if not target.score_value:
        raise ValueError("learning result's score value cannot be empty")
    if not target.test_date:
        raise ValueError("learning result's test date cannot be empty")
    try:
        if not isinstance(target.test_date, date):
            datetime.strptime(target.test_date, "%Y-%m-%d")
    except ValueError:
        raise ValueError("learning result's test date must be in format YYYY-MM-DD")