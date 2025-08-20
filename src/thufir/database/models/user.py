from src.thufir.database.models.base import Base


class User(Base):
    id: int
    email: str
    name: str
    password_hash: str
