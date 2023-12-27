from sqlalchemy import select
from pydantic import ValidationError

from app.database.sqlalchemy import Session
from app.database.models import User
from app.database.schemas import UserSchema
from app.database.crud.order import create_cart

def create_user(user: dict) -> bool:
    try:
        user = UserSchema(**user)
    except ValidationError:
        return False

    db_user = User(**user.dict())
    with Session() as db:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
    if db_user.rights.value == "user":
        create_cart(db_user.id)

    return True


def read_user(id: int) -> dict | None:
    stmt = select(User).where(User.id == id)
    with Session() as db:
        user = db.scalars(stmt).first()

    if not user:
        return None
    user = UserSchema.from_orm(user).__dict__
    user["rights"] = user["rights"].value
    return user


def delete_user(id: int) -> bool:
    with Session() as db:
        user = db.get(User, id)
        if not user:
            return False
        db.delete(user)
        db.commit()
    return True
