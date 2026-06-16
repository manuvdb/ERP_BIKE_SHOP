from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, Identity, String, Numeric, Integer, DateTime
from decimal import Decimal
from datetime import datetime, timezone
from db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from models import RepairOrderPart, ClientBike, SparePart

class RepairOrder(Base):
    __tablename__ = "repair_orders"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    client_bike_id: Mapped[int] = mapped_column(ForeignKey("client_bikes.id"), nullable=False)
    issue_description: Mapped[str | None] = mapped_column(String(100), nullable=True)
    labor_hours: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    labor_hourly_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    quote_status: Mapped[str] = mapped_column(String(20), nullable=False, default="pending")
    repair_status: Mapped[str] = mapped_column(String(20), nullable=False, default="to do")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    client_bike: Mapped["ClientBike"] = relationship("ClientBike", back_populates="repair_orders")
    repair_order_parts: Mapped[list["RepairOrderPart"]] = relationship("RepairOrderPart", back_populates="repair_order")

    def __repr__(self):
        return f"RepairOrder(id={self.id}, client_id={self.client_bike_id}, quote_status={self.quote_status}, repair_status={self.repair_status})"
    
class RepairOrderPart(Base):
    __tablename__ = "repair_order_parts"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    repair_order_id: Mapped[int] = mapped_column(ForeignKey("repair_orders.id"), nullable=False)
    spare_part_id: Mapped[int] = mapped_column(ForeignKey("spare_parts.id"), nullable=False)
    quantity_used: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

    repair_order: Mapped["RepairOrder"] = relationship("RepairOrder", back_populates="repair_order_parts")
    spare_part: Mapped["SparePart"] = relationship("SparePart", back_populates="repair_lines")

    def __repr__(self):
        return f"RepairOrderPart(id={self.id}, repair_order_id={self.repair_order_id}, spare_part_id={self.spare_part_id}, quantity_used={self.quantity_used})"