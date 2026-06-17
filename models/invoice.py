from sqlalchemy import String, ForeignKey, Identity, Numeric, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from decimal import Decimal
from db.database import Base


class Invoice(Base):
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False)
    invoice_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    total_net: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    vat_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_amount : Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    invoice_lines: Mapped[list["InvoiceLine"]] = relationship("InvoiceLine", back_populates="invoice")

    def __repr__(self):
        return f"Invoice(id={self.id}, invoice_number={self.invoice_number}, repair_order_id={self.repair_order_id}, sale_id={self.sale_id}, invoice_date={self.invoice_date})"
    
class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    #tracking
    source_type: Mapped[str] = mapped_column(String(50), nullable=False)
    source_id: Mapped[int] = mapped_column(Integer, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="invoice_lines")

    def __repr__(self):
        return f"InvoiceLine(id={self.id}, invoice_id={self.invoice_id}, description={self.description}, quantity={self.quantity}, unit_price={self.unit_price}, total_amount={self.total_amount})"