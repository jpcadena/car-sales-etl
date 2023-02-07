"""
Main script for ETL process
"""
import asyncio
import concurrent.futures
import logging

from core import logging_config

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


async def main() -> None:
    """
    Main function to execute
    :return: None
    :rtype: NoneType
    """
    print("Executing")
    await asyncio.sleep(1)
    logger.info("ETL pipeline completed successfully")


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # try:
    #     loop.run_until_complete(main())
    # finally:
    #     loop.close()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(asyncio.run, main())
