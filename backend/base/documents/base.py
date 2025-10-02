from abc import abstractmethod
from django_opensearch_dsl import Document

class BaseDocument(Document):
    """All Search document classes have to extend this class and implement it methods."""
    @classmethod
    @abstractmethod
    def get_query_set(self):
        pass  # No implementation in the abstract base class