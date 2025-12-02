from __future__ import annotations
from sqlalchemy import UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.users.model import User
    from app.db.tables.rooms.model import Room
    from app.db.tables.seats.model import Seat

class Player(Base):
    __tablename__ = 'players'
    __table_args__ = (
        UniqueConstraint('user_id', 'room_id', name='uq_user_room'),
        {'extend_existing': True},
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', name='fk_player_user_id'),
        index=True,
        nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rooms.id', name='fk_player_room_id'),
        index=True,
        nullable=False
    )
    
    # Datos dinámicos del jugador en esta room
    stack: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relaciones
    user: Mapped['User'] = relationship('User', back_populates='players')
    room: Mapped['Room'] = relationship('Room', back_populates='players')
    seat: Mapped[Optional['Seat']] = relationship('Seat', back_populates='player', uselist=False)
