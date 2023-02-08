"""
Transformation script for Engineering module
"""
from typing import Any

import numpy as np
import pandas as pd
from numpy import uint16, uint8, float16

from core.config import settings


def cast_column(
        dataframe: pd.DataFrame, column: str = 'Buyer Gender',
        d_type: Any = 'category') -> pd.DataFrame:
    """
    Simple transformation of datatype for a column into category
    :param dataframe: Dataframe to transform
    :type dataframe: pd.DataFrame
    :param column: Dataframe column to cast
    :type column: str
    :param d_type: Data type to cast to
    :type d_type: Any
    :return: Converted dataframe
    :rtype: pd.DataFrame
    """
    dataframe[column] = dataframe[column].astype(d_type)
    return dataframe


def remove_missing_values(
        dataframe: pd.DataFrame, how_to_drop: str = "any") -> pd.DataFrame:
    """
    Remove missing values from the dataframe
    :param dataframe: Dirty dataframe to remove missing values from
    :type dataframe: pd.DataFrame
    :param how_to_drop: Way to drop row. any or all
    :type how_to_drop: str
    :return: Cleaned dataframe
    :rtype: pd.DataFrame
    """
    missing_values: pd.Series = (dataframe.isnull().sum())
    if len(missing_values) > 0:
        print(missing_values[missing_values > 0])
        print(missing_values[missing_values > 0] / dataframe.shape[0] * 100)
        dataframe.dropna(how=how_to_drop, inplace=True)
    return dataframe


def convert_date_column(
        dataframe: pd.DataFrame, date_column: str = "Purchase Date",
        date_format: str = "%Y-%m-%d"
) -> pd.DataFrame:
    """
    Convert a date column into a standard date format
    :param dataframe: DataFrame to convert its column
    :type dataframe: pd.DataFrame
    :param date_column: Name of dataframe date column to convert
    :type date_column: str
    :param date_format: Date format to use
    :type date_format: str
    :return: Converted dataframe with standard date format
    :rtype: pd.DataFrame
    """
    print("convert_date_column")
    dataframe[date_column] = pd.to_datetime(
        dataframe[date_column], format=date_format).dt.normalize()
    print(dataframe.dtypes)
    print(dataframe[date_column])
    return dataframe


def create_sale_year(
        dataframe: pd.DataFrame, new_column: str = 'Purchase Year',
        date_column: str = 'Purchase Date') -> pd.DataFrame:
    """
    Create a new column to store the year of the sale
    :param dataframe: Dataframe to manipulate
    :type dataframe: pd.DataFrame
    :param new_column: New column for year of the sale
    :type new_column: str
    :param date_column: Column of the sale date
    :type date_column: str
    :return: Updated Dataframe containing the year of the sale
    :rtype: pd.DataFrame
    """
    print("create sale year")
    dataframe[new_column] = dataframe[date_column].dt.year
    return dataframe


def create_categorical_model(
        dataframe: pd.DataFrame, model_column: str = 'Make') -> pd.DataFrame:
    """
    Create a new column to store the categorical model of the cars as
     numerical values
    :param dataframe: Dataframe to manipulate
    :type dataframe: pd.DataFrame
    :param model_column: Dataframe column to store the categorical model
    :type model_column: str
    :return: Updated Dataframe containing the new numerical columns
    :rtype: pd.DataFrame
    """
    make_counts = dataframe[model_column].value_counts()
    dataframe['Make_Frequency'] = dataframe[model_column].map(
        make_counts).astype(uint16)
    quantiles: list[float16] = np.linspace(
        0.00, 1.00, uint8(settings.NUM_BINS) + 1, dtype=float16)
    dataframe['Make_Classification'] = pd.qcut(
        dataframe['Make_Frequency'], q=quantiles,
        labels=settings.LABELS).astype("category")
    dataframe.drop([model_column, 'Make_Frequency'], axis=1, inplace=True)
    # Other option could be use Pandas Dummies or LabelTransformer
    # from Scikit-Learn
    car_model_map: dict[str, uint8] = {
        settings.LABELS[i]: i + 1 for i in range(len(settings.LABELS))}
    dataframe['Make_Classification'] = dataframe[
        'Make_Classification'].replace(car_model_map).astype(uint8)
    return dataframe
