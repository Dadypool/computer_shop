from sqlalchemy import select
from pydantic import ValidationError

from app.database import Session
from app.models import Product
from app.schemas import Productcreate


def create_product(product: dict) -> bool:
    try:
        product = Productcreate(**product)
    except ValidationError:
        return False

    db_product = Product(**product.dict())
    with Session() as db:
        db.add(db_product)
        db.commit()
        db.refresh(db_product)
    return True


def read_product_by_id(id: int) -> dict | None:
    stmt = select(Product).where(Product.id == id)
    with Session() as db:
        product = db.scalars(stmt).first()

    if not product:
        return None

    product = Productcreate.from_orm(product).__dict__
    product['category'] = product['category'].value
    return product


def read_product_by_category(category: str) -> list[dict]:
    stmt = select(Product).where(Product.category == category)
    with Session() as db:
        products = db.scalars(stmt).all()
    return [Productcreate.from_orm(product).__dict__ for product in products]
