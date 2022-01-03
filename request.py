import requests
import pandas as pd
import os
import datetime

año = datetime.date.today().year
mes = datetime.date.today().month
dia = datetime.date.today().day

MESES = {1:'enero',
        2:'febrero',
        3:'marzo',
        4:'abril',
        5:'mayo',
        6:'junio',
        7:'julio',
        8:'agosto',
        9:'septiembre',
        10:'octubre',
        11:'noviembre',
        12:'diciembre'}

urls = {
    'museos':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos.csv',
    'salas_de_cine':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/392ce1a8-ef11-4776-b280-6f1c7fae16ae/download/cine.csv',
    'biblotecas_populares':'https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv'
    }

def download_and_save():

    try:
        for key in urls:
            url = urls[key]
            r = requests.get(url)

            año_mes_ruta = f'{key}/{año}-{MESES[mes]}'
            if not os.path.exists(año_mes_ruta):
                os.mkdir(año_mes_ruta)

            if os.path.isfile(f'{key}-{dia}-{mes}-{año}.csv') == True:
                os.remove(f'{key}-{dia}-{mes}-{año}.csv')

            open(f'{key}/{año}-{MESES[mes]}/{key}-{dia}-{mes}-{año}.csv', 'wb').write(r.content)

    except:
        pass

    dfs = {}

    dfs['museos'] = pd.read_csv(f'museos/{año}-{MESES[mes]}/museos-{dia}-{mes}-{año}.csv', encoding='ISO 8859-1')
    dfs['salas_de_cine'] = pd.read_csv(f'salas_de_cine/{año}-{MESES[mes]}/salas_de_cine-{dia}-{mes}-{año}.csv')
    dfs['biblotecas_populares'] = pd.read_csv(f'biblotecas_populares/{año}-{MESES[mes]}/biblotecas_populares-{dia}-{mes}-{año}.csv')

    return dfs