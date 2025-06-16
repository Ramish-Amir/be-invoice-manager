from sqlalchemy import Column, Float, ForeignKey, Integer, String
from datetime import datetime
from app.db.database import Base
from sqlalchemy.orm import relationship


class InvoiceService(Base):
    __tablename__ = "invoice_services"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    price = Column(Float)

    invoice_id = Column(Integer, ForeignKey("invoices.id", ondelete="CASCADE"))
    invoice = relationship(
        "Invoice",
        back_populates="services",
    )
