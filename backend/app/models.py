
from datetime import datetime, timezone

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


def utc_now():
    return datetime.now(timezone.utc)


class Order(Base):
    __tablename__ = "orders"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    order_id: Mapped[str] = mapped_column(
        String(40), unique=True, index=True
    )
    customer_email: Mapped[str] = mapped_column(
        String(255), index=True
    )
    status: Mapped[str] = mapped_column(String(40))
    estimated_delivery: Mapped[str | None] = mapped_column(
        String(20), nullable=True
    )


class SupportTicket(Base):
    __tablename__ = "support_tickets"

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True
    )
    ticket_id: Mapped[str] = mapped_column(
        String(40), unique=True, index=True
    )
    issue: Mapped[str] = mapped_column(Text)
    customer_email: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    status: Mapped[str] = mapped_column(
        String(30), default="open"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utc_now
    )
