"""
Main script for ETL process
"""
import asyncio
import concurrent.futures
import logging

import pandas as pd

from analysis import numerical_eda, visualize_data
from core import logging_config
from core.persistence_manager import PersistenceManager
from db.db import init_db
from engineering import extract_data, transform_data, load_to_db

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
    PersistenceManager.save_to_pickle(transformed_df)
    await init_db()
    numerical_eda(transformed_df)  # Check statistics for final df
    try:
        loaded: bool = await load_to_db(transformed_df)
    except Exception as exc:
        logger.error(exc)
        raise exc
    if loaded:
        logger.info("Data loaded")
    logger.info("ETL pipeline completed successfully")


if __name__ == '__main__':
    logger.info("First log message")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        logger.warning("Executing Thread Pool")
        executor.submit(asyncio.run, main())
        logger.warning("Executor submitted")
    logger.info("End of the program execution")
