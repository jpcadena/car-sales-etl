"""
Loading script for Engineering module
"""
import logging

import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from core import logging_config
from models.car import Car
from services.car import CarService

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


async def loading(dataframe: pd.DataFrame, session: AsyncSession) -> bool:
    """
    Loading data from dataframe into the Car table
    :param dataframe: Dataframe with cars sales information
    :type dataframe: pd.DataFrame
    :param session: Async session for database connection
    :type session:AsyncSession
    :return: True if the rows were inserted; otherwise false
    :rtype: bool
    """
    sales_records: list[dict] = dataframe.to_dict('records')
    cars: list[Car] = [Car(**data) for data in sales_records]
    cars_inserted: bool = await CarService.insert_multiple_car_sales(
        cars, session)
    logger.info("Inserted %s car sales into the table.", str(len(cars)))
    return cars_inserted
