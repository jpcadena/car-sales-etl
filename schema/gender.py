"""
Gender schema
"""
from enum import Enum


class Gender(str, Enum):
    """
    Gender class that inherits from built-in Enum
    """
    MALE: str = 'Male'
    FEMALE: str = 'Female'
    OTHER: str = 'Other'
