"""
Init DB script
"""
from sqlalchemy.exc import CompileError, DataError, DatabaseError, \
    DisconnectionError, IntegrityError, InternalError, InvalidatePoolError, \
    PendingRollbackError, TimeoutError as SATimeoutError
from sqlalchemy.ext.asyncio import AsyncTransaction
from db.base import Base
from db.session import async_engine


async def create_db_and_tables() -> None:
    """
    Create database and tables without duplicating them.
    :return: None
    :rtype: NoneType
    """
    async with async_engine.connect() as async_connection:
        try:
            transaction: AsyncTransaction = async_connection.begin()
            await transaction.start()
            await async_connection.run_sync(Base.metadata.drop_all)
            await async_connection.run_sync(
                Base.metadata.create_all, checkfirst=True)
            await transaction.commit()
        except PendingRollbackError as pr_exc:
            await transaction.rollback()
            print(pr_exc)
        except CompileError as c_exc:
            print(c_exc)
        except DataError as d_exc:
            print(d_exc)
        except IntegrityError as i_exc:
            print(i_exc)
        except InternalError as int_exc:
            print(int_exc)
        except DatabaseError as db_exc:
            print(db_exc)
        except InvalidatePoolError as ip_exc:
            print(ip_exc)
        except DisconnectionError as dc_exc:
            print(dc_exc)
        except SATimeoutError as t_exc:
            print(t_exc)


async def init_db() -> None:
    """
    Initialization of the database connection
    :return: None
    :rtype: NoneType
    """
    await create_db_and_tables()
    print("init_db")
