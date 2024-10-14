import os
import base64
import dotenv
import requests

import pandas as pd
from .data_prep import DataFormatter

dotenv.load_dotenv()
client_id = os.getenv('KEY')
client_secret = os.getenv('SECRET_KEY')
username= os.getenv('LOGIN_USERNAME')
password= os.getenv('PASSWORD')
token_url = 'https://api.cnptia.embrapa.br/token'

@staticmethod
def get_token():
    auth = f"{client_id}:{client_secret}"
    encoded_credentials = base64.b64encode(auth.encode()).decode()
    
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password
    }
    
    headers = {
        'Authorization': f'Basic {encoded_credentials}',
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    
    response = requests.post(token_url, headers=headers, data=data)
    
    if response.status_code == 200:
        token = response.json()['access_token']
        return token
    else:
        print(f'Erro ao obter o token: {response.status_code} - {response.text}, DATA: {data}')
        return None


class QueryService:
    def __init__(self, query_service_url = None):
        self.query_service_url = query_service_url

    def query_test(self):
        token = get_token()
        
        if token:
            headers = {
                'Authorization': f'Bearer {token}'
            }
            response = requests.get(self.query_service_url, headers=headers)
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f'Erro na consulta à API: {response.status_code} - {response.text}')
        else:
            print('Token inválido ou não foi possível obter o token.')

    def query_zarc(self, id_cultura, codigo_ibge, risco):
        token = get_token()
        
        if token:
            query_url = f"https://api.cnptia.embrapa.br/agritec/v2/zoneamento?idCultura={id_cultura}&codigoIBGE={codigo_ibge}&risco={risco}"
            headers = {
                'Authorization': f'Bearer {token}',
                'accept': 'application/json'
            }
            response = requests.get(query_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json().get('data',[])
                if data:
                    data = pd.DataFrame(data)
                    data_formated = DataFormatter.merge_dates(data=data)
                    return data_formated
                else:
                    print('Nenhum dado encontrado.')
            else:
                print(f'Erro na consulta à API: {response.status_code} - {response.text}')
        else:
            print('Token inválido ou não foi possível obter o token.')
            
    
    def get_cultivares(self, safra, id_cultura, uf, grupo, data_atualizacao):
        token = get_token()
        
        if token:
            query_url = f"https://api.cnptia.embrapa.br/agritec/v2/cultivares?safra={safra}&idCultura={id_cultura}&uf={uf}&grupo={grupo}&dataAtualizacao={data_atualizacao}"
            headers = {
                'Authorization': f'Bearer {token}',
                'accept': 'application/json'
            }
            response = requests.get(query_url, headers=headers)
            
            if response.status_code == 200:
                data = response.json().get('data',[])
                if data:
                    data = pd.DataFrame(data)
                    return data
                else:
                    print('Nenhum dado encontrado.')
            else:
                print(f'Erro na consulta à API: {response.status_code} - {response.text}')
        else:
            print('Token inválido ou não foi possível obter o token.')
    
    