from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.tables.model import Table

class Game(Base):
    __tablename__ = 'games'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    table_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tables.id', name='fk_game_table_id'),
        index=True,
        unique=True,
        nullable=False
    )
    
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    
    # Relaciones
    table: Mapped['Table'] = relationship('Table', back_populates='game', uselist=False)
