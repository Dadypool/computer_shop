from datetime import datetime

from pydantic import BaseModel, Field, ConfigDict

from app.database.models import Rights, Category, OrderStatus

price_constr = Field(gt=0)
str_constr = Field(min_length=2, max_length=30)


class MyBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class UserSchema(MyBaseModel):
    id: int
    name: str = str_constr
    rights: Rights = Rights.user


class ProductCategory(MyBaseModel):
    name: str = str_constr
    price: int = price_constr
    manufacturer: str = str_constr

class ProductCreate(ProductCategory):
    category: Category

class ProductSchema(ProductCreate):
    id: int


class OrderCreate(MyBaseModel):
    user_id: int
    products: list[ProductSchema]


class OrderSchema(MyBaseModel):
    id: int
    user_id: int
    status: OrderStatus
    created_at: datetime
    updated_at: datetime
