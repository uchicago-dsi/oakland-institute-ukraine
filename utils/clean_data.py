# Name: Josemaria Macedo Carrillo
# Title: Clean data
# Created: 07/14/23
# Last modified: -
# DSI

import sys
import unicodedata
from deep_translator import GoogleTranslator, DeeplTranslator

def keep_chr(ch):
    """
    Find all characters that are classifed as punctuation in Unicode.
    Reference: CAPP121 course, Programming Assigment 3.

    Inputs:
        ch (str): character number
    
    Returns: character in Unicode
    """

    return unicodedata.category(ch).startswith('P')

def rename_columns(df):
    """
    Rename all columns with standardized names (lowercase, no spaces and no
        special characters).
    
    Inputs:
        df (DataFrame): dataset where we want to rename columns
    
    Returns (DataFrame): dataframe with new column names.
    """
    
    # Create string with punctuation marks we want to remove. Reference: CAPP121
    # course, Programming Assigment 3.
    PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                            if keep_chr(chr(i))])
    
    d = {}
    for col in df.columns:
        new_name = col.lower().strip(PUNCTUATION).replace("(", "").replace(" ", "_")
        d[col] = new_name

    df = df.rename(columns=d)

    return df

def create_columns(df, source):
    """
    Create columns necessary for time series plots.

    Inputs:
        df (DataFrame): dataframe, either from Import Genius or the Black Sea
            Grain Initiative datasets.
        source (str): data source, either "ig" (Import Genius) or "bsgi" (Black
            Sea Grain Initiative).
    
    Returns: None. Changes to dataframe are done in place in input dataframe.
    """
    assert source == "ig" or source == "bsgi", "Wrong data source Error: source\
                                                must be either 'ig' or 'bsgi'."
    
    if source == "ig":
        df["year"] = df["export_date"].dt.year
        df["month"] = df["export_date"].dt.month
        df["weight_ton"] = df["weight_kg"] / 1000
        df["date"] = df["month"].astype(str) + "/" + df["year"].astype(str)

    else:
        df["year"] = df["departure_date"].dt.year
        df["month"] = df["departure_date"].dt.month
        df = df.rename(columns={"metric_tons": "weight_ton"})
        df["date"] = df["month"].astype(str) + "/" + df["year"].astype(str)

def translate_column(df, column, translator, source="uk", target="en"):
    """
    Translate string column faster with Google or Deepl translator.

    Inputs:
        df (DataFrame): dataset
        column (str): name of column to translate. Column values should be
            strings
        translator (str): translator to use. Can be either 'google' or 'deepl'
        source (str): code of language to translate. Default is 'uk' (Ukrainian)
        target (str): target of language to translate. Default is 'en' (English)

    Return: None. Adds new column to passed dataframe.
    """

    # We create list with unique column values so we only translate neccesary
    # number of values
    unique_val = df[column].unique()

    # Translate with Google Translate
    d = {}
    if translator == "google":
        for val in unique_val:
            d[val] = GoogleTranslator(source=source, target=target).translate(val)
        df[column.lower() + "_gt"] = df[column].apply(lambda x: d[x])
    elif translator == "deepl":
        for val in unique_val:
            # REMOVE API KEY AND SUBSTITUTE WITH ENVIRONMENT VARIABLE
            d[val] = DeeplTranslator(api_key="38e53e96-d3f6-559d-f08b-163d92b711a8:fx", source=source, target=target, use_free_api=True).translate(val)
        df[column.lower() + "_deepl"] = df[column].apply(lambda x: d[x])
    else:
        # CHANGE THIS FOR ASSERTION ERROR AT THE BEGGINING OF THE FUNCTION
        return "Wrong translator name. Use 'google' or 'deepl'."