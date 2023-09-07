# Name: Josemaria Macedo Carrillo
# Title: Transform data
# Created: 07/25/23
# Last modified: -
# DSI

from .record_linkage import filter_crop, test_crop
from .plot import cargo_grouping, plot_pie
import pandas as pd

def estimate_weights(company_df, company_col, company_add, bsgi_df, bsgi_col, plot_title, crop=None):
    """
    Estimate the export weights for a specific crop.

    Inputs:
        company_df (DataFrame): company dataframe with data from Import Genius
            or Panjiva
        company_col (str): column name from the company dataframe that we want
            to group by
        company_add (str): column name from the company dataframe that we want
            to add
        bsgi_df (DataFrame): BSGI dataframe
        bsgi_col (str): column name from the BSGI dataframe that we want to add
        plot_title (str): title for plot
        crop (str): crop we want to use to estimate export weights.

    Returns (DataFrame): dataframe to plot.
    """
    
    if crop is None:
        company_g = cargo_grouping(company_df, [company_col], [company_add], [company_col], True, {company_add: "sum"})
        bsgi_weight = bsgi_df[bsgi_col].sum()
        print("bsgi_weight: ", bsgi_weight)
        company_weight = company_g["weight_ton"].sum()
        print("ig_weight: ", company_weight)
        other = bsgi_weight - company_weight

        bsgi_dict = {company_col: 'Other', bsgi_col: [other]}
        bsgi_final = pd.DataFrame(bsgi_dict)
        final = pd.concat([company_g, bsgi_final], ignore_index=True)
        final = final.sort_values(by=[bsgi_col], ascending=False)
        # print("Table for plot:\n", final)
        plot_pie(final[company_col], final[bsgi_col], company_col, plot_title, "Company data for October 2022", 2, 0.1)
        return final
    
    else:
        test_crop(crop)
        try:
            row_1 = filter_crop(company_df, crop, "ig")[company_col].sum()
        except:
            # Case when we already filtered the company_df data by crop
            row_1 = company_df[company_col].sum()
        
        row_2 = filter_crop(bsgi_df, crop, "bsgi")[bsgi_col].sum()

    # CHANGE THIS SO COMPANY NAMES CAN BE DYMANIC
    d = {"company":["Kernel", "Other"], "weight":[row_1, row_2]}
    df = pd.DataFrame(data=d)
    
    return df

def get_company_dict(company_col, company_dict):
    """
    Get a dictionary with raw company names (shipper) as keys and standardized
    company names as values.

    Inputs:
        company_col (Series): series with raw company names in
            Ukrainian
        company_dict (dict): dictionary with parent companies in English as keys
            and subsiary companies in Ukrainian as values.
    
    Return (dict): dictionary with raw company names (shipper) as keys and
        standardized company names as values.
    """
    all_companies = company_col.unique()
    rename_dict = {}

    for row in all_companies:
        for parent, subsidiaries in company_dict.items():
            for subsidiary in subsidiaries:
                if subsidiary in row:
                    rename_dict[row] = parent
        if row not in rename_dict.keys():
            rename_dict[row] = "Other"
    
    return rename_dict

def standard_company_name(company_col, company_dict):
    """
    Create new column with standardized company names from "column" parameter.

    Inputs:
        company_col (Series): series with raw company names in
            Ukrainian
        company_dict (dict): dictionary with parent companies in English as keys
            and subsiary companies in Ukrainian as values.
    
    Return (Series): series with new standardized company names.
    """
    rename_dict = get_company_dict(company_col, company_dict)
    standard_col = company_col.apply(lambda x: rename_dict[x])
    
    return standard_col

def create_wide_table(df, group, other_cols, sort, asc_bool, agg_dict,
                   new_name = None):
    """
    Create wide table from dataframe.

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

    Return(DataFrame): wide table with month-year and standardized company names
    as columns
    """
    # First we get long table by grouping data
    df_g = cargo_grouping(df, group, other_cols, sort, asc_bool, agg_dict)
    df_g["date"] = df_g["month"].astype(str) + "/" + df_g["year"].astype(str)
    
    # Now we get the wide table format
    pivot = pd.pivot_table(data=df_g, index=['date', "year", "month"],
                           columns=['company_std'],
                           values='weight_ton').reset_index()
    pivot = pivot.sort_values(by=["year", "month"]).drop(['year', 'month'],
                                                         axis=1).round(1)
    
    return pivot
    