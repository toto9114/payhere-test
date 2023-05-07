import phonenumbers
import re


def validate_phone_number(phone_number: str) -> bool:
    try:
        parsed = phonenumbers.parse(phone_number, 'KR')
        return phonenumbers.is_valid_number(parsed)
    except phonenumbers.NumberParseException:
        return False


def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[a-zA-Z]', password):
        return False
    return True
