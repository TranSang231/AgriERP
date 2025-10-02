from typing import List
from .base import Const

class ResponseMessages(Const):
    CREATED = "{0} created"
    UPDATED = "{0} updated"
    DELETED = "{0} deleted"

    @classmethod
    def get_response_message(cls, message: str, params: List[str] = []) -> str:
        return message.format(*params)
