import pandas as pd

df_codes = pd.read_csv("../data/scraped/codes.csv")
df_codes['Code'] = df_codes['Code'].astype(int)

skip_rows = list(range(0, 5)) + list(range(6, 9))
df = pd.read_excel("../data/raw/Regionalportraits.xlsx", skiprows=skip_rows)

df['Gemeindecode'] = pd.to_numeric(df['Gemeindecode'], errors='coerce')
df = df.dropna(subset=['Gemeindecode'])
df['Gemeindecode'] = df['Gemeindecode'].astype(int)

df = df[df['Gemeindecode'].isin(df_codes['Code'].tolist())]

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

df.to_csv('../data/scraped/regionalportraits.csv', index=False)
print(df)
