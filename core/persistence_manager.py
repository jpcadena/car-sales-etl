"""
Persistence script for Core module.
This script provides methods to save and load dataframes to and from
 CSV and pickle files, respectively.
"""
import logging
from enum import Enum

import pandas as pd
from pandas import NaT
from pandas.io.parsers import TextFileReader

from core import logging_config
from core.config import settings

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


class DataType(str, Enum):
    """
    Data Type class based on Enum
    """
    RAW: str = 'data/raw/'
    PROCESSED: str = 'data/processed/'
    FIGURES: str = 'reports/figures/'


class PersistenceManager:
    """
    Persistence Manager class.
    Defines the different data types that can be saved and loaded.
    """

    @staticmethod
    def save_to_csv(
            dataframe: pd.DataFrame, data_type: DataType = DataType.PROCESSED,
            filename: str = 'processed_data.csv') -> bool:
        """
        Save dataframe as csv file
        :param dataframe: DataFrame to save
        :type dataframe: pd.DataFrame
        :param data_type: Path where data will be saved
        :type data_type: DataType
        :param filename: name of the file
        :type filename: str
        :return: True if the csv file was created; otherwise false
        :rtype: bool
        """
        if len(dataframe) == 0:
            return False
        if not settings.ENCODING:
            raise AttributeError("Encoding is not set.")
        dataframe.to_csv(f'{data_type.value}{filename}', index=False,
                         encoding=settings.ENCODING)
        logger.info("Dataframe saved to csv")
        return True

    @staticmethod
    def load_from_csv(
            filename: str = 'raw_data.csv',
            data_type: DataType = DataType.RAW,
            chunk_size: int = settings.CHUNK_SIZE, dtypes: dict = None,
            parse_dates: list[str] = None, converters: dict = None
    ) -> pd.DataFrame:
        """
        Load dataframe from CSV using chunk scheme
        :param filename: name of the file including extension
        :type filename: str
        :param data_type: Path where data will be saved
        :type data_type: DataType
        :param chunk_size: Number of chunks to split dataset
        :type chunk_size: int
        :return: Dataframe retrieved from CSV after optimization with chunks
        :rtype: pd.DataFrame
        """
        filepath: str = f'{data_type.value}{filename}'
        if not settings.ENCODING:
            raise AttributeError("Encoding is not set.")
        text_file_reader: TextFileReader = pd.read_csv(
            filepath, sep=', ', header=0, chunksize=chunk_size,
            encoding=settings.ENCODING, parse_dates=parse_dates,
            converters=converters, na_values=[NaT, 'nan', '', ' '])
        dataframe: pd.DataFrame = pd.concat(text_file_reader,
                                            ignore_index=True)
        for key, value in dtypes.items():
            if value in [float, int]:
                try:
                    dataframe[key] = pd.to_numeric(dataframe[key],
                                                   errors='coerce')
                    dataframe[key] = dataframe[key].astype(value)
                except Exception as exc:
                    logger.error(exc)
            else:
                try:
                    dataframe[key] = dataframe[key].astype(value)
                except Exception as exc:
                    logger.error(exc)
        logger.info("Dataframe loaded from csv")
        return dataframe

    @staticmethod
    def save_to_pickle(
            dataframe: pd.DataFrame, data_type: DataType = DataType.PROCESSED,
            filename: str = 'optimized_df.pkl') -> None:
        """
        Save dataframe to pickle file
        :param dataframe: Dataframe to save
        :type dataframe: pd.DataFrame
        :param data_type: Path where data will be saved
        :type data_type: DataType
        :param filename: Name of the file
        :type filename: str
        :return: None
        :rtype: NoneType
        """
        dataframe.to_pickle(f'{data_type.value}{filename}')
        logger.info("Dataframe saved to pickle")

    @staticmethod
    def load_from_pickle(
            data_type: DataType, filename: str = 'optimized_df.pkl'
    ) -> pd.DataFrame:
        """
        Load dataframe from Pickle file
        :param filename: Name of the file to search and load
        :type filename: str
        :param data_type: Path where data will be saved from Data Type
        :type data_type: DataType
        :return: Dataframe read from pickle
        :rtype: pd.DataFrame
        """
        dataframe: pd.DataFrame = pd.read_pickle(
            f'data/{data_type.value}/{filename}')
        logger.info("Dataframe loaded from pickle")
        return dataframe
