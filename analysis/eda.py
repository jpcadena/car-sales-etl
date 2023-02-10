"""
Exploratory Data Analysis script including:
 numerical and visualization analysis.
"""
import re

import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

from core.config import settings

pd.set_option('display.max_columns', 10)


def analyze_dataframe(dataframe: pd.DataFrame) -> None:
    """
    Analyze the dataframe and its columns with inference statistics
    :param dataframe: DataFrame to analyze
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    print(dataframe.head())
    print(dataframe.shape)
    print(dataframe.dtypes)
    print(dataframe.info(memory_usage='deep'))
    print(dataframe.memory_usage(deep=True))
    print(dataframe.describe(include='all', datetime_is_numeric=True))

    # non_numeric_df = dataframe.select_dtypes(exclude=settings.NUMERICS)
    # for column in non_numeric_df.columns:
    #     print(non_numeric_df[column].value_counts())
    #     print(non_numeric_df[column].unique())
    #     print(non_numeric_df[column].value_counts(normalize=True) * 100)


def plot_count(dataframe: pd.DataFrame, hue: str) -> None:
    """
    This method plots the counts of observations from the given variables
    :param dataframe: dataframe containing tweets info
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    plot_iterator: int = 1
    variables = dataframe.select_dtypes(
        include=['bool', 'category', 'object'])
    label: str
    for i in variables:
        plt.figure(figsize=settings.FIG_SIZE)
        sns.countplot(
            x=dataframe[i], hue=dataframe[hue], palette=settings.PALETTE)
        label = re.sub(
            pattern=settings.RE_PATTERN, repl=settings.RE_REPL, string=i)
        plt.xlabel(label, fontsize=15)
        plt.ylabel('Count', fontsize=15)
        plt.title(f'Count-plot for {label}')
        plot_iterator += 1
        plt.tight_layout()
        plt.savefig(f'reports/figures/discrete_{i}.png')
        plt.show()


def plot_distribution(df_column: pd.Series, color: str) -> None:
    """
    This method plots the distribution of the given quantitative
     continuous variable
    :param df_column: Single column
    :type df_column: pd.Series
    :param color: color for the distribution
    :type color: str
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    label: str = re.sub(
        pattern=settings.RE_PATTERN, repl=settings.RE_REPL,
        string=str(df_column.name))
    dist_plot = sns.displot(x=df_column, kde=True, color=color, height=8,
                            aspect=1.5)
    plt.title('Distribution Plot for ' + label)
    plt.xlabel(label, fontsize=settings.FONT_SIZE)
    plt.ylabel('Frequency', fontsize=settings.FONT_SIZE)
    dist_plot.fig.tight_layout()
    plt.savefig('reports/figures/' + str(df_column.name) + '.png')
    plt.show()


def boxplot_dist(
        dataframe: pd.DataFrame, first_variable: str, second_variable: str
) -> None:
    """
    This method plots the distribution of the first variable data
    in regard to the second variable data in a boxplot
    :param dataframe: data to use for plot
    :type dataframe: pd.DataFrame
    :param first_variable: first variable to plot
    :type first_variable: str
    :param second_variable: second variable to plot
    :type second_variable: str
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    x_label: str = re.sub(
        pattern=settings.RE_PATTERN, repl=settings.RE_REPL,
        string=first_variable)
    y_label: str = re.sub(
        pattern=settings.RE_PATTERN, repl=settings.RE_REPL,
        string=second_variable)
    sns.boxplot(x=first_variable, y=second_variable, data=dataframe,
                palette=settings.PALETTE)
    plt.title(
        x_label + ' in regards to ' + y_label, fontsize=settings.FONT_SIZE)
    plt.xlabel(x_label, fontsize=settings.FONT_SIZE)
    plt.ylabel(y_label, fontsize=settings.FONT_SIZE)
    plt.savefig(
        f'reports/figures/discrete_{first_variable}_{second_variable}.png')
    plt.show()


def plot_scatter(
        dataframe: pd.DataFrame, x_column: str, y_column: str, hue: str
) -> None:
    """
    This method plots the relationship between x and y for hue subset
    :param dataframe: dataframe containing tweets
    :type dataframe: pd.DataFrame
    :param x_column: x-axis column name from dataframe
    :type x_column: str
    :param y_column: y-axis column name from dataframe
    :type y_column: str
    :param hue: grouping variable to filter plot
    :type hue: str
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    sns.scatterplot(x=x_column, data=dataframe, y=y_column, hue=hue,
                    palette=settings.PALETTE)
    label: str = re.sub(
        pattern=settings.RE_PATTERN, repl=settings.RE_REPL, string=y_column)
    plt.title(f'{x_column} Wise {label} Distribution')
    print(dataframe[[x_column, y_column]].corr())
    plt.savefig(f'reports/figures/{x_column}_{y_column}_{hue}.png')
    plt.show()


def plot_heatmap(dataframe: pd.DataFrame) -> None:
    """
    Plot heatmap to analyze correlation between features
    :param dataframe: dataframe containing tweets
    :type dataframe: pd.DataFrame
    :return: None
    :rtype: NoneType
    """
    plt.figure(figsize=settings.FIG_SIZE)
    sns.heatmap(data=dataframe.select_dtypes(
        include=settings.NUMERICS).corr(), annot=True, cmap="RdYlGn")
    plt.title('Heatmap showing correlations among columns',
              fontsize=settings.FONT_SIZE)
    plt.savefig('reports/figures/correlations_heatmap.png')
    plt.show()
