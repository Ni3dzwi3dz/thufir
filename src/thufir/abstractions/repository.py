from abc import abstractmethod, ABC
from src.thufir.abstractions.database import Database


class Repository(ABC):

    def __init__(self, database: Database):
        self.database = database
