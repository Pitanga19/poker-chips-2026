from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base_class import Base

class Table(Base):
    __tablename__ = 'tables'
    __table_args__ = {'extend_existing': True}
    
    id: Mapped[int] = mapped_column(primary_key=True)
    room_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('rooms.id', name='fk_table_room_id'),
        index=True,
        nullable=False
    )
    
    # Relaciones
    room = relationship('Room', back_populates='tables')
    seats = relationship('Seat', back_populates='table', cascade='all, delete')
