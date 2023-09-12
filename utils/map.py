# Name: Josemaria Macedo Carrillo
# Title: Map
# Created: 07/26/23
# Last modified: 
# DSI

import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import matplotlib.pyplot as plt

def filter_country(locations, country_df):
    """
    Get location data from Land Matrix for Ukraine

    Inputs:
        locations (DataFrame): dataframe with coordinates data
        country_df (DataFrame): dataframe with country data

    Returns (DataFrame): dataframe with Ukrainian land locations
    """

    locations_c = locations.copy()
    deals_c = country_df.copy()
    
    # Remove NAs first from "Point" column
    locations_c = locations_c.dropna(subset = ["Point"])

    # Create new column with point list split by comma
    locations_c.loc[:, "point_lst"] = locations_c.loc[:, "Point"].str.split(",")

    # Filter Ukrainian lands
    deals_c.loc[:, "country_low"] = deals_c.loc[:, "Target country"].str.lower()
    deals_c = deals_c.loc[deals_c.loc[:, "country_low"].str.contains("ukraine", na=False), ["Deal ID"]]
    final = deals_c.merge(locations_c, on="Deal ID")

    return final

def plot_map(location_data, shape_file):
    """
    Map the land holding locations in Ukraine for different companies

    Inputs:
        location_data (DataFrame): dataframe with location data (coordinates)
        shape_file (GeoDataFrame): geodataframe with Ukrainian administrative
            divisions at the 'hromada' (municipality) level
    
    Return: None. Plots map with land locations.
    """
    
    # Define coordinate reference system standard
    crs = {'init':'epsg:4326'}

    # Create list of Point objects  
    geometry = []

    for coordinate in location_data.loc[:, "point_lst"]:
        latitude, longitude = coordinate
        geometry.append(Point(float(longitude), float(latitude)))

    lands = gpd.GeoDataFrame(location_data, crs = crs, geometry = geometry)

    # PENDING: Add region names and map title later
    fig, ax = plt.subplots(figsize=(15,15))
    shape_file.plot(ax=ax, color='grey')
    lands.plot(ax=ax, markersize=5, color="blue", marker="o")

def top_subsidiaries(data, company, top_k):
    """
    Get top k subsidiaries based of parent company based on land size of deal

    Inputs:
        data (DataFrame): dataset with companies' data
        company (str): parent company name
        top_k (int): maximum number of subsidiaries related to parent company
            you want to display
    
    Returns (array): array with top k subsidiaries
    """
    data_c = data.copy()
    company = company.lower()
    column_name = company + "_bool"
    data_c[column_name] = data_c["Top parent companies"].str.lower().str.contains(company, na=False)

    data_c = data_c.loc[data_c.loc[:, column_name] == True]

    data_g = data_c.loc[:, ["Operating company: Name", "Deal size"]].groupby(["Operating company: Name"])
    data_g = data_g.sum().reset_index().sort_values(by="Deal size", ascending=False)

    return data_g["Operating company: Name"].unique()[:top_k]

def top_parent(data, top_k):
    """
    Get top k parent companies based on land size of deal

    Inputs:
        data (DataFrame): dataset with companies' data
        top_k (int): maximum number of subsidiaries related to parent company
            you want to display
    
    Returns (array): array with top k parent companies
    """
    
    data_g = data.loc[:, ["Top parent companies", "Deal size"]].groupby(["Top parent companies"])
    data_g = data_g.sum().reset_index().sort_values(by="Deal size", ascending=False)

    return data_g["Top parent companies"].unique()[:top_k]