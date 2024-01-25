import os

# ROOT_PATH = os.path.dirname(os.getcwd()) # Path that runs correctly when we run Jupyter notebook
ROOT_PATH = os.getcwd() # path that runs correctly when running python pipeline.py
IG_FILES_PATH = os.path.join(ROOT_PATH, "data/ig")
COUNTRY_FILES = {"asia": "ig_asia_22-23.csv", "spain": "ig_spain_22-23.csv",
                 "belgium": "ig_belgium_22-23.csv"}
CLEAN_FILES = {"asia": "ig_clean_asia.csv", "spain": "ig_clean_spain.csv",
                 "belgium": "ig_clean_belgium.csv"}