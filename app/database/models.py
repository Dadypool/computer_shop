import datetime
import enum
from typing import Annotated, Optional

from sqlalchemy import ForeignKey, String, text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

intpk = Annotated[int, mapped_column(primary_key=True)]
created_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
    ),
]
updated_at = Annotated[
    datetime.datetime,
    mapped_column(
        server_default=text("TIMEZONE('utc', now())"),
        onupdate=datetime.datetime.utcnow,
    ),
]
str_256 = Annotated[str, 256]


class Base(DeclarativeBase):
    type_annotation_map = {str_256: String(256)}

    repr_cols_num = 3
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class Rights(enum.Enum):
    user = "user"
    seller = "seller"
    admin = "admin"


class Category(enum.Enum):
    cpu = "cpu"
    gpu = "gpu"
    ram = "ram"
    hdd = "hdd"
    ps = "ps"
    block = "block"


class ProductStatus(enum.Enum):
    free = "free"
    reserved = "reserved"
    ordered = "ordered"
    sold = "sold"


class OrderStatus(enum.Enum):
    cart = "cart"
    created = "created"
    confirmed = "confirmed"
    canceled = "canceled"
    shipped = "shipped"
    cloes = "closed"


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]

    name: Mapped[str]

    rights: Mapped[Rights] = mapped_column(default=Rights.user)

    orders: Mapped[list["Order"]] = relationship(
        back_populates="user",
    )


class Product(Base):
    __tablename__ = "product"

    id: Mapped[intpk]

    name: Mapped[str]

    price: Mapped[int]

    category: Mapped[Category]

    manufacturer: Mapped[str]

    status: Mapped[ProductStatus] = mapped_column(default=ProductStatus.free)

    order_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("order.id", ondelete="CASCADE")
    )

    order: Mapped["Order"] = relationship(
        back_populates="products",
    )


class Order(Base):
    __tablename__ = "order"

    id: Mapped[intpk]

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    status: Mapped[OrderStatus] = mapped_column(default=OrderStatus.created)

    created_at: Mapped[created_at]

    updated_at: Mapped[updated_at]

    user: Mapped[User] = relationship(
        back_populates="orders",
    )

    products: Mapped[list["Product"]] = relationship(
        back_populates="order",
    )
