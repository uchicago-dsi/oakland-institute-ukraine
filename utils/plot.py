# Name: Josemaria Macedo Carrillo
# Title: Plot functions
# Created: 07/14/23
# Last modified: 07/26/23
# DSI

import matplotlib.pyplot as plt
from .clean_data import standard_name
import numpy as np
from matplotlib.ticker import FuncFormatter


def cargo_grouping(df, group, other_cols, sort, asc_bool, agg_dict,
                   new_name = None):
    """
    Create grouped dataframes for charts.

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
        new_name (lst): optional paramater with list of new names for grouped
            dataframe. Default is "None".

    Return(DataFrame): grouped dataframe for charts.
    """
    assert isinstance(agg_dict, dict), "Argument Error: Pass a dictionary to\
    'agg_dict' with columns to aggregate as keys and aggretate functions as values."

    cols = other_cols[:]
    cols.extend(group)
    df_g = df.loc[:, cols].groupby(group, as_index=False)

    if new_name is not None:
        col_dict = {}
        for i, col in enumerate(other_cols):
            col_dict[col] = new_name[i]
        grouped = df_g.agg(agg_dict).rename(columns = col_dict)

    else:
        grouped = df_g.agg(agg_dict)
    
    grouped.columns = list(map(''.join, grouped.columns.values))
    
    if sort is None:
        return grouped
    else:
        return grouped.sort_values(by=sort, ascending=asc_bool)


