# Name: Josemaria Macedo Carrillo
# Title: Record linkage functions
# Created: 07/14/23
# Last modified: 07/18/23
# DSI

import recordlinkage
from .clean_data import PRODUCTS_VAL, translate_column, clean_column


def find_matches(df_a, df_b, exact_vars= None, string_vars=None,
                 block_vars=None):
    """
    Find most possible matches between two datasets based on different columns

    Inputs:
        df_a (DataFrame): first dataset to match
        df_b (DataFrame): second dataset to match
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
    for block in block_vars:
        indexer.block(block)
    candidate_links = indexer.index(df_a, df_b)

    # Comparison step
    compare_cl = recordlinkage.Compare()

    for exact in exact_vars:
        compare_cl.exact(exact, exact, label=exact)
    for string in string_vars:
        compare_cl.string(string, string, method="jarowinkler", threshold=0.9,
                                                                label=string)

    features = compare_cl.compute(candidate_links, df_a, df_b)

    # Classification step
    matches = features[features.sum(axis=1) > 1]
    matches = matches.reset_index()
    print("Number of matches: ",len(matches))

    return matches

def record_linkage(df_ig, df_bsgi, crop, exact_vars= None, string_vars=None,
                   block_vars=None):
    """
    Merge two dataframes based on different variables.

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
    product_std = set(PRODUCTS_VAL)
    assert crop in product_std, "Wrong crop Error: crop must be in {crops}."\
                                        .format(crops = product_std)
    
    # We create a variable that sums the number of products mentioned in the
    # product name
    crop_ig = df_ig.copy()
    crop_ig["n_products"] = 0

    for product in product_std:
        crop_ig["n_products"] += crop_ig[product]

    # Filter rows that only have the specified crop so we get more unique
    # matches with the BSGI dataset
    crop_ig = crop_ig.loc[(crop_ig.loc[:, crop] == True) &
                          (crop_ig.loc[:, "n_products"] == 1)]
    crop_bsgi = df_bsgi.loc[df_bsgi.loc[:, "product_std"] == "sunflower"]

    translate_column(crop_bsgi, "country", "google", "en", "uk")
    crop_bsgi = crop_bsgi.rename(columns={"country": "country_en", "country_gt": "country"})
    clean_column(crop_bsgi, "country")

    # Then we group the IG data by export date and country of destination because
    # their data is more granular than the BSGI data.
    crop_ig = crop_ig[["date", "country", "weight_ton"]]\
                            .groupby(["date", "country"]).sum().reset_index()

    crop_ig.index.name = "df_ig"
    crop_bsgi.index.name = "df_bsgi"

    matches = find_matches(crop_ig, crop_bsgi, ["date"], ["country"], ["date"])
    
    # Create a unique matches index and filter the matches indexes by it to find
    # unique matches
    bsgi_i = matches.groupby("df_bsgi")["df_ig"].nunique()
    unique = matches[matches["df_bsgi"].isin(bsgi_i[bsgi_i == 1].index)][["df_ig", "df_bsgi"]].reset_index(drop=True)

    full_unique = unique.merge(crop_ig, left_on='df_ig', right_index=True)
    full_unique = full_unique.merge(crop_bsgi, left_on='df_bsgi', right_index=True)
    
    return full_unique