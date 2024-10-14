import pandas as pd

class DataFormatter:
    @staticmethod
    def merge_dates(data):
        df = data.copy()
        df['dataIni'] = pd.to_datetime(df['safraIni'].astype(str) + '-' + df['mesIni'].astype(str) + '-' + df['diaIni'].astype(str))
        df['dataFim'] = pd.to_datetime(df['safraIni'].astype(str) + '-' + df['mesFim'].astype(str) + '-' + df['diaFim'].astype(str))
        df['safra'] = df['safraIni'].astype(str) + '/' + df['safraFim'].astype(str)
        
        df.drop(columns=['safraIni', 'mesIni', 'diaIni', 'safraFim', 'mesFim', 'diaFim'], inplace=True)
        return df