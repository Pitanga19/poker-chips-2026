from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional
from app.db.base_class import Base

class RoomSettings(Base):
    __tablename__ = 'room_settings'
    __table_args__ = {'extend_existing': True}

    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rooms.id', name='fk_room_settings_room_id'),
        index=True,
        unique=True,
        nullable=False
    )
    use_default_buy_in: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    buy_in: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    big_blind_value: Mapped[int] = mapped_column(Integer, nullable=False)
    small_blind_value: Mapped[int] = mapped_column(Integer, nullable=False)
    min_stack_bb: Mapped[int] = mapped_column(Integer, nullable=False)
    max_stack_bb: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    # Relaciones
    room = relationship('Room', back_populates='room_settings')
