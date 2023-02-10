"""
Car service script
"""
import logging
from typing import Optional

from sqlalchemy.exc import ArgumentError, PendingRollbackError, \
    MultipleResultsFound, IdentifierError
from sqlalchemy.ext.asyncio import AsyncSession

from core import logging_config
from models.car import Car

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


class CarService:
    """
    Car services for database
    """

    @staticmethod
    async def read_sale_by_id(
            sale_id: int, session: AsyncSession) -> Optional[Car]:
        """
        Read car sale information from table
        :param sale_id: Unique identifier of the car sale
        :type sale_id: int
        :param session: Async Session for Database
        :type session: AsyncSession
        :return: Car sale information
        :rtype: Car
        """
        car: Car = None
        try:
            car = await session.get(Car, sale_id)
        except MultipleResultsFound as mrf_exc:
            logger.error(mrf_exc)
        except ArgumentError as a_exc:
            logger.error(a_exc)
        except IdentifierError as i_exc:
            logger.error(i_exc)
        logger.info("FOUND Car sale!")
        return car

    @staticmethod
    async def insert_car_sale(car: Car, session: AsyncSession) -> bool:
        """
        Insert a new car sale into the table
        :param car: Car object based on table model
        :type car: Car
        :param session: Async Session for Database
        :type session: AsyncSession
        :return: True if the row was inserted; otherwise false
        :rtype: bool
        """
        async with session.begin():
            try:
                session.add(car)
            except ArgumentError as a_exc:
                logger.error(a_exc)
                await session.rollback()
                return False
            except PendingRollbackError as pr_exc:
                logger.error(pr_exc)
                await session.rollback()
                return False
            await session.commit()
            logger.info("Row inserted successfully")
            return True

    @staticmethod
    async def insert_multiple_car_sales(
            cars: list[Car], session: AsyncSession) -> bool:
        """
        Insert multiple cars sales into the table
        :param cars: List of Car objects based on table model
        :type cars: list[Car]
        :param session: Async Session for Database
        :type session: AsyncSession
        :return: True if the rows were inserted; otherwise false
        :rtype: bool
        """
        async with session.begin():
            try:
                session.add_all(cars)
            except ArgumentError as a_exc:
                logger.error(a_exc)
                await session.rollback()
                return False
            except PendingRollbackError as pr_exc:
                logger.error(pr_exc)
                await session.rollback()
                return False
            await session.commit()
            logger.info("Rows inserted successfully")
            return True
