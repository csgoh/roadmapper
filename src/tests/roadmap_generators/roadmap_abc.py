from abc import ABC, abstractmethod


class RoadmapABC(ABC):

    @abstractmethod
    def generate_and_save_as(self, file_name: str = "example.png"):
        pass

    @abstractmethod
    def generate(self):
        pass
