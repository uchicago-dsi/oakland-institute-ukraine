# Name: Josemaria Macedo Carrillo
# Title: Transform data
# Created: 07/25/23
# Last modified: -
# DSI

from .record_linkage import filter_crop, test_crop
import pandas as pd

def estimate_weights(company_df, company_col, bsgi_df, bsgi_col, crop=None):
    """
    Estimate the export weights for a specific crop.

    Inputs:
        company_df (DataFrame): company dataframe with data from Import Genius
            or Panjiva
        company_col (str): column name from the company dataframe that we want
            to add
        bsgi_df (DataFrame): BSGI dataframe
        bsgi_col (str): column name from the BSGI dataframe that we want to add.
        crop (str): crop we want to use to estimate export weights

    Returns (DataFrame): dataframe with total export weight for a specific crop
    and company in one row and export weight for a specific crop in the BSGI
    dataframe in the other row.
    """
    test_crop(crop)
    
    # CHANGE THIS SO IT CAN ALLOW MORE THAN ONE COMPANY BY GETTING WEIGHT BY
    # GROUPING BY COMPANY WITH CARGO_GROUPING FUNCTION MAYBE
    
    if crop is None:
        row_1 = company_df[company_col].sum()
        row_2 = bsgi_df[bsgi_col].sum()
    else:
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