from sqlalchemy import String, Integer, event
from sqlalchemy.orm import Mapped, mapped_column

from src.model.postgres.base import Base

class ClassRoom(Base):
    __tablename__ = "class_room"
    code: Mapped[str] = mapped_column(String(20), primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False)
    special_program: Mapped[str | None] = mapped_column(String(50))

@event.listens_for(ClassRoom, "before_insert")
@event.listens_for(ClassRoom, "before_update")
def validate(mapper, connection, target):
    if not target.code:
        raise ValueError("class's code cannot be empty")
    if not target.name:
        raise ValueError("class's name cannot be empty")
    if target.size is None:
        raise ValueError("class's size cannot be empty")
    if target.size <= 0:
        raise ValueError("class's size must be greater than 0")
