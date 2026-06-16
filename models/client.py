from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity, String
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import ClientBike
    from models import Sale

class Client(Base):
    __tablename__ = "clients"
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    bikes: Mapped[list["ClientBike"]] = relationship("ClientBike", back_populates="client")
    sales: Mapped[list["Sale"]] = relationship("Sale", back_populates="client")

    def __repr__(self):
        return f"Client(id={self.id}, last_name={self.last_name}, first_name={self.first_name}, phone={self.phone}, email={self.email})"