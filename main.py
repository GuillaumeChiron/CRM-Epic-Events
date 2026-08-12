from database.database import engine
from models.base import Base

# Ces imports enregistrent les tables dans Base.metadata
from models.user import User
from models.client import Client
from models.contract import Contract
from models.event import Event


def create_tables() -> None:
    Base.metadata.create_all(bind=engine)
    print("Tables MySQL créées avec succès.")


if __name__ == "__main__":
    create_tables()
