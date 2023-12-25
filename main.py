from app.crud.user import create_user, read_user
from app.crud.product import (
    create_product,
    read_product_by_id,
    read_product_by_category,
    update_product_status,
    update_product_price
)
from app.database import create_tables


def _create_tables():
    create_tables()


def _create_user():
    form_data = {"id": 1, "name": "Dan", "rights": "seller"}
    res = create_user(form_data)
    print(res)


def _read_user():
    return read_user(1)


def _create_product():
    products_data = [
        {
            "name": "Intel Core i7",
            "price": 300,
            "category": "processor",
            "manufacturer": "Intel",
        },
        {
            "name": "AMD Ryzen 5",
            "price": 250,
            "category": "processor",
            "manufacturer": "AMD",
        },
        {
            "name": "NVIDIA GeForce RTX 3080",
            "price": 800,
            "category": "graphics card",
            "manufacturer": "NVIDIA",
        },
        {
            "name": "Corsair Vengeance LPX",
            "price": 100,
            "category": "ram",
            "manufacturer": "Corsair",
        },
        {
            "name": "Seagate Barracuda",
            "price": 80,
            "category": "hdd",
            "manufacturer": "Seagate",
        },
        {
            "name": "EVGA 750 B5",
            "price": 120,
            "category": "power supply",
            "manufacturer": "EVGA",
        },
        {"name": "NZXT H510", "price": 90, "category": "block", "manufacturer": "NZXT"},
    ]

    for product in products_data:
        create_product(product)


def _read_product():
    print(read_product_by_category("block"))


def _update_product_status():
    update_product_status(1, "reserved")


def _update_product_price():
    update_product_price({"name": "NZXT H510", "price": 90, "category": "block", "manufacturer": "NZXT"}, 100)


if __name__ == "__main__":
    _update_product_price()
