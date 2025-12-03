from __future__ import annotations
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.hands.model import Hand
    from app.db.tables.turns.model import Turn

class BetRound(Base):
    __tablename__ = 'bet_rounds'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('hands.id', name='fk_bet_round_hand_id', ondelete='CASCADE'),
        index=True, nullable=False
    )
    
    # FK a Turn actual (nullable)
    last_turn_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('turns.id', name='fk_bet_round_last_turn_id'),
        nullable=True
    )
    
    # posición (seat.position) del jugador que tiene el turno actualmente, null hasta que arranque
    current_turn_position: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    current_max_bet: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    current_min_raise: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    
    # Relaciones
    hand: Mapped['Hand'] = relationship(
        'Hand',
        back_populates='bet_rounds',
        foreign_keys=[hand_id],
        primaryjoin='BetRound.hand_id==Hand.id'
    )
    last_turn: Mapped[Optional['Turn']] = relationship(
        'Turn',
        foreign_keys=[last_turn_id],
        primaryjoin='BetRound.last_turn_id==Turn.id',
        uselist=False
    )
    turns: Mapped[List['Turn']] = relationship(
        'Turn',
        back_populates='bet_round',
        foreign_keys='Turn.bet_round_id',
        primaryjoin='BetRound.id==Turn.bet_round_id',
        cascade='all, delete'
    )
