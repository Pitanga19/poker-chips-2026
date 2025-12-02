from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.hands.model import Hand

class Pot(Base):
    __tablename__ = 'pots'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hand_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('hands.id', name='fk_pot_hand_id'),
        index=True,
        nullable=False
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    size: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    
    # Relaciones
    hand: Mapped['Hand'] = relationship('Hand', back_populates='pots')
