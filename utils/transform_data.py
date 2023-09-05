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