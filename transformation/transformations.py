import pycountry
from geopy.geocoders import Nominatim
import re
import pandas as pd
def findCountry (location_name):
    """
    Function to get the country and city acording to the location.
    :param location: location that can be a country or a City
    return Tuple with the country and city related to the location
    """
    geo = Nominatim(user_agent="MyApp")
    if location_name != None:
        loct = geo.geocode(location_name)
        location = geo.reverse(loct[1])    
        if location.raw["address"]["country"] == "United Kingdom":
                country = location.raw["address"]["state"]
        else:
             country = location.raw["address"]["country"]
        return [country, location_name if location_name != country else ""]
    else:
        return ["", ""]

def exctract_email (email):
    """
    Function to get the clear Name and Email.
    :param email: raw email 
    return Tuble with the name and the email 
    """
    new_email = re.search(r'[\w.+-]+@[\w-]+\.[\w.-]+', email)
    name = re.search(r'[\w]+[^ ]', email)
    return [new_email.group(0), name.group(0)]

def Delete_duplicates (dataframe):
    """
    Function to delete duplicates by name and email
    :param email: dataframe with all the information
    return Dataframe without any duplicate
    """
    df = dataframe.sort_values('properties.createdate', ascending=False).groupby('Name', as_index=False).first()
    df2 = dataframe.sort_values('properties.createdate', ascending=False).groupby('Name')['properties.industry'].apply(lambda x: ';'.join(x)).reset_index()
    df3 = pd.merge(df,df2, left_on = 'Name', right_on = 'Name', how = 'inner')
    df = df3.sort_values('properties.createdate', ascending=False).groupby('Email', as_index=False).first()
    df2 = df3.sort_values('properties.createdate', ascending=False).groupby('Email')['properties.industry_y'].apply(lambda x: ';'.join(x)).reset_index()
    for i in range(len(df2)):
        if df2.loc[i, 'properties.industry_y'] != None:
            sin_comas = df2.loc[i, 'properties.industry_y'].split(";")
            df2.loc[i, "Industry"] = ';'.join(set(sin_comas))
        else:
            df2.loc[i, "Industry"] = ""
    df3 = pd.merge(df,df2, left_on = 'Email', right_on = 'Email', how = 'inner')
    for i in range(len(df3)):
        if df3.loc[i, 'Industry'] != None and len(df3.loc[i, 'Industry'].split(";")) > 1:
            df3.loc[i, 'Industry'] =';' + df3.loc[i, 'Industry']
        elif df3.loc[i, 'Industry'] == None:
             df3.loc[i, 'Industry'] = ""
        else:
            df3.loc[i, "Industry"] = df3.loc[i, "Industry"]
    return df3[["id", "Name", "Email", "properties.country", "properties.phone", "Industry", "properties.technical_test___create_date", "properties.hs_object_id"]]

def get_phone_number (dataframe):
    """
    Function to delete duplicates by name and email
    :param email: dataframe with all the information
    return Dataframe without any duplicate
    """
    dataframe["Phone_1"] = dataframe["properties.phone"].str.replace('-','')
    prefijo = pd.read_csv('resources/paises.csv') 
    for i in range(len(dataframe)):
        if dataframe.loc[i, "Phone_1"] != None:
            dataframe.loc[i, "Phone_1"] = dataframe.loc[i, "Phone_1"].lstrip('0')
        else:
            dataframe.loc[i, "Phone_1"] = ""
    dataframe_1 = pd.merge(dataframe,prefijo, left_on = 'Country', right_on = 'ENGLISH', how = 'inner')
    dataframe_1["Phone"] = dataframe_1[["PHONE_CODE", "Phone_1"]].apply(lambda x: ") ".join(x), axis =1)
    dataframe_1['Phone'] = '(+' + dataframe_1['Phone'].astype(str)
    return dataframe_1[["id", "Name", "Email", "Country", "City", "Industry", "Phone", "properties.technical_test___create_date", "properties.hs_object_id"]]



