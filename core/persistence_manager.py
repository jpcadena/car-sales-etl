"""
Persistence script for Core module
"""
from enum import Enum

import pandas as pd
from pandas import NaT
from pandas.io.parsers import TextFileReader

from core.config import settings


class DataType(str, Enum):
    """
    Data Type class based on Enum
    """
    RAW: str = 'data/raw/'
    PROCESSED: str = 'data/processed/'


class PersistenceManager:
    """
    Persistence Manager class
    """

    @staticmethod
    def save_to_csv(
            data: pd.DataFrame, data_type: DataType = DataType.PROCESSED,
            filename: str = 'processed_data.csv') -> bool:
        """
        Save dataframe as csv file
        :param data: DataFrame to save
        :type data: pd.DataFrame
        :param data_type: Path where data will be saved
        :type data_type: DataType
        :param filename: name of the file
        :type filename: str
        :return: True if the csv file was created; otherwise false
        :rtype: bool
        """
        dataframe: pd.DataFrame
        if isinstance(data, pd.DataFrame):
            dataframe = data
        else:
            if not data:
                return False
            dataframe = pd.DataFrame(data)
        dataframe.to_csv(f'{data_type.value}{filename}', index=False,
                         encoding=settings.ENCODING)
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
        text_file_reader: TextFileReader = pd.read_csv(
            filepath, header=0, chunksize=chunk_size,
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
                    print(exc)
            else:
                try:
                    dataframe[key] = dataframe[key].astype(value)
                except Exception as exc:
                    print(exc)
        return dataframe

    @staticmethod
    def save_to_pickle(
            dataframe: pd.DataFrame, data_type: DataType,
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
        dataframe.to_pickle(f'data/{data_type.value}/{filename}')

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
        return dataframe
