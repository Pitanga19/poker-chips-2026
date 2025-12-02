from __future__ import annotations
from sqlalchemy import UniqueConstraint, Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.tables.model import Table
    from app.db.tables.players.model import Player

class Seat(Base):
    __tablename__ = 'seats'
    __table_args__ = (
        UniqueConstraint('table_id', 'position', name='uq_table_position'),
        UniqueConstraint('table_id', 'player_id', name='uq_table_player'),
        {'extend_existing': True},
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('tables.id', name='fk_seat_table_id'), index=True, nullable=False
    )
    player_id: Mapped[Optional[int]] = mapped_column(
        Integer, ForeignKey('players.id', name='fk_seat_player_id'), index=True, nullable=True
    )
    vacate: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    position: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Relaciones
    table: Mapped['Table'] = relationship('Table', back_populates='seats')
    player: Mapped[Optional['Player']] = relationship(
        'Player',
        back_populates='seat',
        uselist=False
    )
