from sqlalchemy import select
from pydantic import ValidationError

from app.database import Session
from app.models import Product, ProductStatus
from app.schemas import ProductSchema, ProductCategory


def create_product(product: dict) -> bool:
    try:
        product = ProductSchema(**product)
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

    product = ProductSchema.from_orm(product).__dict__
    product["category"] = product["category"].value
    return product


def read_product_by_category(category: ProductCategory) -> list[dict]:
    with Session() as db:
        products = db.execute(
            select(Product.name, Product.price, Product.manufacturer)
            .distinct()
            .where(Product.status == ProductStatus.free)
            .where(Product.category == category)
        ).all()
    return [ProductCategory.from_orm(product).__dict__ for product in products]


def update_product_status(id: int, new_status: ProductStatus) -> bool:
    with Session() as db:
        product = db.get(Product, id)
        if not product:
            return False
        product.status = new_status
        db.commit()
    return True


def update_product_price(product: ProductSchema, new_price: int) -> bool:
    with Session() as db:
        products = db.get(Product, product).all()
        if not products:
            return False
        for product in products:
            product.price = new_price
        db.commit()
    return True


def delete_product(id: int) -> bool:
    with Session() as db:
        product = db.get(Product, id)
        if not product:
            return False
        db.delete(product)
        db.commit()
    return True
