from abc import ABC, abstractmethod


class BaseLoader(ABC):

    @abstractmethod
    def load(self):
        """
        Returns a list of benchmark samples.
        """
        pass