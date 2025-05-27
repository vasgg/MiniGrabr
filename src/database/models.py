from datetime import UTC, datetime

from sqlalchemy import BigInteger, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from bot.internal.enums import OrderStatus, UserType


class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(UTC))


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, nullable=False, unique=True, primary_key=True)
    username: Mapped[str | None] = mapped_column(String(32))
    fullname: Mapped[str]
    balance: Mapped[int] = mapped_column(default=0)
    mode: Mapped[UserType] = mapped_column(default=UserType.CUSTOMER)

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, username={self.username!r})"

    def __repr__(self):
        return str(self)


class Order(Base):
    __tablename__ = "orders"

    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    traveler_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.DRAFT)
    description: Mapped[str | None] = mapped_column(String(2083))
    name: Mapped[str | None]
    from_where: Mapped[str | None]
    to: Mapped[str | None]
    when: Mapped[str | None]
    size: Mapped[str | None]
    weight: Mapped[str | None]
    price: Mapped[str | None]

    traveler: Mapped["User"] = relationship(
        "User", foreign_keys=traveler_id, backref="orders_as_traveler", lazy=False
    )
    customer: Mapped["User"] = relationship(
        "User", foreign_keys=customer_id, backref="orders_as_customer", lazy=False
    )

    def __str__(self):
        return f"{self.__class__.__name__}(id={self.id}, customer_id={self.customer_id!r}, status={self.status!r})"


class Application(Base):
    __tablename__ = "applications"
    __table_args__ = (UniqueConstraint("order_id", "traveler_id"),)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id", ondelete="CASCADE"))
    customer_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    traveler_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    completion_days: Mapped[int | None] = mapped_column()
    message: Mapped[str | None] = mapped_column(String(2083))
    is_active: Mapped[bool] = mapped_column(default=True)

    order: Mapped["Order"] = relationship(
        "Order", foreign_keys=[order_id], backref="applications", lazy=False
    )
    traveler: Mapped["User"] = relationship(
        "User", foreign_keys=[traveler_id], backref="applications", lazy=False
    )
