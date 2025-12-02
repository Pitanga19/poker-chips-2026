from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from app.db.base_class import Base

class Room(Base):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True}
    id: Mapped[int] = mapped_column(primary_key=True)
    hoster_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False
    )
    code: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    
    # Relaciones
    hoster: Mapped['User'] = relationship('User', back_populates='hosted_rooms')
    tables: Mapped[List['Table']] = relationship(
        'Table', back_populates='room',
        cascade='all, delete-orphan'
    )
    players: Mapped[List['Player']] = relationship(
        'Player', back_populates='room',
        cascade='all, delete-orphan'
    )
    room_settings: Mapped[Optional['RoomSettings']] = relationship(
        'RoomSettings', back_populates='room', uselist=False, cascade='all, delete-orphan'
    )
