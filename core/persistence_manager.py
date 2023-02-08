"""
Persistence script for Core module
"""
import json
from enum import Enum

import pandas as pd
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
        Save list of dictionaries as csv file
        :param data: DataFrame to save
        :type data: pd.DataFrame
        :param data_type: folder where data will be saved from Data Type
        :type data_type: DataType
        :param filename: name of the file
        :type filename: str
        :return: confirmation for csv file created
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
            filename: str = 'Car Sales.csv',
            data_type: DataType = DataType.RAW,
            chunk_size: int = settings.CHUNK_SIZE, dtypes: dict = None,
            parse_dates: list[str] = None, converters: dict = None
    ) -> pd.DataFrame:
        """
        Load dataframe from CSV using chunk scheme
        :param filename: name of the file including extension
        :type filename: str
        :param data_type: folder where data will be saved from Data Type
        :type data_type: DataType
        :param chunk_size: Number of chunks to split dataset
        :type chunk_size: int
        :return: dataframe retrieved from CSV after optimization with chunks
        :rtype: pd.DataFrame
        """
        filepath: str = f'{data_type.value}/{filename}'
        # combined_converters: dict = {**dtypes, **converters}
        #
        # def apply_converter(value):
        #     try:
        #         return combined_converters[value]
        #     except KeyError:
        #         return value

        text_file_reader: TextFileReader = pd.read_csv(
            filepath, header=0, chunksize=chunk_size,
            encoding=settings.ENCODING, parse_dates=parse_dates,
            converters=converters)
        dataframe: pd.DataFrame = pd.concat(text_file_reader,
                                            ignore_index=True)
        for key, value in dtypes.items():
            print(key, value)
            dataframe[key] = dataframe[key].astype(value)
        return dataframe

    @staticmethod
    def save_to_pickle(
            dataframe: pd.DataFrame, data_type: DataType,
            filename: str = 'optimized_df.pkl') -> None:
        """
        Save dataframe to pickle file
        :param dataframe: dataframe
        :type dataframe: pd.DataFrame
        :param data_type: folder where data will be saved from Data Type
        :type data_type: DataType
        :param filename: name of the file
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
        :param filename: name of the file to search and load
        :type filename: str
        :param data_type: folder where data will be saved from Data Type
        :type data_type: DataType
        :return: dataframe read from pickle
        :rtype: pd.DataFrame
        """
        dataframe: pd.DataFrame = pd.read_pickle(
            f'data/{data_type.value}/{filename}')
        return dataframe

    @staticmethod
    def read_from_json(
            filename: str = 'docs/config.json') -> dict:
        """
        Read data from JSON file
        :param filename: name of the file to search and load
        :type filename: str
        :return: Data loaded as a dictionary
        :rtype: dict
        """
        with open(filename, encoding=settings.ENCODING) as file:
            data: dict[str, list[str]] = json.load(file)
        return data
