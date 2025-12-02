from __future__ import annotations
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.hands.model import Hand

class BetRound(Base):
    __tablename__ = 'bet_rounds'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('hands.id', name='fk_bet_round_hand_id'),
        index=True, nullable=False
    )
    
    current_max_bet: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_min_raise: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # posición (seat.position) del jugador que tiene el turno actualmente, null hasta que arranque
    current_turn_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Relaciones
    hand: Mapped['Hand'] = relationship('Hand', back_populates='bet_rounds')
