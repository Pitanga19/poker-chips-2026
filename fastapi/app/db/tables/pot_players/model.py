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

class PotPlayer(Base):
    __tablename__ = 'pot_players'
    __table_args__ = (
        UniqueConstraint('pot_id', 'player_id', name='uq_pot_player'),
        {'extend_existing': True},
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    pot_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('pots.id', name='fk_pot_player_pot_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    player_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('players.id', name='fk_pot_player_player_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    
    # Relaciones
    pot: Mapped[Pot] = relationship('Pot', back_populates='pot_players')
    player: Mapped[Player] = relationship('Player')
