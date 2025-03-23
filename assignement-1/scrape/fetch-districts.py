import io
import json
import requests
import pandas as pd
from pyjstat import pyjstat

# Ich verwende die zuvor extrahierten Gemeinde-Codes, um die relevanten Daten für unsere Gemeinden zu extrahieren.
df_codes = pd.read_csv("../data/scraped/codes.csv")
municipality_codes = df_codes['Code'].astype(str).tolist()

# Die Query kann unter folgendem Link erstellt werden und dann in den Code kopiert werden:
# https://www.pxweb.bfs.admin.ch/pxweb/en/px-x-0202020000_102/-/px-x-0202020000_102.px/
# Achtung für die Gemeinden verwende ich die extrahierten Gemeinde-Codes
query = {
    "query": [
        {
            "code": "Bezirk (>>) / Gemeinde (......)",
            "selection": {
                "filter": "item",
                # Gemeinde-Codes hier einfügen
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

# API-Endpoint
url = "https://www.pxweb.bfs.admin.ch/api/v1/en/px-x-0202020000_102/px-x-0202020000_102.px"

# Anfrage an die API senden
response = requests.post(url, json=query)
response.raise_for_status()
data = response.json()

# JSON in einen dataframe umwandeln
json_stream = io.StringIO(json.dumps(data))
dataset = pyjstat.Dataset.read(json_stream)
df = dataset.write('dataframe')
df = pd.DataFrame(df)

# Spalten extrahieren, die ich später benötigen
df = df[['District (>>) / Commune (......)', 'value']]
# Spalten umbenennen
df = df.rename(columns={
    'District (>>) / Commune (......)': 'Gemeinde',
    'value': 'Strassenflaeche-Hektar'
})

# Gemeinde-Namen bereinigen
df['Gemeinde'] = df['Gemeinde'].str.strip().str.replace(r'^\.*', '', regex=True)

# Roverdo (GR) umbenennen damit es in allen Datensätzen gleich benannt ist
df.loc[df['Gemeinde'] == 'Roveredo (GR)', 'Gemeinde'] = 'Roveredo'

# Daten in einer CSV Datei speichern
df.to_csv('../data/scraped/streets.csv', index=False)
print(df.head())
