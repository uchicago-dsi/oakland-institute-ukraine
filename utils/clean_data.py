# Name: Josemaria Macedo Carrillo
# Title: Clean data
# Created: 07/14/23
# Last modified: 01/17/24
# DSI

import sys
import os
import unicodedata
from deep_translator import GoogleTranslator, DeeplTranslator
import pandas as pd
from .get_data import get_data, compile_data
from config import IG_FILES_PATH, COUNTRY_FILES, ROOT_PATH, PRODUCTS_VAL,\
    CROP_DICT, HS_DICT, HS_BSGI, CLEAN_FILES_PATH, RAW_FILES_PATH
import json
from .map import top_parent, top_subsidiaries
import re
import copy

def keep_chr(ch):
    """
    Find all characters that are classifed as punctuation in Unicode.
    Reference: CAPP121 course, Programming Assigment 3.

    Inputs:
        ch (str): character number
    
    Returns: character in Unicode
    """

    return unicodedata.category(ch).startswith('P')

PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                            if keep_chr(chr(i))])

def standard_name(string):
    """
    Convert string to standard form: lowercase, no spaces and no special
        characters.
    
    Inputs:
        string (str): string we want to convert to standard form.
    
    Returns (str): string in standard form (lowercase, no spaces and no special
        characters).
    """
    
    return string.lower().strip(PUNCTUATION).replace("(", "").replace(" ", "_")

def rename_columns(df, source):
    """
    Rename all columns with standardized names (lowercase, no spaces and no
        special characters).
    
    Inputs:
        df (DataFrame): dataset where we want to rename columns.
        source (str): data source, either "ig" (Import Genius), "bsgi" (Black
            Sea Grain Initiative) or "panjiva".
    
    Returns (DataFrame): dataframe with new column names.
    """
    
    d = {}
    for col in df.columns:
        new_name = standard_name(col)
        d[col] = new_name

    df = df.rename(columns=d)

    if source == "ig":
        df = df.rename(columns={"export_date": "date",
                                "destination_country": "country"})
    
    elif source == "bsgi":
        df = df.rename(columns={"departure_date": "date",
                                "metric_tons": "weight_ton",
                                "commodity": "product"})
    
    elif source == "panjiva":
        df = df.rename(columns={"shipment_destination": "country",
                                "goods_shipped": "product"})

    return df

def create_crop_dict(df):
    """
    Create crop dictionary with BSGI crop categories as keys and simplified
        categories as values.

    Inputs:
        df (DataFrame): dataframe where we can find the crop categories.
    
    Returns (dict): dictionary with crop categories.
    """
    products = df["product"].unique()

    d = {}
    for i, product in enumerate(products):
        d[product] = PRODUCTS_VAL[i]
 
    return d

def create_columns(df, source):
    """
    Create columns necessary for time series plots.

    Inputs:
        df (DataFrame): dataframe, either from Import Genius or the Black Sea
            Grain Initiative datasets
        source (str): data source, either "ig" (Import Genius), "bsgi" (Black
            Sea Grain Initiative) or "panjiva".
    
    Returns: None. Changes to dataframe are done in place in input dataframe.
    """
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    
    if source == "ig":
        df["weight_ton"] = df["weight_kg"] / 1000
        df["bsgi_commodity"] = df["hs_code"].str[:4].apply(lambda x: HS_BSGI[x]
                                                           if x in HS_BSGI
                                                           else "Not in BSGI")
        # df["parent_company"] = df["company_searched"].apply(lambda x: SUBSIDIARY_DICT[x])
        product_std = set(PRODUCTS_VAL)
        # We create a variable that sums the number of products mentioned in the
        # product name
        df["n_products"] = 0
        for product in product_std:
            product_uk = GoogleTranslator("en", "uk").translate(product)
            df[product] = df["product"].apply(lambda x: True if product_uk in x.lower() else False)
            df["n_products"] += df[product]

    elif source == "bsgi":
        df["product_std"] = df["product"].apply(lambda x: CROP_DICT[x])
        df["hs_code"] = df["product"].apply(lambda x: HS_DICT[x])

    elif source == "panjiva":
        df["weight_ton"] = df["weight_kg"] / 1000
        product_std = set(PRODUCTS_VAL)
        df["n_products"] = 0
        for product in product_std:
            df[product] = df["product"].apply(lambda x: True if product in x.lower() else False)
            df["n_products"] += df[product]


