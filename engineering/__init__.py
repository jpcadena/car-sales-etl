"""
Engineering package initialization
"""
import logging

import pandas as pd
from numpy import uint16, uint8
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import AsyncSession

from core import logging_config
from core.config import settings
from db.session import get_session
from engineering.extraction import extract_raw_data
from engineering.loading import loading
from engineering.transformation import cast_column, remove_missing_values, \
    convert_date_column, create_sale_year, create_categorical_model, \
    convert_column_names, strip_columns

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
    dataframe: pd.DataFrame = extract_raw_data(filename, gender_column)
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
    dataframe = strip_columns(dataframe)
    dataframe = cast_column(dataframe)
    dataframe = remove_missing_values(dataframe)
    dataframe = convert_date_column(dataframe)
    dataframe = create_sale_year(dataframe)
    dataframe = create_categorical_model(dataframe)
    dataframe = convert_column_names(dataframe)
    dataframe = cast_column(dataframe, 'purchase_year', uint16)
    dataframe = cast_column(dataframe, 'buyer_age', uint8)
    return dataframe


async def load_to_db(dataframe: pd.DataFrame) -> bool:
    """
    Loading data from dataframe into Car table
    :param dataframe: Dataframe with cars sales information
    :type dataframe: pd.DataFrame
    :return: True if the rows were inserted; otherwise false
    :rtype: bool
    """
    logger.info("Running load_to_db()")
    session: AsyncSession = await get_session()
    cars_inserted: bool = await loading(dataframe, session)
    return cars_inserted


def load_with_pandas(dataframe: pd.DataFrame) -> bool:
    """
    Loading data from dataframe into Car table using Pandas API
    :param dataframe: Dataframe with cars sales information
    :type dataframe: pd.DataFrame
    :return: True if the rows were inserted; otherwise false
    :rtype: bool
    """
    url: str = f"postgresql+psycopg://{settings.POSTGRES_USER}:" \
               f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_SERVER}/" \
               f"{settings.POSTGRES_DB}"
    engine: Engine = create_engine(url)
    with engine.begin() as connection:
        try:
            rows_inserted: int = dataframe.to_sql(
                'car',
                connection,
                index=False)
            print(rows_inserted)
        except Exception as exc:
            logger.error(exc)
            return False
    return True
