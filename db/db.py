"""
Init DB script
"""
import logging

from sqlalchemy.exc import CompileError, DataError, DatabaseError, \
    DisconnectionError, IntegrityError, InternalError, InvalidatePoolError, \
    PendingRollbackError, TimeoutError as SATimeoutError
from sqlalchemy.ext.asyncio import AsyncTransaction

from core import logging_config
from db.base import Base
from db.session import async_engine

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


async def create_db_and_tables() -> None:
    """
    Create database and tables without duplicating them.
    :return: None
    :rtype: NoneType
    """
    async with async_engine.connect() as async_connection:
        try:
            transaction: AsyncTransaction = async_connection.begin()
            logger.warning("Database connection established")
            await transaction.start()
            # await async_connection.run_sync(
            #     Base.metadata.drop_alll,
            #     checkfirst=True,
            #     cascade=True
            # )
            await async_connection.run_sync(
                Base.metadata.create_all,
                checkfirst=True
            )
            await transaction.commit()
            logger.warning("Database tables created successfully")
        except PendingRollbackError as pr_exc:
            await transaction.rollback()
            logger.error(pr_exc)
        except CompileError as c_exc:
            logger.error(c_exc)
        except DataError as d_exc:
            logger.error(d_exc)
        except IntegrityError as i_exc:
            logger.error(i_exc)
        except InternalError as int_exc:
            logger.error(int_exc)
        except DatabaseError as db_exc:
            logger.error(db_exc)
        except InvalidatePoolError as ip_exc:
            logger.error(ip_exc)
        except DisconnectionError as dc_exc:
            logger.error(dc_exc)
        except SATimeoutError as t_exc:
            logger.error(t_exc)


async def init_db() -> None:
    """
    Initialization of the database connection
    :return: None
    :rtype: NoneType
    """
    await create_db_and_tables()
    logger.info("Database initialized")
