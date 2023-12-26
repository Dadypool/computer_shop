from sqlalchemy import select
from pydantic import ValidationError

from app.database.sqlalchemy import Session
from app.database.models import Order, OrderStatus
from app.database.schemas import OrderCreate


def create_order(order: dict) -> bool:
    try:
        order = OrderCreate(**order)
    except ValidationError:
        return False

    db_order = Order(**order.dict())
    with Session() as db:
        db.add(db_order)
        db.commit()
        db.refresh(db_order)
    return True


def read_active_orders(user_id: int) -> list[dict]:
    stmt = select(Order).where(Order.user_id == user_id).where(Order.status == Order.status.created or Order.status == Order.status.confirmed or Order.status == Order.status.shipped)
    with Session() as db:
        orders = db.scalars(stmt).all()
    return orders


def read_order_by_id(id: int) -> dict | None:
    stmt = select(Order).where(Order.id == id)
    with Session() as db:
        order = db.scalars(stmt).first()

    if not order:
        return None

    return order


def read_orders_by_user_id(user_id: int) -> list[dict]:
    stmt = select(Order).where(Order.user_id == user_id)
    with Session() as db:
        orders = db.scalars(stmt).all()
    return orders


def update_order_status(id: int, new_status: OrderStatus) -> bool:
    with Session() as db:
        order = db.get(Order, id)
        if not order:
            return False
        order.status = new_status
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