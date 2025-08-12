from abc import abstractmethod, ABC
from src.thufir.abstractions.manager import Manager


class API(ABC):

    def __init__(self, manager: Manager):
        self.manager = manager
