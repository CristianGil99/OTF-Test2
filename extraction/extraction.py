import requests
import json
import pandas as pd

def extract(url, number_extraction):
    """
    Api implementation using request library and selecting/filtering data.
    :param url: url with the requiered data
    :param acces_token: key to access to the data
    :param list_fields: list of fields to be selected
    return Dataframe with the contact collection
    """
    after = 100*number_extraction
    payload = json.dumps({
    "properties": ["country","phone","technical_test___create_date","industry","address","hs_object_id","allowed_to_collect","raw_email"],
    "limit": 100,
    "after": str(after),
    "filterGroups": [
        {
        "filters": [
            {
            "propertyName": "allowed_to_collect",
            "operator": "EQ",
            "value": "true"
            }
        ]
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer pat-na1-3c7b0af9-bb66-40e7-a256-ce4c5eb27e81'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    response_dict = json.loads(response.text)

    return response_dict

def get_full_data(full_data_number):
    """
    Function to get all the data needed.
    :param full_data_number: Number of times the len of the data can be divided
    return Dataframe with the full contact collection
    """
    json = extract("https://api.hubapi.com/crm/v3/objects/contacts/search", 0)["results"]
    dataframe = pd.json_normalize(json)
    for i in range(1, full_data_number):
        new_json = extract("https://api.hubapi.com/crm/v3/objects/contacts/search", i)["results"]
        new_dataframe = pd.json_normalize(new_json)
        dataframe = pd.concat([dataframe, new_dataframe], ignore_index=True)      
    return dataframe