from sqlalchemy import select
from pydantic import ValidationError

from app.database import Session
from app.models import User
from app.schemas import UserSchema


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
    return True


def read_user(id: int) -> dict | None:
    stmt = select(User).where(User.id == id)
    with Session() as db:
        user = db.scalars(stmt).first()

    if not user:
        return None
    user = UserSchema.from_orm(user).__dict__
    user['rights'] = user['rights'].value
    return user
