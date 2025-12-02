from __future__ import annotations
from sqlalchemy import UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base_class import Base
from app.db.tables.pots.model import Pot
from app.db.tables.players.model import Player

if TYPE_CHECKING:
    from app.db.tables.pots.model import Pot
    from app.db.tables.players.model import Player

class PotWinner(Base):
    __tablename__ = 'pot_winners'
    __table_args__ = (
        UniqueConstraint('pot_id', 'winner_id', name='uq_pot_winner'),
        {'extend_existing': True},
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    pot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('pots.id', name='fk_pot_winner_pot_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    winner_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('players.id', name='fk_pot_winner_winner_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    
    amount_won: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Relaciones
    pot: Mapped[Pot] = relationship('Pot', back_populates='pot_winners')
    winner: Mapped[Player] = relationship('Player')
