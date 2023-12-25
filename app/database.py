from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.models import Base

sync_engine = create_engine(
    url=settings.DATABASE_URL_psycopg,
    echo=False,
)

Session = sessionmaker(sync_engine)


def create_tables():
    sync_engine.echo = False
    Base.metadata.drop_all(sync_engine)
    Base.metadata.create_all(sync_engine)
    sync_engine.echo = True


if __name__ == "__main__":
    create_tables()
