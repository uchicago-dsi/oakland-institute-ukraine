# Name: Josemaria Macedo Carrillo
# Title: Record linkage functions
# Created: 07/14/23
# Last modified: 07/18/23
# DSI

import recordlinkage


def find_matches(dfA, dfB, exact_vars= None, string_vars=None, block_vars=None):
    """
    Find most possible matches between two datasets based on different columns

    Inputs:
        dfA (DataFrame): first dataset to match
        dfB (DataFrame): second dataset to match
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
    candidate_links = indexer.index(dfA, dfB)

    # Comparison step
    compare_cl = recordlinkage.Compare()

    for exact in exact_vars:
        compare_cl.exact(exact, exact, label=exact)
    for string in string_vars:
        compare_cl.string(string, string, method="jarowinkler", threshold=0.9, label=string)

    features = compare_cl.compute(candidate_links, dfA, dfB)

    # Classification step
    matches = features[features.sum(axis=1) > 1]
    print("Number of matches: ",len(matches))
    
    return matches