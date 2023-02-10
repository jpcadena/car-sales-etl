"""
Main script for ETL process
"""
import asyncio
import concurrent.futures
import logging

import pandas as pd

from analysis import numerical_eda, visualize_data
from core import logging_config
from db.db import init_db
from engineering import extract_data, transform_data, load_data

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Main function to execute
    :return: None
    :rtype: NoneType
    """
    logger.info("Running main method")
    dataframe: pd.Dataframe = extract_data()
    numerical_eda(dataframe)
    transformed_df = transform_data(dataframe)
    visualize_data(transformed_df)
    numerical_eda(transformed_df)
    # TODO: generate processed dataset
    await init_db()
    # TODO: Check Pandas.to_sql() performance against Async SQLAlchemy
    loaded: bool = await load_data(transformed_df)
    print(loaded)
    await asyncio.sleep(1)
    logger.info("ETL pipeline completed successfully")


if __name__ == '__main__':
    logger.info("first log message")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        logger.warning("Executing Thread Pool")
        executor.submit(asyncio.run, main())
        logger.warning("Executor submitted")
    logger.info("End of the program execution")
