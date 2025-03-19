import pdfplumber
import pandas as pd
import re

PDF_PATH = "../data/raw/Gemeinde-Codes.pdf"

rows = []

pattern = re.compile(r'(\d{3,4})\s+([^\d\n]+?)(?=\s+\d{3,4}|$)')

with pdfplumber.open(PDF_PATH) as pdf:
    page = pdf.pages[0]
    text = page.extract_text()
    if text:
        lines = text.split("\n")
        for line in lines:
            matches = pattern.findall(line)
            if matches:
                for code, name in matches:
                    name = name.strip()
                    rows.append({"Code": code, "Gemeinde": name})

df = pd.DataFrame(rows)
df['Code'] = df['Code'].astype(int)
df.to_csv('../data/scraped/codes.csv', index=False)
print(df.head())
