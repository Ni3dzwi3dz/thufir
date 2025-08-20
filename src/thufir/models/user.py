from src.thufir.models.base_model import ThufirModel
from src.thufir.database.models.user import User as DBUser


class User(ThufirModel):
    _db_model = DBUser

    id: int
    email: str
    name: str
    password_hash: str