def translate_column(df, column, translator, source="uk", target="en"):
    """
    Translate string column faster with Google or Deepl translator.

    Inputs:
        df (DataFrame): dataset
        column (str): name of column to translate. Column values should be
            strings
        translator (str): translator to use. Can be either 'google' or 'deepl'
        source (str): code of language to translate. Default is 'uk' (Ukrainian)
        target (str): target of language to translate. Default is 'en' (English).

    Return: None. Adds new column to passed dataframe.
    """
    assert translator == "google" or translator == "deepl", "Wrong translator\
                                                name. Use 'google' or 'deepl'."

    # Get deepl API key from environment variable "API_KEY"
    deepl_key = os.environ.get("API_KEY")

    # We create list with unique column values so we only translate neccesary
    # number of values
    unique_val = df[column].unique()

    d = {}
    if translator == "google":
        for val in unique_val:
            d[val] = GoogleTranslator(source=source, target=target).translate(val)
        df[column.lower() + "_gt"] = df[column].apply(lambda x: d[x])
    else:
        for val in unique_val:
            d[val] = DeeplTranslator(api_key=deepl_key, source=source,
                                     target=target, use_free_api=True).translate(val)
        df[column.lower() + "_deepl"] = df[column].apply(lambda x: d[x])

def clean_column(df, column):
    """
    Turn string columns to lowercase and remove any special symbols.

    Inputs:
        df (DataFrame): dataframe with columns we want to clean
        column (str): column we want to clean from dataframe.

    Return: None. It does the change in place in the input dataframe.
    """
    df[column] = df[column].str.lower()

def clean_data(source, path=None):
    """
    Get clean data from data source directory
    Inputs:
        source (str): data source, either "ig" (Import Genius), "bsgi" (Black
            Sea Grain Initiative) or "panjiva".

    Return (DataFrame): dataframe with cleaned data (with renamed columns and
        new columns neccesary for analysis).
    """
    data_sources = ["ig", "bsgi", "panjiva"]
    assert source in data_sources, "Wrong data source Error: source must be\
                                    'ig', 'bsgi' or 'panjiva'."
    
    if path is None:
        df = compile_data(source)
    else:
        df = get_data(path, source)
        if source == "ig":
            df["company_searched"] = df["SHIPPER"]
    df = rename_columns(df, source)
    create_columns(df, source)
    
    columns = ["country", "product"]
    for col in columns:
        clean_column(df, col)

    if source == "bsgi":
        translate_column(df, "product_std", "google", "en", "uk")
        translate_column(df, "country", "google", "en", "uk")
        df = df.rename(columns={"country": "country_en",
                                "country_gt": "country"})
        clean_column(df, "country")

    elif source == "panjiva":
        clean_column(df, "shipment_origin")
        df = df.loc[df.loc[:, "shipment_origin"] == "ukraine"]

    return df

def generate_path(countries):
    """
    Generate path where file is located.

    Inputs:
       countries (str): countries which we want the path for. It can be either
            'asia' or 'spain'.
    
    Return (str): file path where file is located.
    """
    try:
        country_file = COUNTRY_FILES[countries]
    except KeyError:
        print("Wrong countries' name. Use 'asia', 'spain' or 'belgium'.")
    except:
        print("Unknown error")
    path = os.path.join(IG_FILES_PATH, COUNTRY_FILES[countries])

    return path

def correct_name(series, name_dict):
    """
    Update column values from a dataframe with correct ones.

    Inputs:
        series (Series): column we want to update
        name_dict (dict): dictionary with incorrect names as keys and correct
            names as values.
    
    Returns: series with correct names.
    """
    return series.apply(lambda x: name_dict[x])

def filter_country(deals, country):
    """
    Filter land deals for a specific country

    Inputs:
        deals (DataFrame): dataframe with land deals data
        country (str): country name

    Returns (DataFrame): dataframe with country land locations
    """
    deals_c = deals.copy()
    deals_c.loc[:, "country_low"] = deals_c.loc[:, "Target country"].str.lower()
    deals_c = deals_c.loc[deals_c.loc[:, "country_low"].str.contains(country.lower(),
                                                                     na=False)]
    
    return deals_c

