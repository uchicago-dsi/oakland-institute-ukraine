# Name: Josemaria Macedo Carrillo
# Title: Plot functions
# Created: 07/14/23
# Last modified: 07/20/23
# DSI

import matplotlib.pyplot as plt
from .clean_data import standard_name

def cargo_grouping(df, group, other_cols, sort, asc_bool, new_name = None):
    """
    Create grouped dataframes for charts

    Inputs:
        df(DataFrame): dataset to be used
        group(lst): list of columns to group by
        other_cols(lst): list of columns that are going to be aggregated
        sortby(lst): list of columns to sort dataframe by. If new_name is not
            empty then the new column names should be used.
        new_name(lst): optional paramater with list of new names for grouped
            dataframe. Default is "None".

    Return(DataFrame): grouped dataframe for charts
    """
    cols = other_cols[:]
    cols.extend(group)
    df_g = df.loc[:, cols].groupby(group)

    if new_name is not None:
        col_dict = {}
        for i, col in enumerate(other_cols):
            col_dict[col] = new_name[i]
        grouped = df_g.sum().reset_index().rename(columns = col_dict) # PENDING: change this later to include any kind of aggregation
    else:
        grouped = df_g.sum().reset_index()
    
    if sort is None:
        return grouped
    else:
        return grouped.sort_values(by=sort, ascending=asc_bool)

    
def plot_line(x_axis, y_axis, line_labels, graph_title, x_label, y_label, save_fig=True):
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
        save_fig (bool): boolean that states wheter or not to save figure in
            "output" directory.
    """
    fig, ax = plt.subplots(figsize=(12, 6))

    for i, column in enumerate(y_axis):
        ax.plot(x_axis, column, label = line_labels[i])
        for x, y in zip(x_axis, column):
            ax.annotate(f'{int(y)}', (x, y), textcoords="offset points", xytext=(0, 10), ha='center')

    plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')

    plt.title(graph_title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.legend()

    if save_fig:
        # plt.savefig("output/" + standard_name(graph_title) + ".png")
        plt.savefig("test_docker.png")

def plot_crops(crop, df_1, df_2, save_fig=True):
    """
    Plot line chart with crops exports for one company and the total BSGI
        exports

    Inputs:
        crop (str): name of crop that we want to plot
        df_1 (DataFrame): dataset to use for first line
        df_2 (DataFrame): dataset to use for second line
        save_fig (bool): boolean that states wheter or not to save figure in
            "output" directory.
    """

    crop_kernel = df_1.loc[df_1.loc[:, crop] == True]
    kernel_g = cargo_grouping(crop_kernel, ["year", "month"], ["weight_ton"], ["year", "month"], True)
    kernel_g["date"] = kernel_g["month"].astype(str) + "/" + kernel_g["year"].astype(str)

    # BSGI data
    crop_bsgi = df_2.loc[df_2.loc[:, "product_std"] == crop]
    outbound_g = cargo_grouping(crop_bsgi, ["year", "month"], ["weight_ton"], ["year", "month"], True)
    outbound_g["date"] = outbound_g["month"].astype(str) + "/" + outbound_g["year"].astype(str)

    # Plot together
    final = kernel_g.merge(outbound_g, on="date", suffixes=("_kernel", "_bsgi"))

    plot_line(final["date"], [final["weight_ton_kernel"], final["weight_ton_bsgi"]], ["Kernel", "Black Sea Grain Initiative"], "BSGI and Kernel volume of {} exports".format(crop), "Export date (m-yy)", "{} exported (tons)".format(crop), save_fig)
