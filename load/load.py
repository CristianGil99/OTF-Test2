import requests
import json


def load_table():
    """
    Api implementation to load data.
    return Response with the succesfull data loaded
    """
    data = {
        "name": "Contact_collection",
        "dateFormat": "YEAR_MONTH_DAY",
        "files": [
            {
            "fileName": "output.csv",
            "fileFormat": "CSV",
            "fileImportPage": {
                "hasHeader": True,
                "columnMappings": [
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "Email",
                    "propertyName": "email",
                    "idColumnType": "HUBSPOT_ALTERNATE_ID"
                },
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "Country",
                    "propertyName": "country/region",
                    "idColumnType": None
                },
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "City",
                    "propertyName": "city",
                    "idColumnType": None
                },
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "Industry",
                    "propertyName": "Original Industry",
                    "idColumnType": None
                },
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "Phone",
                    "propertyName": "Phone number",
                    "idColumnType": None
                },
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "properties.technical_test___create_date",
                    "propertyName": "Original Create Date",
                    "idColumnType": None
                },
                {
                    "columnObjectTypeId": "0-1",
                    "columnName": "properties.hs_object_id",
                    "propertyName": "Temporary ID",
                    "idColumnType": None
                }
                ]
            }
            }
        ]
        }
    datastring = json.dumps(data)

    payload = {"importRequest": datastring}
    files = {'files': open("resources/output.csv", 'rb')}
    headers = {
    'Content-Type': 'application/json',
    'authorization': 'Bearer pat-na1-7ad0d2dd-1c1d-4bd3-983f-0de488f3520e' 
    }
    print(files)

    response = requests.post("https://api.hubapi.com/crm/v3/imports", data=payload, files=files, headers=headers)
    return(print(response.text.encode('utf8')))