from pydantic import BaseModel, Field, ConfigDict

from app.models import Rights, Category

price_constr = Field(gt=0)
str_constr = Field(min_length=2, max_length=30)


class MyBaseModel(BaseModel):
    model_config: ConfigDict = ConfigDict(from_attributes=True)


class UserSchema(MyBaseModel):
    id: int
    name: str = str_constr
    rights: Rights = Rights.user


class Productcreate(MyBaseModel):
    name: str = str_constr
    price: int = price_constr
    category: Category
    manufacturer: str = str_constr
