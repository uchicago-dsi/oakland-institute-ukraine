import os

ROOT_PATH = os.getcwd()
IG_FILES_PATH = os.path.join(ROOT_PATH, "data/ig")
COUNTRY_FILES = {"asia": "ig_asia_22-23.csv", "spain": "ig_spain_22-23.csv",
                 "belgium": "ig_belgium_22-23.csv"}
CLEAN_FILES = {"asia": "ig_clean_asia.csv", "spain": "ig_clean_spain.csv",
                 "belgium": "ig_clean_belgium.csv"}