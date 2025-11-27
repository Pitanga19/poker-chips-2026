from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Room(Base):
    __tablename__ = 'rooms'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    hoster_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', name='fk_room_hoster_id'),
        index=True,
        nullable=False
    )
    
    # Relaciones
    hoster = relationship('User', back_populates='hosted_rooms')
    tables = relationship('Table', back_populates='room', cascade='all, delete')
    players = relationship('Player', back_populates='room', cascade='all, delete')
