import base64
from os.path import join
from django.conf import settings

class FileUtils:
    @classmethod
    def image_to_base64(cls, file_path) -> str:
        """Converts image to base64 string"""
        try:
            with open(file_path, 'rb') as f:
                data = base64.b64encode(f.read())
                f.close()
                str_data = file_str = data.decode('utf-8')
                return f'data:image/svg+xml;base64, {str_data}'
        except:
            return None
        
    @classmethod
    def get_base64_svg_logo(cls):
        logo_path = join(settings.BASE_DIR, "oauth", "static", "logo.svg")
        return cls.image_to_base64(logo_path)
