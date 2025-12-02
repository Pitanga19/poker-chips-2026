from __future__ import annotations
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from app.db.base_class import Base

if TYPE_CHECKING:
    from app.db.tables.users.model import User
    from app.db.tables.tables.model import Table
    from app.db.tables.players.model import Player
    from app.db.tables.room_settings.model import RoomSettings
class Room(Base):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    hoster_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', name='fk_room_hoster_id', ondelete='CASCADE'),
        index=True,
        nullable=False
    )
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    # Relaciones
    hoster: Mapped['User'] = relationship('User', back_populates='hosted_rooms')
    tables: Mapped[List['Table']] = relationship(
        'Table', back_populates='room',
        cascade='all, delete'
    )
    players: Mapped[List['Player']] = relationship(
        'Player', back_populates='room',
        cascade='all, delete'
    )
    room_settings: Mapped[Optional['RoomSettings']] = relationship(
        'RoomSettings', back_populates='room', uselist=False, cascade='all, delete'
    )
