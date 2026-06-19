from sqlalchemy import String, ForeignKey, Identity, Numeric, Integer, DateTime, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime, timezone
from decimal import Decimal
from db.database import Base


class Invoice(Base):
    """
    En-tête de facture uniquement. Une Invoice ne pointe PAS directement vers
    une Sale ou un RepairOrder : elle peut regrouper plusieurs origines
    (ex: vente d'un vélo + d'un casque + une réparation) via ses InvoiceLine,
    qui portent chacune leur propre origine (sale_id ou repair_order_id).
    """
    __tablename__ = "invoices"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_number: Mapped[str] = mapped_column(String(50), nullable=False, unique=True)
    invoice_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))
    total_net: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    vat_rate: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    vat_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    invoice_lines: Mapped[list["InvoiceLine"]] = relationship(
        "InvoiceLine", back_populates="invoice", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return (
            f"Invoice(id={self.id}, invoice_number={self.invoice_number}, "
            f"invoice_date={self.invoice_date}, total_amount={self.total_amount})"
        )


class InvoiceLine(Base):
    """
    Chaque ligne porte DEUX informations polymorphes indépendantes :

    1. article_type / article_id : QUEL article a été vendu
       -> "inventory_bike" (un vélo du stock) ou "spare_part" (une pièce, ex: casque)

    2. origin_type / origin_id : DE QUELLE transaction ça vient
       -> "sale" (vente directe) ou "repair_order" (réparation, ex: pièce
          utilisée + main d'oeuvre facturée au client)

    C'est ce qui permet à une seule Invoice de regrouper, par exemple,
    la vente d'un vélo + d'un casque ET une réparation sur un seul document.
    """
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    invoice_id: Mapped[int] = mapped_column(ForeignKey("invoices.id"), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    quantity: Mapped[int] = mapped_column(Integer, nullable=False)
    unit_price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    article_type: Mapped[str] = mapped_column(String(50), nullable=False)  # "inventory_bike" | "spare_part"
    article_id: Mapped[int] = mapped_column(Integer, nullable=False)

    origin_type: Mapped[str] = mapped_column(String(20), nullable=False)  # "sale" | "repair_order"
    origin_id: Mapped[int] = mapped_column(Integer, nullable=False)

    invoice: Mapped["Invoice"] = relationship("Invoice", back_populates="invoice_lines")

    def __repr__(self):
        return (
            f"InvoiceLine(id={self.id}, invoice_id={self.invoice_id}, "
            f"description={self.description}, quantity={self.quantity}, "
            f"unit_price={self.unit_price}, total_amount={self.total_amount}, "
            f"article_type={self.article_type}, origin_type={self.origin_type})"
        )