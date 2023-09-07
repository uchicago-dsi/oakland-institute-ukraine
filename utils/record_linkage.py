# Name: Josemaria Macedo Carrillo
# Title: Record linkage functions
# Created: 07/14/23
# Last modified: 07/20/23
# DSI

import recordlinkage
from .clean_data import PRODUCTS_VAL, translate_column, clean_column
from .plot import cargo_grouping

def test_crop(crop):
    """
    Assert if a crop is in the standard crop categories.

    Inputs:
        crop (str): crop name
    
    Return: None. The assert function evaluates if statement is True. If False
        it return error text.
    """
    product_std = set(PRODUCTS_VAL)
    assert crop in product_std, "Wrong crop Error: crop must be in {crops}."\
                                        .format(crops = product_std)

def filter_crop(df, crop, source):
    """
    Filter dataframe by crop.
    
    Inputs:
        df (DataFrame): dataset to filter
        crop (str): crop to match on
        source (str): dataset's data source, either "ig" (Import Genius),
            "bsgi" (Black Sea Grain Initiative) or "panjiva".
    
    Return (DataFrame): filtered dataframe.
    """
    if source == "ig" or source == "panjiva":
        crop = df.loc[(df.loc[:, crop] == True) &
                          (df.loc[:, "n_products"] == 1)]
    else:
        crop = df.loc[df.loc[:, "product_std"] == crop]
    
    return crop


def find_matches(df_1, df_2, exact_vars= None, string_vars=None,
                 block_vars=None):
    """
    Find all possible matches between two datasets based on different columns

    Inputs:
        df_1 (DataFrame): first dataset to match
        df_2 (DataFrame): second dataset to match
        exact_vars (lst): list of strings with variables names we want to match
            exactly. If empty, it's set to "None" by default
        string_vars (lst): list of strings with variables names we want to match
            by the Jaro Winkler distance rule. If empty, it's set to "None" by
            default
        block_vars (lst): list of strings with blocking variables names. If
            empty, it's set to "None" by default.

    Returns (DataFrame): dataframe with matches from both datasets. Matches are
        not necessarily unique.
    """

    indexer = recordlinkage.Index()

    if block_vars is not None:
        for block in block_vars:
            indexer.block(block)
    else:
        indexer.full()
    candidate_links = indexer.index(df_1, df_2)

    # Comparison step
    compare_cl = recordlinkage.Compare()

    if exact_vars is not None:
        for exact in exact_vars:
            compare_cl.exact(exact, exact, label=exact)
    if string_vars is not None:
        for string in string_vars:
            compare_cl.string(string, string, method="jarowinkler",
                              threshold=0.9, label=string)

    features = compare_cl.compute(candidate_links, df_1, df_2)

    # Classification step
    matches = features[features.sum(axis=1) > 1]
    matches = matches.reset_index()
    print("Number of matches: ",len(matches))

    return matches


def unique_matches(df_1, df_2, exact_vars= None, string_vars=None,
                 block_vars=None):
    """
    Find unique matches between two datasets based on different columns.

    Inputs:
        df_1 (DataFrame): first dataset to match
        df_2 (DataFrame): second dataset to match
        exact_vars (lst): list of strings with variables names we want to match
            exactly. If empty, it's set to "None" by default
        string_vars (lst): list of strings with variables names we want to match
            by the Jaro Winkler distance rule. If empty, it's set to "None" by
            default
        block_vars (lst): list of strings with blocking variables names. If
            empty, it's set to "None" by default.

    Returns (DataFrame): dataframe with unique matches from both datasets.
    """
    df_1.index.name = "df_1"
    df_2.index.name = "df_2"

    matches = find_matches(df_1, df_2, ["date"], ["country"], ["date"])
    
    # Create a unique matches index and filter the matches indexes by it to find
    # unique matches
    df_2_i = matches.groupby("df_2")["df_1"].nunique()
    unique = matches[matches["df_2"].isin(df_2_i[df_2_i == 1].index)][["df_1", "df_2"]].reset_index(drop=True)

    full_unique = unique.merge(df_1, left_on='df_1', right_index=True)
    full_unique = full_unique.merge(df_2, left_on='df_2', right_index=True)

    return full_unique

def record_linkage(df_1, df_2, group, other_cols, sort, asc_bool, agg_dict,
                   exact_vars= None, string_vars=None, block_vars=None,
                   new_name = None):
    """
    Match dataframes based on different variables.

    Inputs:
        df_1 (DataFrame): first dataset we want to aggregate
        df_2 (DataFrame): second dataset
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
        exact_vars (lst): list of strings with variables names we want to match
            exactly. If empty, it's set to "None" by default
        string_vars (lst): list of strings with variables names we want to match
            by the Jaro Winkler distance rule. If empty, it's set to "None" by
            default
        block_vars (lst): list of strings with blocking variables names. If
            empty, it's set to "None" by default.

    Returns (DataFrame): dataframe with unique matches from both datasets based
        on specified variables.
    """

    df_1_g = cargo_grouping(df_1, group, other_cols, sort, True, agg_dict)

    full_unique = unique_matches(df_1_g, df_2, exact_vars, string_vars, block_vars)

    return full_unique

def rl_ig_bsgi(df_ig, df_bsgi, crop, exact_vars= None, string_vars=None,
                   block_vars=None):
    """
    Merge two dataframes based on different variables. The dataframes are matched
    also based on a specific crop.

    Inputs:
        df_ig (DataFrame): Import Genius dataset
        df_bsgi (DataFrame): BSGI dataset
        crop (str): crop to match on
        exact_vars (lst): list of strings with variables names we want to match
            exactly. If empty, it's set to "None" by default
        string_vars (lst): list of strings with variables names we want to match
            by the Jaro Winkler distance rule. If empty, it's set to "None" by
            default
        block_vars (lst): list of strings with blocking variables names. If
            empty, it's set to "None" by default.

    Returns (DataFrame): dataframe with unique matches from both datasets based
        on specified variables.
    """
    test_crop(crop)

    # Filter rows that only have the specified crop so we get more unique
    # matches with the BSGI dataset
    crop_ig = filter_crop(df_ig, crop, "ig")
    crop_bsgi = filter_crop(df_bsgi, crop, "bsgi")

    # Then we group the IG data by export date and country of destination because
    # their data is more granular than the BSGI data.
    # crop_ig = cargo_grouping(crop_ig, ["date", "country"], ["weight_ton"],
    #                          ["date", "country"], True, {"weight_ton":"sum"})

    # full_unique = unique_matches(crop_ig, crop_bsgi, ["date"], ["country"], ["date"])
    full_unique = record_linkage(crop_ig, crop_bsgi, ["date", "country"],
                                 ["weight_ton"],  ["date", "country"], True,
                                 {"weight_ton":"sum"}, ["date"], ["country"],
                                 ["date"])
    
    return full_unique