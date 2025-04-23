import pdfplumber
import pandas as pd
import re

# Um bei den Regionalportraits und der API die relevanten Daten für unsere Gemeinden zu extrahieren
# benötigen wir die Gemeinde-Codes. Ich habe die Zuordnung der Gemeinde-Codes zu den Gemeinden in einem
# PDF auf der Webseite des Kantons GR gefunden und werde diese hier extrahieren.

PDF_PATH = "../data/raw/Gemeinde-Codes.pdf"

rows = []

# Regex Pattern um die Gemeinde-Codes und Namen zu extrahieren.
# Das regex Pattern hat 2 Capture Groups:
# (\d{3,4}): Fängt den Gemeinde-Code ein welcher 3-4 Ziffern hat (Capture Group 1).
# \s+: Ein oder mehrere Leerzeichen (wird nicht gespeichert).
# ([^\d\n]+?): Fängt den Gemeinde-Namen (Capture Group 2).
# (?=\s+\d{3,4}|$): Danach folgt entweder eine weiter Gemeindecode oder das Ende der Zeile (wird nicht gespeichert).
# Der letzte Ausdruck ist wichtig damit das Pattern mehre Gemeinde Codes in derselben Zeile erkennt.
pattern = re.compile(r'(\d{3,4})\s+([^\d\n]+?)(?=\s+\d{3,4}|$)')

with pdfplumber.open(PDF_PATH) as pdf:
    # Alle Codes befinden sich auf der ersten Seite
    page = pdf.pages[0]
    text = page.extract_text()
    if text:
        lines = text.split("\n")
        for line in lines:
            # Regex anwenden
            matches = pattern.findall(line)
            # Daten in die Liste einfügen
            if matches:
                for code, name in matches:
                    name = name.strip()
                    rows.append({"Code": code, "Gemeinde": name})

df = pd.DataFrame(rows)
df['Code'] = df['Code'].astype(int)

# Daten in einer CSV Datei speichern
df.to_csv('../data/scraped/codes.csv', index=False)
print(df.head())
