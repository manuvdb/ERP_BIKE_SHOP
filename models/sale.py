from db.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Identity, Integer, ForeignKey
from datetime import datetime, timezone
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import InventoryBike
    from models import SparePart
    from models import Client

class Sale(Base):
    __tablename__ = "sales"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("clients.id"), nullable=False)
    sale_date: Mapped[datetime] = mapped_column(nullable=False, default=lambda: datetime.now(timezone.utc))

    client: Mapped["Client"] = relationship("Client", back_populates="sales")
    sale_lines_bikes: Mapped[list["SaleLineBike"]] = relationship("SaleLineBike", back_populates="sale")
    sale_lines_parts: Mapped[list["SaleLinePart"]] = relationship("SaleLinePart", back_populates="sale")

    def __repr__(self):
        return f"Sale(id={self.id}, client_id={self.client_id}, sale_date={self.sale_date})"

class SaleLineBike(Base):
    __tablename__ = "sale_lines_bikes"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), nullable=False)
    bike_inventory_id: Mapped[int] = mapped_column(ForeignKey("inventory_bikes.id"), nullable= False)
    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    sale: Mapped["Sale"] = relationship("Sale", back_populates="sale_lines_bikes")
    bike: Mapped["InventoryBike"] = relationship("InventoryBike", back_populates="sale_lines")

    def __repr__(self):
        return f"SaleLineBike(id={self.id}, sale_id={self.sale_id}, bike_inventory_id={self.bike_inventory_id}, quantity_sold={self.quantity_sold})"

class SaleLinePart(Base):
    __tablename__ = "sale_lines_parts"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    sale_id: Mapped[int] = mapped_column(ForeignKey("sales.id"), nullable=False)
    spare_part_id: Mapped[int] = mapped_column(ForeignKey("spare_parts.id"), nullable= False)
    quantity_sold: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    sale: Mapped["Sale"] = relationship("Sale", back_populates="sale_lines_parts")
    spare_part: Mapped["SparePart"] = relationship("SparePart", back_populates="sale_lines")

    def __repr__(self):
        return f"SaleLinePart(id={self.id}, sale_id={self.sale_id}, spare_part_id={self.spare_part_id}, quantity_sold={self.quantity_sold})"
