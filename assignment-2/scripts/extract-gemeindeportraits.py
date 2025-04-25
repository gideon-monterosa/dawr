import pandas as pd

# Ich verwende die zuvor extrahierten Gemeinde-Codes, um die relevanten Daten für unsere Gemeinden zu extrahieren.
df_codes = pd.read_csv("./data/codes.csv")
df_codes["Code"] = df_codes["Code"].astype(int)

# Header Reihen überspringen
skip_rows = list(range(0, 5)) + list(range(6, 9))
# Excel Datei einlesen
df = pd.read_excel("./data/raw/GemeindePortraits2021.xlsx", skiprows=skip_rows)

df["Gemeindecode"] = pd.to_numeric(df["Gemeindecode"], errors="coerce")
# Alle Zeilen entfernen, die keinen Gemeindecode haben (Footer-Zeilen)
df = df.dropna(subset=["Gemeindecode"])
df["Gemeindecode"] = df["Gemeindecode"].astype(int)

# Alle Zeilen entfernen, die nicht in der Liste von Gemeinde-Codes sind
df = df[df["Gemeindecode"].isin(df_codes["Code"].tolist())]

# Spalten entfernen die einen starken Einfluss auf das erste Assignment hatten
df = df.drop(
    columns=[
        "Wald und Gehölze in %",
    ]
)

# Spalten umbenennen
df = df.rename(
    columns={
        "Gemeindename": "Gemeinde",
        "Einwohner": "Einwohner",
        "Veränderung in %": "Einwohner_Veraenderung_Prozent",
        "Bevölkerungs-dichte pro km²": "Bevoelkerungsdichte_km2",
        "Ausländer in %": "Auslaender_Prozent",
        "0-19 Jahre": "Alter_0_19_Jahre",
        "20-64 Jahre": "Alter_20_64_Jahre",
        "65 Jahre und mehr": "Alter_65_Plus_Jahre",
        "Rohe Heiratssziffer": "Heiratsziffer",
        "Rohe Scheidungsziffer": "Scheidungsziffer",
        "Rohe Geburtenziffer": "Geburtenziffer",
        "Rohe Sterbeziffer": "Sterbeziffer",
        "Anzahl Privathaushalte": "Privathaushalte_Anzahl",
        "Durchschnittliche Haushaltsgrösse in Personen": "Haushaltsgroesse_Durchschnitt",
        "Gesamtfläche in km² 1)": "Flaeche_Total_km2",
        "Siedlungsfläche in %": "Flaeche_Siedlung_Prozent",
        "Veränderung in ha": "Flaeche_Siedlung_Veraenderung_ha",
        "Landwirtschafts-fläche in %": "Flaeche_Landwirtschaft_Prozent",
        "Veränderung in ha.1": "Flaeche_Landwirtschaft_Veraenderung_ha",
        "Wald und Gehölze in %": "Flaeche_Wald_Prozent",
        "Unproduktive Fläche in %": "Flaeche_Unproduktiv_Prozent",
        "Beschäftigte total": "Beschaeftigte_Total",
        "im 1. Sektor": "Beschaeftigte_Sektor1",
        "im 2. Sektor": "Beschaeftigte_Sektor2",
        "im 3. Sektor": "Beschaeftigte_Sektor3",
        "Arbeitsstätten total": "Arbeitsstaetten_Total",
        "im 1. Sektor.1": "Arbeitsstaetten_Sektor1",
        "im 2. Sektor.1": "Arbeitsstaetten_Sektor2",
        "im 3. Sektor.1": "Arbeitsstaetten_Sektor3",
        "Leerwohnungs-ziffer": "Leerwohnungsziffer",
        "Neu gebaute Wohnungen pro 1000 Einwohner": "Neubauwohnungen_pro_1000_Einwohner",
        "Sozialhilfequote": "Sozialhilfequote",
    }
)

print(df.columns)

# TODO: evt könnten die Fehlenden Werte sinnvoll mit tabpfn predicted werden
# Fehlende Werte mit 0 ersetzen
df = df.replace("X", 0)

# Roverdo (GR) umbenennen damit es in allen Datensätzen gleich benannt ist
df.loc[df["Gemeinde"] == "Roveredo (GR)", "Gemeinde"] = "Roveredo"

# Daten in einer CSV Datei speichern
df.to_csv("./data/regionalportraits.csv", index=False)
print(df)
