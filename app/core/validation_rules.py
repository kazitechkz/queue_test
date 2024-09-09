import re

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
TWELVE_DIGITS_REGEX = re.compile(r"^\d{12}$")
PHONE_REGEX = re.compile(r"^\+7\(\d{3}\) \d{3}-\d{2}-\d{2}$")