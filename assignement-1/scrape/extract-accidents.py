import pdfplumber
import pandas as pd

PDF_PATH = "../data/raw/Verkehrsunfälle-Graubuenden.pdf"

with pdfplumber.open(PDF_PATH) as pdf:
    data = []

    for i in range(11, 14):
        page = pdf.pages[i]
        tables = page.extract_tables()
        for table in tables:
            for row in table:
                if row and len(row) >= 8:
                    gemeinde = row[0]
                    sachschaden = row[1]
                    personenschaden = row[2]
                    getoetete = row[3]
                    schwerverletzte = row[4]
                    lebensbedrohlich_verletzte = row[5]
                    erheblich_verletzte = row[6]
                    leichtverletzte = row[6]

                    if gemeinde and gemeinde not in ['Total', None, '']:
                        data.append({
                            'Gemeinde': gemeinde.strip(),
                            'Unfälle-mit-Sachschaden': sachschaden,
                            'Unfälle-mit-Personenschaden': personenschaden,
                            'Getötete': getoetete,
                            'Schwerverletzte': schwerverletzte,
                            'Lebensbedrohlich-Verletzte': lebensbedrohlich_verletzte,
                            'Erheblich-Verletzte': erheblich_verletzte
                        })

    df = pd.DataFrame(data)
    numeric_cols = df.columns.drop('Gemeinde')
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Roverdo (GR) umbenennen damit es in allen Datensätzen gleich benannt ist
    df.loc[df['Gemeinde'] == 'Roveredo (GR)', 'Gemeinde'] = 'Roveredo'

    # Tschiertschen-Praden hat im Jahr 2025 mit Chur fusioniert
    # Da dieser Datensatz vom Jahr 2023 ist muss diese Fusionierung hier manuell nachgeführt werden
    tschi = df.loc[df['Gemeinde'] == 'Tschiertschen-Praden']
    if not tschi.empty:
        numeric_cols = df.columns.drop('Gemeinde')
        df.loc[df['Gemeinde'] == 'Chur', numeric_cols] += tschi[numeric_cols].iloc[0]
        df = df[df['Gemeinde'] != 'Tschiertschen-Praden'].reset_index(drop=True)

    df.to_csv('../data/scraped/accidents.csv', index=False)
    print(df.head())
