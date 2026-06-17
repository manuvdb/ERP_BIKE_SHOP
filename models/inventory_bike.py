from sqlalchemy import String, ForeignKey, Identity, Numeric, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from decimal import Decimal
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import SaleLineBike

class InventoryBike(Base):
    __tablename__ = "inventory_bikes"
    
    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    ean_code: Mapped[str | None] = mapped_column(String(13), unique= True, nullable=True)
    brand: Mapped[str | None] = mapped_column(String(50), nullable=True)
    model: Mapped[str | None] = mapped_column(String(50), nullable=True)
    type: Mapped[str] = mapped_column(String(50), nullable=False)
    color: Mapped[str] = mapped_column(String(20), nullable=False)
    frame_size: Mapped[str | None] = mapped_column(String(10), nullable=True)
    purchase_price_net: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    retail_price_net: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    frame_number: Mapped[str | None] = mapped_column(String(100), unique=True, nullable=True)

    sale_lines: Mapped[list["SaleLineBike"]] = relationship("SaleLineBike", back_populates="bike")

    def __repr__(self):
        return f"InventoryBike(id={self.id}, type={self.type}, color={self.color})"