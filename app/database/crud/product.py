from sqlalchemy import select
from pydantic import ValidationError

from app.database.sqlalchemy import Session
from app.database.models import Product, ProductStatus
from app.database.schemas import ProductSchema, ProductCategory, ProductCreate
from app.database.crud.order import read_cart_by_user_id, read_products_by_order_id


def create_product(product: dict) -> bool:
    try:
        product = ProductCreate(**product)
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


def read_free_product_by_name(name: str) -> dict | None:
    stmt = (
        select(Product)
        .where(Product.name == name)
        .where(Product.status == ProductStatus.free)
    )
    with Session() as db:
        product = db.scalars(stmt).first()
    if not product:
        return None
    return ProductSchema.from_orm(product).__dict__


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


def update_add_product_to_cart(user_id: int, product_id: int) -> bool:
    with Session() as db:
        product = db.get(Product, product_id)
        if not product:
            return False
        product.order_id = read_cart_by_user_id(user_id)["id"]
        product.status = "reserved"
        db.commit()
    return True


def update_remove_product_from_cart(user_id: int, product_id: int) -> bool:
    with Session() as db:
        product = db.get(Product, product_id)
        if not product:
            return False
        product.order_id = None
        product.status = "free"
        db.commit()
    return True


def delete_product(id: int) -> bool:
    with Session() as db:
        product = db.get(Product, id)
        if not product:
            return False
        if product.status in ("ordered", "sold"):
            return False
        db.delete(product)
        db.commit()
    return True
