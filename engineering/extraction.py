"""
Extraction script for Engineering module
"""
import pandas as pd
from numpy import float16, float32

from core.persistence_manager import PersistenceManager
from schema.gender import Gender


def extraction(
        filename: str, gender_column: str, parse_dates: list[str] | None = None
) -> pd.DataFrame:
    """
    Engineering method to extract raw data from csv file
    :param filename: Filename to extract data from
    :type filename: str
    :param gender_column: Name of gender column
    :type gender_column: str
    :param parse_dates: List of date columns to parse
    :type parse_dates: list[str]
    :return: Dataframe with raw data
    :rtype: pd.DataFrame
    """
    d_types: dict = {
        'Buyer Gender': str, 'Color': str, 'Make': str, 'New Car': bool,
        'Buyer Age': int, 'Discount': float16, 'Sale Price': float32}
    mapping: dict[str, str] = {
        'Male': Gender.MALE.value, 'Agender': Gender.OTHER.value,
        'Female': Gender.FEMALE.value, 'Non-binary': Gender.OTHER.value,
        'Genderqueer': Gender.OTHER.value, 'Polygender': Gender.OTHER.value,
        'Genderfluid': Gender.OTHER.value, 'Bigender': Gender.OTHER.value}

    def convert_gender(gender: str):
        """
        Convert a gender by grouping less common into Other
        :param gender: Gender to convert
        :type gender: str
        :return: Gender converted
        :rtype: str
        """
        return mapping.get(gender, Gender.OTHER.value)

    if not parse_dates:
        parse_dates = ['Purchase Date']
    converters: dict = {gender_column: convert_gender}
    dataframe: pd.DataFrame = PersistenceManager.load_from_csv(
        filename=filename, dtypes=d_types, parse_dates=parse_dates,
        converters=converters)
    return dataframe
