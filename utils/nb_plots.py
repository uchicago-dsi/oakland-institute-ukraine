# Name: Josemaria Macedo Carrillo
# Title: Group data
# Created: 01/24/24
# Last modified: -
# DSI

import pandas as pd
from .transform_data import create_wide_table
from .plot import cargo_grouping, plot_stack_bar, plot_pie

def estimate_table_percentages(table):
    """
    Add non-repeated values from 'new_dict' to 'old_dict' based on keys.

    Inputs:
        old_dict (dict): dictionary with parent companies as keys and
            subsidaries as values.
        new_dict (dict): dictionary with parent companies as keys and new
            subsidaries as values.

    Returns (dict): None. The function does the change in place of the input
        'old_dict'.
    """
    table = table.fillna(0)
    date = table["date"]
    percentage_df = table.drop(columns=["date"]).divide(table.drop(columns=\
                                            ["date"]).sum(axis=1), axis=0) * 100
    percentage_df = percentage_df.round(2)
    percentage_df["date"] = date
    
    return percentage_df

def plot_multiple_countries(country_dict, data, y_axis_limit, source):
    """
    Plot stacked bar charts for more than one country

    Inputs:
        country_dict (dict): dictionary with country names in BSGI as keys
            (in English) and country names in IG as values (Ukrainian)
        data (DataFrame): dataset with information to plot
        y_axis_limit (int): y axis limit in scale
        source (str): text to say which is the data source for the plot.

    Returns (dict): None. The function plots the stacked bar charts.
    """
    for country_en, country_uk in country_dict.items():
        ig_country = data[data["country"] == country_uk]
        pivot_country = create_wide_table(ig_country,
                                          ["year", "month", "company_std"],
                                          ["weight_ton"],
                                          ["year", "month", "company_std"], True,
                                          {"weight_ton": "sum"})
        plot_stack_bar(pivot_country, "Total exports by company",
                       "Weight of exports (metric tons)",
                       f"Total exports to {country_en.capitalize()} by company",
                       "date", y_axis_limit, source)

def plot_all_period(data, source, min_wedge_percentage=2,
                    min_legend_percentage=0):
    """
    Plot a pie chart to estimate the export shares for the whole period of time
        (August 2022 until March 2023), not by month.

    Inputs:
        data (DataFrame): dataset with information to plot
        source (str): text to say which is the data source for the plot
        min_wedge_percentage (float, optional): minimum percentage threshold for
            annotating wedges (default is 2)
        min_legend_percentage (float, optional): minimum percentage threshold
            for adding wedges legend (default is 0).

    Returns (DataFrame): table used to plot pie chart.
    """
    whole_period_g = cargo_grouping(data, ["company_std"], ["weight_ton"],
                                    ["weight_ton"], False, {"weight_ton": "sum"})
    whole_period_g = whole_period_g.reset_index(drop=True)
    plot_pie(whole_period_g["company_std"], whole_period_g["weight_ton"],
             "Company category",
             "Share of exports (metric tons) exported by company", source,
             min_wedge_percentage, min_legend_percentage)
    
    return whole_period_g

def plot_pc_monthly(df, group, agg_cols, sort, asc_bool, agg_dict, x_title,
                    y_title, plot_title, x_axis_ticks, data_source):
    """
    Plot a pie chart to estimate the export shares for the whole period of time
        (August 2022 until March 2023) by month for one country.

    Inputs:
        df (DataFrame): dataset to be used
        group (lst): list of columns to group by
        other_cols(lst): list of columns that are going to be aggregated
        sort (lst): list of columns to sort dataframe by. If new_name is not
            empty then the new column names should be used
        asc_bool (bool): boolean stating wheter or not to sort data "ascending"
            (True) or "descending" (False)
        agg_dict (dict): dict with aggregation functions we want to apply to
            data. If we want to aggregate a column by more than one function
            we put the functions as a list. Example: {"var": ["count", "sum"]}.
        x_title (str): horizontal axis title
        y_title (str): horizontal axis title
        plot_title (str): plot title
        x_axis_ticks (str): name of column to use for x axis tick names
        data_source (str): data source text.

    Return: None. Function plots pie chart.
    """
    pivot = create_wide_table(df=df, group=group, agg_cols=agg_cols, sort=sort,
                              asc_bool=asc_bool, agg_dict=agg_dict, new_name=None)

    percentages_df = estimate_table_percentages(pivot)

    plot_stack_bar(df=percentages_df, x_title=x_title, y_title=y_title,
                plot_title=plot_title, x_ticks=x_axis_ticks, ylim=105,
                data_source=data_source)