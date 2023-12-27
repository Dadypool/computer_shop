from sqlalchemy import select
from pydantic import ValidationError

from app.database.sqlalchemy import Session
from app.database.models import User, Order, OrderStatus, Product
from app.database.schemas import OrderCreate, OrderSchema, ProductSchema


def create_cart(user_id: int) -> bool:
    with Session() as db:
        db_cart= Order(user_id=user_id, status=OrderStatus.cart)
        db.add(db_cart)
        db.commit()
        db.refresh(db_cart)
    return True


def create_order(user_id: int) -> bool:
    cart = read_cart_by_user_id(user_id)
    with Session() as db:
        db_order = db.get(Order, cart["id"])
        for product in db_order.products:
            db_product = db.get(Product, product.id)
            db_product.status = "ordered"
        db_order.status = "created"
        db.commit()
    create_cart(user_id)
    return True


def read_cart_by_user_id(user_id: int) -> list[dict]:
    stmt = select(Order).where(Order.user_id == user_id).where(Order.status == OrderStatus.cart)
    with Session() as db:
        cart = db.scalars(stmt).first()
    return OrderSchema.from_orm(cart).__dict__


def read_active_orders(user_id: int) -> list[dict]:
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .where(
            Order.status == Order.status.created
            or Order.status == Order.status.confirmed
            or Order.status == Order.status.shipped
        )
    )
    with Session() as db:
        orders = db.scalars(stmt).all()
    return [OrderSchema.from_orm(order).__dict__ for order in orders]


def read_order_by_id(id: int) -> dict | None:
    stmt = select(Order).where(Order.id == id)
    with Session() as db:
        order = db.scalars(stmt).first()
    if not order:
        return None
    return OrderSchema.from_orm(order).__dict__


def read_orders_by_user_id(user_id: int) -> list[dict]:
    stmt = select(Order).where(Order.user_id == user_id).where(Order.status != OrderStatus.cart)
    with Session() as db:
        orders = db.scalars(stmt).all()
    return [OrderSchema.from_orm(order).__dict__ for order in orders]


def read_created_orders() -> list[dict]:
    stmt = (
        select(Order)
        .where(Order.status == OrderStatus.created)
        .order_by(Order.created_at)
    )
    with Session() as db:
        orders = db.scalars(stmt).all()
    return [OrderSchema.from_orm(order).__dict__ for order in orders]


def read_confirmed_orders() -> list[dict]:
    stmt = (
        select(Order)
        .where(Order.status == OrderStatus.confirmed)
        .order_by(Order.updated_at)
    )
    with Session() as db:
        orders = db.scalars(stmt).all()
    return [OrderSchema.from_orm(order).__dict__ for order in orders]


def read_products_by_order_id(order_id: int) -> list[dict]:
    stmt = select(Product).where(Product.order_id == order_id)
    with Session() as db:
        products = db.scalars(stmt).all()
    return [ProductSchema.from_orm(product).__dict__ for product in products]


def read_products_in_cart_by_user_id(user_id: int) -> list[dict]:
    cart = read_cart_by_user_id(user_id)
    return read_products_by_order_id(cart["id"])


def read_order_price(order_id: int) -> int:
    stmt = select(Order).where(Order.id == order_id)
    with Session() as db:
        order = db.scalars(stmt).first()
        if not order:
            return 0
        price = 0
        for product in order.products:
            price += product.price
    return price


def update_order_status(order_id: int, new_status: OrderStatus) -> bool:
    with Session() as db:
        order = db.get(Order, order_id)
        if not order or order.status == "cart":
            return False
        order.status = new_status
        if new_status == "confirmed":
            for product in order.products:
                product.status = "ordered"
        elif new_status == "closed":
            for product in order.products:
                product.status = "sold"
        db.commit()
    return True


def delete_order(id: int) -> bool:
    with Session() as db:
        order = db.get(Order, id)
        if not order:
            return False
        db.delete(order)
        db.commit()
    return True
