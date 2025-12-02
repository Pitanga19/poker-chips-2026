from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional, List, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.tables.model import Table
    from app.db.tables.hands.model import Hand

class Game(Base):
    __tablename__ = 'games'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tables.id', name='fk_game_table_id', ondelete='CASCADE'),
        index=True,
        unique=True,
        nullable=False
    )
    current_hand_id: Mapped[Optional[int]] = mapped_column(
        Integer,
        ForeignKey('hands.id', name='fk_game_current_hand_id', ondelete='CASCADE'),
        index=True,
        nullable=True
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relaciones
    table: Mapped['Table'] = relationship('Table', back_populates='game', uselist=False)
    hands: Mapped[List['Hand']] = relationship(
        'Hand',
        back_populates='game',
        cascade='all, delete',
        foreign_keys='Hand.game_id'
    )
    current_hand: Mapped[Optional['Hand']] = relationship(
        'Hand',
        foreign_keys=[current_hand_id],
        uselist=False
    )