def extend_list(list, character):
    """
    Create new list with split text based on "character" parameter

    Inputs:
        list (lst): list of strings
        character (str): character to use to separate string values in list

    Returns (lst): new list with split text based on "character" parameter
    """
    new_lst = []
    for value in list:
        new_lst += value.split(character)

    return new_lst

def clean_list(list, pattern):
    """
    Create new list with clean text based on "pattern" parameter

    Inputs:
        list (lst): list of strings
        pattern (str): pattern we want to find and replace in each string value
            on the list

    Returns (lst): None. Makes changes in place in input "list".
    """
    for i, value in enumerate(list):
        match = re.search(pattern, value)
        if match:
            list[i] = match.group(0)

def parent_subsidiary_dict(parent_lst, deals_data, n_subsidiaries):
    """
    Create dictionary with parent companies as keys and subsidaries as values.

    Inputs:
        parent_lst (lst): list of parent companies
        deals_data (DataFrame): deals dataframe where we're going to look for
            subsidiaries
        n_subsidiaries (int): number of subsidiaries we want to get for parent
            company.

    Returns (dict): dictionary with parent companies as keys and subsidaries as
        values.
    """
    subsidiaries_dict = {}

    for parent in parent_lst:
        subsidiaries_dict[parent] = top_subsidiaries(deals_data, parent,
                                                     n_subsidiaries)

    return subsidiaries_dict

def translate_subsidiaries(dict, source_lan, target_lan):
    """
    Create dictionary with translated subsidiaries' names as values.

    Inputs:
        dict (dict): dictionary with subsidarie names in English
        source_lan (str): current language code of values of dictionary
        target_lan (str): target language code we want to translate values to


    Returns (dict): dictionary with parent companies as keys and subsidaries as
        values.
    """
    d_target = {}

    for parent, sub_lst in dict.items():
        target_lst = []
        for subsidiary in sub_lst:
            target_lst.append(GoogleTranslator(source_lan, target_lan).\
                              translate(subsidiary))
        d_target[parent] = target_lst

    return d_target

def dict_to_lower(dict):
    """
    Convert dictionary values of 'dict' to lowercase

    Inputs:
        dict (dict): dictionary with parent companies as keys and subsidaries
            as values.

    Returns (dict): None. The function does the change in place of the input
        'dict'.
    """
    for parent, subsidiary_lst in dict.items():
        for i, subsidiary in enumerate(subsidiary_lst):
            subsidiary_lst[i] = subsidiary.lower()

def add_companies_manually(old_dict, new_dict):
    """
    Add non-repeated values from 'new_dict' to 'old_dict' based on keys.

    Inputs:
        old_dict (dict): dictionary with parent companies as keys and
            subsidaries as values.
        new_dict (dict): dictionary with parent companies as keys and new
            subsidaries as values.

    Returns (dict): dictionary with non-repeated values from 'new_dict' to
        'old_dict' based on keys.
    """
    old_dict_copy = copy.deepcopy(old_dict)
    
    for parent, subsidiary_lst in new_dict.items():
        for i, subsidiary in enumerate(subsidiary_lst):
            subsidiary_lst[i] = subsidiary.lower()

        if parent in old_dict_copy:
            # old_dict_copy[parent] += new_dict[parent]
            old_dict_copy[parent].extend(subsidiary_lst)
        else:
            # old_dict_copy[parent] = new_dict[parent]
            old_dict_copy[parent] = subsidiary_lst
    
    return old_dict_copy

