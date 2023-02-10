"""
Engineering package initialization
"""
import logging

import pandas as pd
from numpy import uint16, uint8
from sqlalchemy.ext.asyncio import AsyncSession

from core import logging_config
from db.session import get_session
from engineering.extraction import extraction
from engineering.loading import loading
from engineering.transformation import cast_column, remove_missing_values, \
    convert_date_column, create_sale_year, create_categorical_model, \
    convert_column_names

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


def extract_data(
        filename: str = 'raw_data.csv') -> pd.DataFrame:
    """
    Abstract extract data function
    :param filename: Filename to extract data from
    :type filename: str
    :return: Dataframe with raw data
    :rtype: pd.DataFrame
    """
    gender_column: str = "Buyer Gender"
    logger.info("Running extract_data()")
    dataframe: pd.DataFrame = extraction(filename, gender_column)
    return dataframe


def transform_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Transform dataframe based on the requirements
    :param dataframe: Raw dataframe
    :type dataframe: pd.DataFrame
    :return: Transformed dataframe
    :rtype: pd.DataFrame
    """
    logger.info("Running transform_data()")
    dataframe = cast_column(dataframe)
    dataframe = remove_missing_values(dataframe)
    dataframe = convert_date_column(dataframe)
    dataframe = create_sale_year(dataframe)
    dataframe = create_categorical_model(dataframe)
    dataframe = cast_column(dataframe, 'Purchase Year', uint16)
    dataframe = cast_column(dataframe, 'Buyer Age', uint8)
    dataframe = convert_column_names(dataframe)
    return dataframe


async def load_data(dataframe: pd.DataFrame) -> bool:
    """
    Loading data from dataframe into Car table
    :param dataframe: Dataframe with cars sales information
    :type dataframe: pd.DataFrame
    :return: True if the rows were inserted; otherwise false
    :rtype: bool
    """
    logger.info("Running load_data()")
    session: AsyncSession = await get_session()
    cars_inserted: bool = await loading(dataframe, session)
    return cars_inserted