def plot_line(x_axis, y_axis, line_labels, graph_title, x_label, y_label, data_source, save_fig=True):
    """
    Plot line chart

    Inputs:
        x_axis (array or Series): values for the x axis of the plot
        y_axis (lst): list of arrays or series with values for y axis of the
            plot. If list has n elements then chart will plot n lines. 
        line_labels (lst): list of strings with label names for each line
            respectively
        graph_title (str): title for line chart
        x_label (str): title for the x axis
        y_label (str): title for the y axis
        data_source (str): data source for plot
        save_fig (bool): boolean that states whether or not to save figure in
            "output" directory.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, column in enumerate(y_axis):
        ax.plot(x_axis, column, label=line_labels[i])
        for x, y in zip(x_axis, column):
            formatted_y = format_func(y, None)  # Format y value with commas
            ax.annotate(f'{formatted_y}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()
    spacing = 0.1
    fig.subplots_adjust(bottom=spacing)

    ax.yaxis.set_major_formatter(FuncFormatter(format_func))
    plt.annotate(f"Source: {data_source}.", (0, 0), (-90, -60), fontsize=6, 
             xycoords='axes fraction', textcoords='offset points', va='top')

    if save_fig:
        plt.savefig("app/output/" + standard_name(graph_title) + ".png")

def plot_crops(crop, df_1, df_2, data_source, save_fig=True):
    """
    Plot line chart with crops exports for one company and the total BSGI
        exports

    Inputs:
        crop (str): name of crop that we want to plot
        df_1 (DataFrame): dataset to use for first line
        df_2 (DataFrame): dataset to use for second line
        data_source (str): data source for plot
        save_fig (bool): boolean that states wheter or not to save figure in
            "output" directory.
    """

    crop_kernel = df_1.loc[df_1.loc[:, crop] == True]
    kernel_g = cargo_grouping(crop_kernel, ["year", "month"], ["weight_ton"], ["year", "month"], True, {"weight_ton": "sum"})
    kernel_g["date"] = kernel_g["month"].astype(str) + "/" + kernel_g["year"].astype(str)

    # BSGI data
    crop_bsgi = df_2.loc[df_2.loc[:, "product_std"] == crop]
    outbound_g = cargo_grouping(crop_bsgi, ["year", "month"], ["weight_ton"], ["year", "month"], True, {"weight_ton": "sum"})
    outbound_g["date"] = outbound_g["month"].astype(str) + "/" + outbound_g["year"].astype(str)

    # Plot together
    final = kernel_g.merge(outbound_g, on="date", suffixes=("_kernel", "_bsgi"))

    plot_line(final["date"], [final["weight_ton_kernel"], final["weight_ton_bsgi"]], ["Kernel", "Black Sea Grain Initiative"], "BSGI and Kernel volume of {} exports".format(crop), "Export date (m-yy)", "{} exported (tons)".format(crop), save_fig)


def label(percentage, data, min_wedge_percentage):
    """
    Create labels to pie wedges with absolute and percentage values. Reference: https://matplotlib.org/stable/gallery/pie_and_polar_charts/pie_and_donut_labels.html

    Inputs:
        percentage (float): percentage of the wedge calculated by the pie function
        data (array or Series): values to be summed and get absolute total value
        min_wedge_percentage (float, optional): minimum percentage threshold for annotating wedges (default is 5)
    
    Return (str): string with absolute and percentage values, or an empty string if wedge percentage is below threshold
    """
    if percentage >= min_wedge_percentage:
        return f"{percentage:.1f}%"
    else:
        return ""


def plot_pie(categories, values, category_title, graph_title, data_source, min_wedge_percentage=5, min_legend_percentage=2):
    """
    Plot pie chart with annotations only for wedges above a minimum threshold size.

    Inputs:
        categories (array or Series): categories for the pie wedges
        values (array or Series): values for the pie wedges
        category_title (str): title for category section
        graph_title (str): title for pie chart
        min_wedge_percentage (float, optional): minimum percentage threshold for annotating wedges (default is 5)
        min_legend_percentage (float, optional): minimum percentage threshold for annotating wedges (default is 2)
    """
    fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    print("Values passed to ax.pie:\n", values)
    wedges, texts, autotexts = ax.pie(values, autopct=lambda pct: label(pct, values, min_wedge_percentage),
                                    textprops=dict(color="w"),
                                    wedgeprops=dict(width=0.5), startangle=-40,
                                    pctdistance=0.8)

    annotated_wedges = [wedge for wedge, percentage in zip(wedges, values / sum(values) * 100) if percentage >= min_legend_percentage]
    ax.legend(annotated_wedges, categories,
            title=category_title,
            loc="center left",
            bbox_to_anchor=(1.2, 0.5),
            fontsize="7")

    plt.setp(autotexts, size=7, weight="bold")
    ax.set_title(graph_title)
    plt.annotate(f"Source: {data_source}.", (0, 0), (-90, -60), fontsize=6, 
             xycoords='axes fraction', textcoords='offset points', va='top')
    plt.show()


def format_func(value, tick_number):
    return '{:,}'.format(int(value))


def plot_horizontal(df, x_var, y_var, x_title, y_title, plot_title, data_source):
    """
    Plot a horizontal bar graph.

    Inputs:
        df (DataFrame): data we want to plot
        x_var (str): variable we want to plot in horizontal axis
        y_var (str): variable we want to plot in vertical axis
        x_title (str): horizontal axis title
        plot_title (str): plot title
        data_source (str): cite data source for plot.
    """
    plt.rcdefaults()
    fig, ax = plt.subplots()

    y_labels = df.loc[:, y_var].unique()
    y_pos = np.arange(df.loc[:, y_var].nunique())

    # PENDING: PUT CARGO VALUES TO BARS AND SEPARATE COUNTRY NAMES AND CARGO VALUES MORE
    ax.barh(y_pos, df.loc[:, x_var], align='center')
    ax.set_yticks(y_pos, labels=y_labels)
    ax.invert_yaxis()
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(plot_title)
    ax.tick_params(axis="y", labelsize = 6)

    # Add annotations to the bars
    for i, value in enumerate(df.loc[:, x_var]):
        # Adjust the x-coordinate value (value + xOffset) to move the annotation to the right
        xOffset = 0.05
        ax.text(value + xOffset, i, f'{value:,.0f}', ha='left', va='center', color='black', fontsize=8)

    ax.xaxis.set_major_formatter(FuncFormatter(format_func))
    
    # Adjust layout to prevent overlapping labels
    plt.tight_layout()
    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
    plt.annotate(f"Source: {data_source}.", (0,0), (-90,-60), fontsize=6, 
             xycoords='axes fraction', textcoords='offset points', va='top')
    plt.show()

def plot_bar(x_var, y_var, x_title, y_title, plot_title):
    """
    Plot a vertical bar graph.

    Inputs:
        df (DataFrame): data we want to plot
        x_var (str): variable we want to plot in horizontal axis
        y_var (str): variable we want to plot in vertical axis
        x_title (str): horizontal axis title
        y_title (str): horizontal axis title
        plot_title (str): plot title.
    """

    fig, ax = plt.subplots()

    for i, na_value in enumerate(y_var):
        rects = ax.bar(x_var[i], na_value, label = na_value)
        ax.bar_label(rects, padding=3)
        
    ax.set_xlabel(x_title)
    ax.set_ylabel(y_title)
    ax.set_title(plot_title)

    spacing = 0.1
    fig.subplots_adjust(bottom=spacing)

    plt.xticks(rotation=90)
    plt.tick_params(axis='x', which='major', labelsize=10)
    plt.show()