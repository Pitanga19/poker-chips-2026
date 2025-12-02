from __future__ import annotations
from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as SAEnum
from typing import Optional, List, TYPE_CHECKING
from app.db.base_class import Base
from app.db.tables.hands.schemas import HandStreet

if TYPE_CHECKING:
    from app.db.tables.games.model import Game
    from app.db.tables.bet_rounds.model import BetRound
    from app.db.tables.pots.model import Pot

class Hand(Base):
    __tablename__ = 'hands'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('games.id', name='fk_hand_game_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    
    current_bet_round_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('bet_rounds.id', name='fk_hand_current_bet_round_id', ondelete='CASCADE'),
        index=True,
        nullable=True
    )
    
    street: Mapped[HandStreet] = mapped_column(
        SAEnum(HandStreet, name='hand_street'),
        nullable=False,
        default=HandStreet.PRE_FLOP
    )
    dealer_position: Mapped[int] = mapped_column(Integer, nullable=False)
    need_small_blind: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    need_big_blind: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relaciones
    game: Mapped['Game'] = relationship(
        'Game',
        back_populates='hands',
        foreign_keys=[game_id]
    )
    bet_rounds: Mapped[List['BetRound']] = relationship(
        'BetRound',
        back_populates='hand',
        foreign_keys='BetRound.hand_id',
        primaryjoin='Hand.id==BetRound.hand_id',
        cascade='all, delete'
    )
    current_bet_round: Mapped[Optional['BetRound']] = relationship(
        'BetRound',
        foreign_keys=[current_bet_round_id],
        primaryjoin='Hand.current_bet_round_id==BetRound.id',
        uselist=False
    )
    pots: Mapped[List['Pot']] = relationship(
        'Pot',
        back_populates='hand',
        cascade='all, delete'
    )
