import pandas as pd

# Ich verwende die zuvor extrahierten Gemeinde-Codes, um die relevanten Daten für unsere Gemeinden zu extrahieren.
df_codes = pd.read_csv("../data/scraped/codes.csv")
df_codes['Code'] = df_codes['Code'].astype(int)

# Header Reihen überspringen
skip_rows = list(range(0, 5)) + list(range(6, 9))
# Excel Datei einlesen
df = pd.read_excel("../data/raw/Regionalportraits.xlsx", skiprows=skip_rows)

df['Gemeindecode'] = pd.to_numeric(df['Gemeindecode'], errors='coerce')
# Alle Zeilen entfernen, die keinen Gemeindecode haben (Footer-Zeilen)
df = df.dropna(subset=['Gemeindecode'])
df['Gemeindecode'] = df['Gemeindecode'].astype(int)

# Alle Zeilen entfernen, die nicht in der Liste von Gemeinde-Codes sind
df = df[df['Gemeindecode'].isin(df_codes['Code'].tolist())]

# Spalten extrahieren, die ich später benötigen
columns_to_extract = [
    'Gemeindename',
    'Einwohner',
    '0-19 Jahre',
    '20-64 Jahre',
    '65 Jahre und mehr',
    'Anzahl Privathaushalte',
    'Gesamtfläche in km² 1)',
    'Wald und Gehölze in %'
]
df = df[columns_to_extract]

# Spalten umbenennen
df = df.rename(columns={
    'Gemeindename': 'Gemeinde',
    'Einwohner': 'Population',
    '0-19 Jahre': 'Age_0_19',
    '20-64 Jahre': 'Age_20_64',
    '65 Jahre und mehr (altersverteilungen)': 'Age_65_plus',
    'Anzahl Privathaushalte': 'Households',
    'Gesamtfläche in km² 1)': 'Total_Area_km2',
    'Wald und Gehölze in %': 'Forest_Vegetation_pct'
})

# Roverdo (GR) umbenennen damit es in allen Datensätzen gleich benannt ist
df.loc[df['Gemeinde'] == 'Roveredo (GR)', 'Gemeinde'] = 'Roveredo'

# Daten in einer CSV Datei speichern
df.to_csv('../data/scraped/regionalportraits.csv', index=False)
print(df)
