"""
Loading script for Engineering module
"""
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from models.car import Car
from services.car import CarService


async def loading(dataframe: pd.DataFrame, session: AsyncSession) -> bool:
    """
    Loading data from dataframe into Car table
    :param dataframe: Dataframe with cars sales information
    :type dataframe: pd.DataFrame
    :param session: Async session for database connection
    :type session:AsyncSession
    :return: True if the rows were inserted; otherwise false
    :rtype: bool
    """
    sales_records: list[dict] = dataframe.to_dict('records')
    cars: list[Car] = [Car(**data) for data in sales_records]
    cars_inserted: bool = await CarService.insert_cars_sales(cars, session)
    return cars_inserted
