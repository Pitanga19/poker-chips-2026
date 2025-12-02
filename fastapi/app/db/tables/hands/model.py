from __future__ import annotations
from sqlalchemy import Integer, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM as SAEnum
from typing import TYPE_CHECKING
from app.db.base_class import Base
from app.db.tables.hands.schemas import HandStreet

if TYPE_CHECKING:
    from app.db.tables.games.model import Game

class Hand(Base):
    __tablename__ = 'hands'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    game_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('games.id', name='fk_hand_game_id'),
        index=True,
        nullable=False
    )
    
    street: Mapped[HandStreet] = mapped_column(
        SAEnum(HandStreet, name='hand_street'),
        nullable=False,
        default=HandStreet.PRE_FLOP,
    )
    dealer_position: Mapped[int] = mapped_column(Integer, nullable=False)
    need_small_blind: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    need_big_blind: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    
    # Relaciones
    game: Mapped['Game'] = relationship('Game', back_populates='hands')
