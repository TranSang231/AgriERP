from ..constants.phone import region_codes

class DataUtils:
    @classmethod
    def cast_to_int(cls, val, default=0):
        try:
            return int(val)
        except (ValueError, TypeError):
            return default
        
    @classmethod
    def format_phone_number(cls, phone, region):
        phone_string = f'{phone}'.strip()
        if phone_string.startswith('+'):
            return phone_string
        if len(phone_string) > 9 and not phone_string.startswith('0'):
            return f'+{phone_string}'

        region_code = region_codes.get(region, None)
        national_number = phone_string[1:] if phone_string.startswith('0') else phone_string
        if region_code is not None:
            return f'+{region_code}{national_number}'
        
        return phone
