"""
Gender schema
"""
from enum import Enum


class Gender(str, Enum):
    """
    Gender class that inherits from built-in Enum
    """
    MALE: str = 'MALE'
    FEMALE: str = 'FEMALE'
    OTHER: str = 'OTHER'
