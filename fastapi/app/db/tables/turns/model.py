from __future__ import annotations
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as SAEnum
from typing import Optional, TYPE_CHECKING
from app.db.base_class import Base
from app.db.utils.enums import ActionType

if TYPE_CHECKING:
    from app.db.tables.bet_rounds.model import BetRound
    from app.db.tables.players.model import Player

class Turn(Base):
    __tablename__ = 'turns'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    bet_round_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('bet_rounds.id', name='fk_turn_bet_round_id', ondelete='CASCADE'),
        index=True, nullable=False,
    )
    player_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('players.id', name='fk_turn_player_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    
    action: Mapped[ActionType] = mapped_column(
        SAEnum(ActionType, name='action_type'),
        nullable=False
    )
    amount: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    
    # Relaciones
    bet_round: Mapped['BetRound'] = relationship(
        'BetRound',
        back_populates='turns',
        foreign_keys=[bet_round_id],
        primaryjoin='Turn.bet_round_id==BetRound.id'
    )
    player: Mapped['Player'] = relationship('Player', back_populates='turns')
