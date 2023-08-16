from abc import ABC, abstractmethod
from typing import List

class KeywordSearchService(ABC):
    @abstractmethod
    def get_list(self, query: str) -> List[str]:
        pass