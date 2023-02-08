"""
Main script for ETL process
"""
import asyncio
import concurrent.futures
import logging

import pandas as pd

from analysis.eda import analyze_dataframe, plot_count, plot_distribution, \
    boxplot_dist, plot_scatter, plot_heatmap
from core import logging_config
from engineering.extraction import extract_data
from engineering.transformation import cast_column, remove_missing_values, \
    convert_date_column, create_sale_year, create_categorical_model

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


def transform_data(dataframe: pd.DataFrame) -> pd.DataFrame:
    """
    Transform dataframe based on the requirements
    :param dataframe: Raw dataframe
    :type dataframe: pd.DataFrame
    :return: Transformed dataframe
    :rtype: pd.DataFrame
    """
    dataframe = cast_column(dataframe)
    dataframe = remove_missing_values(dataframe)
    dataframe = convert_date_column(dataframe)
    dataframe = create_sale_year(dataframe)
    dataframe = create_categorical_model(dataframe)
    return dataframe


def visualize_data(dataframe: pd.DataFrame) -> None:
    """
    Basic visualization of the dataframe
    :param dataframe: Dataframe to visualize
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    plot_count(dataframe, 'Buyer Gender')
    plot_distribution(dataframe.Make, 'lightskyblue')
    boxplot_dist(dataframe, 'Buyer Age', 'Color')
    plot_scatter(dataframe, 'Make', 'Buyer Gender', 'New Car')
    plot_heatmap(dataframe)


async def main() -> None:
    """
    Main function to execute
    :return: None
    :rtype: NoneType
    """
    print("Starting main")
    dataframe: pd.Dataframe = extract_data()
    analyze_dataframe(dataframe)
    transformed_df = transform_data(dataframe)
    print(transformed_df)
    print(transformed_df.dtypes)
    print(transformed_df.info(memory_usage='deep'))
    print(transformed_df.memory_usage(deep=True))
    # Fixme: Some Matplotlib issue. Maybe with thread pool
    # visualize_data(transformed_df)
    # print("after visualization")
    await asyncio.sleep(1)
    print("after sleep")
    logger.info("ETL pipeline completed successfully")


if __name__ == '__main__':
    # loop = asyncio.new_event_loop()
    # asyncio.set_event_loop(loop)
    # try:
    #     loop.run_until_complete(main())
    # finally:
    #     loop.close()
    logger.info("first log")
    print("__name__")
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print("before execution")
        executor.submit(asyncio.run, main())
        print("finishing")
    print("end of thread")
