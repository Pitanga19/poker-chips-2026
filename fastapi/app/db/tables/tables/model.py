from __future__ import annotations
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.rooms.model import Room
    from app.db.tables.seats.model import Seat
    from app.db.tables.games.model import Game

class Table(Base):
    __tablename__ = 'tables'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rooms.id', name='fk_table_room_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    
    # Relaciones
    room: Mapped['Room'] = relationship('Room', back_populates='tables')
    seats: Mapped[List['Seat']] = relationship(
        'Seat',
        back_populates='table',
        cascade='all, delete'
    )
    
    # relación 1:1 opcional con Game
    game: Mapped[Optional['Game']] = relationship('Game', back_populates='table', uselist=False)
