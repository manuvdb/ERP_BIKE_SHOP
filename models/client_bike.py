from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Identity, String
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import Client

class ClientBike(Base):
    __tablename__ = "client_bikes"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    brand: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model: Mapped[str | None] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    serial_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)

    client: Mapped["Client"] = relationship("Client", back_populates="bikes")
    repair_orders: Mapped[list["RepairOrder"]] = relationship("RepairOrder", back_populates="client_bike")

    def __repr__(self):
        return f"ClientBike(id={self.id}, client_id={self.client_id}, type={self.type}, color={self.color})"