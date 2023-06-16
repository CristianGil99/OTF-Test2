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
    return new_email.group(0)

def Delete_duplicates (dataframe):
    """
    Function to delete duplicates by name and email
    :param email: dataframe with all the information
    return Dataframe without any duplicate
    """
    dataframe["Name"] = dataframe["properties.firstname"] + " " + dataframe["properties.lastname"]
    email_df = dataframe[dataframe["Email"] != ""].sort_values('properties.createdate', ascending=False).groupby('Email', as_index=False).first()
    email_industry_df = dataframe[dataframe["Email"] != ""].sort_values('properties.createdate', ascending=False).groupby('Email')['properties.industry'].apply(lambda x: ';'.join(x)).reset_index()
    full_email_df = pd.merge(email_df,email_industry_df, left_on = 'Email', right_on = 'Email', how = 'inner')
    full_email_df = full_email_df[["id", "Name", "Email", "properties.country", "properties.phone", "properties.address","properties.industry_y", "properties.technical_test___create_date", "properties.hs_object_id", 'properties.createdate']]
    name_df = dataframe[dataframe["Email"] == ""].sort_values('properties.createdate', ascending=False).groupby('Name', as_index=False).first()
    name_industry_df = dataframe[dataframe["Email"] == ""].sort_values('properties.createdate', ascending=False).groupby('Name')['properties.industry'].apply(lambda x: ';'.join(x)).reset_index()
    full_name_df = pd.merge(name_df,name_industry_df, left_on = 'Name', right_on = 'Name', how = 'inner')
    full_name_df = full_name_df[["id", "Name", "Email", "properties.country", "properties.phone", "properties.address", "properties.industry_y", "properties.technical_test___create_date", "properties.hs_object_id", 'properties.createdate']]
    final_df = pd.concat([full_email_df, full_name_df])
    final_df["Email"] = final_df["Email"].replace('', None)
    final1_df = final_df.sort_values('properties.createdate', ascending=False).groupby('Name', as_index=False).first()
    final2_df = final_df.sort_values('properties.createdate', ascending=False).groupby('Name')['properties.industry_y'].apply(lambda x: ';'.join(x)).reset_index()
    full_final_df = pd.merge(final1_df,final2_df, left_on = 'Name', right_on = 'Name', how = 'inner')
    for i in range(len(full_final_df)):
        if full_final_df.loc[i, 'properties.industry_y_y'] != None:
            sin_comas = full_final_df.loc[i, 'properties.industry_y_y'].split(";")
            full_final_df.loc[i, "Industry"] = ';'.join(set(sin_comas))
        else:
            full_final_df.loc[i, "Industry"] = ""
    for i in range(len(full_final_df)):
        if full_final_df.loc[i, 'Industry'] != None and len(full_final_df.loc[i, 'Industry'].split(";")) > 1:
            full_final_df.loc[i, 'Industry'] =';' + full_final_df.loc[i, 'Industry']
        elif full_final_df.loc[i, 'Industry'] == None:
             full_final_df.loc[i, 'Industry'] = ""
        else:
            full_final_df.loc[i, "Industry"] = full_final_df.loc[i, "Industry"]
    return full_final_df[["id", "Name", "Email", "properties.country", "properties.phone", "properties.address", "Industry", "properties.technical_test___create_date", "properties.hs_object_id",'properties.createdate']]

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
    return dataframe_1[["Email", "Country", "City", "Industry", "Phone", "properties.technical_test___create_date", "properties.hs_object_id"]]



