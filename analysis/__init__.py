"""
Analysis package initialization
"""
import logging

import pandas as pd

from analysis.eda import analyze_dataframe, plot_count, plot_distribution, \
    boxplot_dist, plot_scatter, plot_heatmap
from core import logging_config

logging_config.setup_logging()
logger: logging.Logger = logging.getLogger(__name__)


def numerical_eda(dataframe: pd.DataFrame) -> None:
    """
    EDA based on numerical values for dataset
    :param dataframe: Dataframe to analyze
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    logger.info("Running Exploratory Data Analysis")
    analyze_dataframe(dataframe)


def visualize_data(dataframe: pd.DataFrame) -> None:
    """
    Basic visualization of the dataframe
    :param dataframe: Dataframe to visualize
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    logger.info("Running visualization")
    plot_count(dataframe, 'buyer_gender')
    plot_distribution(dataframe.make_classification, 'lightskyblue')
    boxplot_dist(dataframe, 'buyer_age', 'color')
    plot_scatter(dataframe, 'make_classification', 'buyer_age', 'new_car')
    plot_heatmap(dataframe)
