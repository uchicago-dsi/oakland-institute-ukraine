# Name: Josemaria Macedo Carrillo
# Ttile: Plot functions
# Created: 07/14/23
# Last modified: -
# DSI

def keep_chr(ch):
    """
    Find all characters that are classifed as punctuation in Unicode.
    This function comes from CAPP121 Programming Assigment 3.

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
    
    # Create string with punctuation marks we want to remove. Took this string
    # function from CAPP121 course (Programming Assigment 3): https://github.com/uchicago-CAPP30121-aut-2022/pa3-jmacedoc1/blob/main/analyze.py
    PUNCTUATION = " ".join([chr(i) for i in range(sys.maxunicode)
                            if keep_chr(chr(i))])
    
    d = {}
    for col in df.columns:
        new_name = col.lower().strip(PUNCTUATION).replace("(", "").replace(" ", "_")
        d[col] = new_name

    df = df.rename(columns=d)

    return df