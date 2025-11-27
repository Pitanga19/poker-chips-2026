from sqlalchemy import UniqueConstraint, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Player(Base):
    __tablename__ = 'players'
    __table_args__ = (
        UniqueConstraint('user_id', 'room_id', name='uq_user_room'),
        {'extend_existing': True},
    )
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('users.id', name='fk_player_user_id'),
        index=True,
        nullable=False
    )
    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rooms.id', name='fk_player_room_id'),
        index=True,
        nullable=False
    )
    # Datos dinámicos del jugador en esta room
    stack: Mapped[int] = mapped_column(Integer, default=0)

    # Relaciones
    user = relationship('User', back_populates='players')
    room = relationship('Room', back_populates='players')
