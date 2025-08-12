from abc import abstractmethod, ABC
from typing import Optional
from src.thufir.abstractions.provider import Provider
from src.thufir.abstractions.repository import Repository


class Manager(ABC):

    def __init__(self, repository: Repository, provider: Optional[Provider] = None):
        self.provider = provider
        self.repository = repository
