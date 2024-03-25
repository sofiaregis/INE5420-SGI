from abc import ABC, abstractmethod

class GraphicalObject(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def draw(self):
        pass
