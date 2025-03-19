import io
import json
import requests
import pandas as pd
from pyjstat import pyjstat

df_codes = pd.read_csv("../data/scraped/codes.csv")
municipality_codes = df_codes['Code'].astype(str).tolist()

query = {
    "query": [
        {
            "code": "Bezirk (>>) / Gemeinde (......)",
            "selection": {
                "filter": "item",
                "values": municipality_codes
            }
        },
        {
            "code": "Standardnomenklatur (NOAS04)",
            "selection": {
                "filter": "item",
                "values": [
                    "10030600"
                ]
            }
        },
        {
            "code": "Periode",
            "selection": {
                "filter": "item",
                "values": [
                    "2013/18"
                ]
            }
        }
    ],
    "response": {
        "format": "json-stat"
    }
}

url = "https://www.pxweb.bfs.admin.ch/api/v1/en/px-x-0202020000_102/px-x-0202020000_102.px"

response = requests.post(url, json=query)
response.raise_for_status()
data = response.json()

json_stream = io.StringIO(json.dumps(data))

dataset = pyjstat.Dataset.read(json_stream)
df = dataset.write('dataframe')
df = pd.DataFrame(df)

df = df[['District (>>) / Commune (......)', 'value']]

df = df.rename(columns={
    'District (>>) / Commune (......)': 'Gemeinde',
    'value': 'Strassenflaeche-Hektar'
})

df['Gemeinde'] = df['Gemeinde'].str.strip().str.replace(r'^\.*', '', regex=True)

# Roverdo (GR) umbenennen damit es in allen Datensätzen gleich benannt ist
df.loc[df['Gemeinde'] == 'Roveredo (GR)', 'Gemeinde'] = 'Roveredo'

df.to_csv('../data/scraped/streets.csv', index=False)
print(df.head())
