import os

## HANDLE FILEPATHS ##

# ROOT_PATH = os.path.dirname(os.getcwd()) # Path that runs correctly when we run Jupyter notebook
# ROOT_PATH = os.getcwd() # path that runs correctly when running python pipeline.py
ROOT_PATH = os.path.dirname(os.path.realpath(__file__))
RAW_FILES_PATH = os.path.join(ROOT_PATH, "data/raw")
CLEAN_FILES_PATH = os.path.join(ROOT_PATH, "data/clean")
IG_FILES_PATH = os.path.join(RAW_FILES_PATH, "ig")

COUNTRY_FILES = {"asia": "ig_asia_22-23.csv", "spain": "ig_spain_22-23.csv",
                 "belgium": "ig_belgium_22-23.csv"}
CLEAN_FILES = {"asia": "ig_clean_asia.csv", "spain": "ig_clean_spain.csv",
                 "belgium": "ig_clean_belgium.csv"}

## CONSTANTS FOR FILTERING DATA ##

PRODUCTS_VAL = ["corn", "soya", "sunflower", "wheat", "sunflower", "barley",
                "peas", "rapeseed", "sunflower", "vegetable", "soya", "canola",
                "rapeseed", "sunflower", "mixed", "wheat", "sugar beet"]

CROP_DICT =  {'Rapeseed': 'rapeseed', 'Corn': 'corn',
              'Sunflower meal': 'sunflower', 'Wheat': 'wheat',
              'Sunflower oil': 'sunflower', 'Soya beans': 'soya',
              'Barley': 'barley', 'Peas': 'peas',
              'Sunflower seed': 'sunflower', 'Vegetable oil': 'vegetable',
              'Soya oil': 'soya', 'Canola': 'canola',
              'Rapeseed meal': 'rapeseed', 'Sunflower pellets': 'sunflower',
              'Mixed': 'mixed', 'Wheat bran pellets': 'wheat',
              'Sugar beet pellets': 'sugar beet'}

HS_DICT = {"Rapeseed": "1205", "Rapeseed meal": "2306", "Canola": "1514",
           "Corn": "1005", "Sunflower oil": "1512", "Sunflower seed": "1206",
           "Sunflower pellets": "2306", "Sunflower meal": "2306",
           "Wheat": "1001", "Soya beans": "1201", "Soya oil": "1507",
           "Barley": "1003", "Peas": "0713", "Vegetable oil": "1516",
           "Wheat bran pellets": "2302", "Mixed": "",
           "Sugar beet pellets": "2302"}

HS_BSGI = {"1205": "Rapeseed", "1514": "Canola",
           "1005": "Corn", "1512": "Sunflower oil", "1206": "Sunflower seed",
           "2306": "Sunflower meal", "1001":  "Wheat", "1201": "Soya beans",
           "1507": "Soya oil", "1003":  "Barley", "0713": "Peas",
           "1516": "Vegetable oil", "2302": "Sugar beet pellets"}

SUBSIDIARY_DICT = {"enselcoagro": "Kernel Holding", "mhp": "MHP",
                   "khmilnytske": "Astarta Holding",
                   "slobozhanschynaagro": "Industrial Milk \nCompany (IMC)",
                   "nibulon": "Nibulon", "cargill": "Cargill",
                   "prykarpattya": "UkrLandFarming",
                   "louisdreyfus": "Louis Dreyfus",
                   "dobrobut": "Astarta Holding",
                   "pivdenagroinvest": "TNA Corporate \nSolutions",
                   "agroton": "Agroton Public \nLimited",
                   "kernel": "Kernel Holding",
                   "podillyaagroservice": "Kernel Holding",
                   "agroholdyngms": "System Capital \nManagement",
                   "buratagro": "Industrial Milk \nCompany (IMC)",
                   "agroprosperis": "NHC Capital",
                   "druzhbanova": "Kernel Holding",
                   "astarta": "Astarta Holding",
                   "agroprogress": "Industrial Milk \nCompany (IMC)"}