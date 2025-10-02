import re
from uuid import UUID

class StringUtil():
    @staticmethod
    def convert_to_int(string):
        try:
            number = int(string)
        except ValueError:
            number = 0
        return number

    @staticmethod
    def is_valid_uuid(uuid_to_test, version=4):
        try:
            _ = UUID(uuid_to_test, version=version)
            return True
        except ValueError:
            return False

    @staticmethod
    def remove_local_characters(text: str):
        text = re.sub(r"[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]", "A", text)
        text = re.sub(r"[àáạảãâầấậẩẫăằắặẳẵ]", "a", text)
        text = re.sub(r"[èéẹẻẽêềếệểễ]", "e", text)
        text = re.sub(r"[ÈÉẸẺẼÊỀẾỆỂỄ]", "E", text)
        text = re.sub(r"[òóọỏõôồốộổỗơờớợởỡ]", "o", text)
        text = re.sub(r"[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]", "O", text)
        text = re.sub(r"[ìíịỉĩ]", "i", text)
        text = re.sub(r"[ÌÍỊỈĨ]", "I", text)
        text = re.sub(r"[ùúụủũưừứựửữ]", "u", text)
        text = re.sub(r"[ƯỪỨỰỬỮÙÚỤỦŨ]", "U", text)
        text = re.sub(r"[ỳýỵỷỹ]", "y", text)
        text = re.sub(r"[ỲÝỴỶỸ]", "Y", text)
        text = re.sub(r"[Đ]", "D", text)
        text = re.sub(r"[đ]", "d", text)
        return text

    @staticmethod
    def get_id(input_id):
        return input_id.hex if isinstance(input_id, UUID) else str(input_id)