def create_subsidiary_dict(n_parent_companies, n_subsidiaries, ig_data):
    """
    Create dictionary with parent companies as keys and subsidiaries as values
        using Land Matrix data.

    n_parent_companies (int): top 'n' parent companies we want to 
    """
    # Import Land Matrix data and create list with top parent companies
    path = os.path.join(RAW_FILES_PATH, "land_matrix/deals.csv")
    deals = pd.read_csv(path, delimiter=";")
    deals_c = filter_country(deals, "ukraine")
    parent_lst = top_parent(deals_c, n_parent_companies)
    parent_lst = extend_list(parent_lst, "|")

    # Regex cleans parent company names. Names include deal_id as 'Kernel #366#'
    # Function removes specified regex pattern.
    pattern = r'^.*?(?=#\d+#)'
    clean_list(parent_lst, pattern)

    # Create dictionary with parent companies as keys and subsidiaries as values
    subsidiaries_dict = parent_subsidiary_dict(parent_lst, deals_c, n_subsidiaries)

    # Translate subsidiary names to Ukrainian to try to match them to IG shipper
    # names which are in Ukrainian
    subsidiaries_uk = translate_subsidiaries(subsidiaries_dict, "en", "uk")

    # Turn company values to lowercase both in subsidiary dictionary and IG
    # shipper column
    dict_to_lower(subsidiaries_uk)
    ig_data["shipper_low"] = ig_data["shipper"].str.lower()

    # Manually add some companies we identified separately
    # Import countries dictionaries from JSON file
    # TODO: change path back to previous one
    f = open('names.json') # works when running python pipeline.py command
    # f = open('../names.json') # works when running Jupyter notebook
    data = json.load(f)

    KNOWN_COMPANIES = data["KNOWN_COMPANIES"]
    subsidiaries_c = add_companies_manually(subsidiaries_uk, KNOWN_COMPANIES)

    return subsidiaries_c

def clean_bsgi_by_country(countries):
    """
    Get Black Sea Grain Initiative (BSGI) data for specific countries.

    Inputs:
        countries (str): countries which we want the path for. It can be either
            'asia' or 'spain'.

    Returns (DataFrame): table with filtered BSGI data.
    """
    
    # assert_countries(countries)
    bsgi = clean_data("bsgi")

    # We filter only corresponding months and countries in BSGI dataset
    
    if countries == "asia":
        bsgi_country = bsgi[(bsgi["date"] >= "2022-08-01") &
                            (bsgi["date"] < "2023-04-01") &
                            ((bsgi["country_en"] == "india") |
                             (bsgi["country_en"] == "sri lanka") |
                             (bsgi["country_en"] == "viet nam"))]
    elif countries == "spain":
        bsgi_country = bsgi[(bsgi["date"] >= "2022-08-01") &
                            (bsgi["date"] < "2023-04-01") &
                            (bsgi["country_en"] == "spain")]
    elif countries == "belgium":
        bsgi_country = bsgi[(bsgi["date"] >= "2022-08-01") &
                            (bsgi["date"] < "2023-04-01") &
                            (bsgi["country_en"] == "belgium")]
    else:
        print("Wrong countries' name. Use 'asia', 'spain' or 'belgium'.")

    return bsgi_country

def export_csv(df, file_name, translate=False):
    """
    Export dataframe as .cvs file with a specific file name.

    Inputs:
        df (Dataframe): Import Genius clean and transformed data
        file_name (string): file name for .csv file we want to export

    Return: None. Exports .csv file in "/data" directory
    """
    df_filtered = df[["shipper", "company_std", "weight_ton"]]
    
    if translate:
        translate_column(df_filtered, "shipper", "google", source="uk", target="en")
    
    df_filtered = df_filtered.rename(columns={"shipper": "subsidiary",
                                                "company_std": "parent_company",
                                                "weight_ton": "weight_ton_subs",
                                                "shipper_gt": "subsidiary_en"})
    slice_cols = ["subsidiary", "subsidiary_en", "parent_company", "weight_ton_subs"] if translate else ["subsidiary", "parent_company", "weight_ton_subs"]
    df_filtered = df_filtered[slice_cols]
    df_filtered = df_filtered.sort_values(by = "weight_ton_subs", ascending=False)
        
    
    group_cols = ["subsidiary", "subsidiary_en", "parent_company"] if translate else ["subsidiary", "parent_company"]
    df_g = df_filtered.groupby(group_cols, as_index=False)
    df_g = df_g.sum("weight_ton_subs").sort_values(by=["weight_ton_subs"], ascending=False)

    path = os.path.join(CLEAN_FILES_PATH, file_name)
    df_g.to_csv(path, index=False)