from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Identity, String, Numeric, Integer
from decimal import Decimal
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import SaleLinePart

class SparePart(Base):
    __tablename__ = "spare_parts"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    ean_code: Mapped[str | None] = mapped_column(String(13), unique= True, nullable=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    category: Mapped[str] = mapped_column(String(50), nullable=False)
    purchase_price_net: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    retail_price_net: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quantity_in_stock: Mapped[int] = mapped_column(Integer, nullable=False, default=0)

    sale_lines: Mapped[list["SaleLinePart"]] = relationship("SaleLinePart", back_populates="spare_part")

    def __repr__(self):
        return f"SparePart(id={self.id}, name={self.name}, category={self.category})"