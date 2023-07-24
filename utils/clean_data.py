# Name: Josemaria Macedo Carrillo
# Title: Clean data
# Created: 07/14/23
# Last modified: 07/20/23
# DSI

import os
import sys
import unicodedata
from deep_translator import GoogleTranslator, DeeplTranslator
import pandas as pd

PRODUCTS_VAL = ["corn", "soya", "sunflower", "wheat", "sunflower", "barley",
                "peas", "rapeseed", "sunflower", "vegetable", "soya", "canola",
                "rapeseed", "sunflower", "mixed", "wheat", "sugar beet"]


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
        product_std = set(PRODUCTS_VAL)
        # We create a variable that sums the number of products mentioned in the
        # product name
        df["n_products"] = 0
        for product in product_std:
            product_uk = GoogleTranslator("en", "uk").translate(product)
            df[product] = df["product"].apply(lambda x: True if product_uk in x.lower() else False)
            df["n_products"] += df[product]
        translate_column(df, "country", "google", "en", "uk")


    elif source == "bsgi":
        d = create_crop_dict(df)
        df["product_std"] = df["product"].apply(lambda x: d[x])

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