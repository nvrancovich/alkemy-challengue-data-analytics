import pandas as pd
import numpy as np
from logger.logger import log

def normalize(dfs):

    # Preparando la tabla museos

    dfs['museos']['id_departamento'] = np.nan
    dfs['museos']['categoría'] = 'Museos'

    df_museos = dfs['museos'][['localidad_id','provincia_id','id_departamento','categoría','provincia','localidad','nombre',
              'direccion','codigo_postal','telefono','mail','web','fuente']]

    df_museos = df_museos.rename(columns = {'localidad_id':'cod_localidad',
                                            'provincia_id':'id_provincia',
                                            'direccion':'domicilio',
                                            'telefono':'número_de_telefono',
                                            'codigo_postal':'código_postal'}, inplace = False)

    # Preparando la tabla cines

    df_salas_de_cine = dfs['salas_de_cine'][['Cod_Loc','IdProvincia','IdDepartamento','Categoría','Provincia','Localidad','Nombre',
              'Dirección','CP','Teléfono','Mail','Web','Fuente']]

    df_salas_de_cine = df_salas_de_cine.rename(columns = {'Cod_Loc':'cod_localidad',
                                                          'IdProvincia':'id_provincia',
                                                          'IdDepartamento':'id_departamento',
                                                          'Categoría':'categoría',
                                                          'Provincia':'provincia',
                                                          'Localidad':'localidad',
                                                          'Nombre':'nombre',
                                                          'Dirección':'domicilio',
                                                          'CP':'código_postal',
                                                          'Teléfono':'número_de_telefono',
                                                          'Mail':'mail',
                                                          'Web':'web',
                                                          'Fuente':'fuente'}, inplace = False)

    # Preparando la tabla biblotecas

    df_biblotecas = dfs['biblotecas_populares'][['Cod_Loc','IdProvincia','IdDepartamento','Categoría','Provincia','Localidad','Nombre',
              'Domicilio','CP','Teléfono','Mail','Web','Fuente']]
    df_biblotecas = df_biblotecas.rename(columns = {'Cod_Loc':'cod_localidad',
                                                    'IdProvincia':'id_provincia',
                                                    'IdDepartamento':'id_departamento',
                                                    'Categoría':'categoría',
                                                    'Provincia':'provincia',
                                                    'Localidad':'localidad',
                                                    'Nombre':'nombre',
                                                    'Domicilio':'domicilio',
                                                    'CP':'código_postal',
                                                    'Teléfono':'número_de_telefono',
                                                    'Mail':'mail',
                                                    'Web':'web',
                                                    'Fuente':'fuente'}, inplace = False)

    # Armando una tabla normalizada con todos los registros

    df_normalizada = df_biblotecas.append(df_salas_de_cine).append(df_museos)
    df_normalizada = df_normalizada.replace('s/d',np.nan)
    df_normalizada = df_normalizada.replace('',np.nan)
    df_normalizada = df_normalizada.astype(object)
    df_normalizada['conteo'] = 1

    log.info('Se normalizaron las tablas descargadas')

    # Armando la tabla de registros totales por categoría

    df_registros_totales = df_normalizada.groupby('categoría').sum(['conteo'])

    # Armando la tabla de registros totales por provincia y categoría

    df_provincia_categoría = df_normalizada.groupby(['provincia','categoría']).sum(['conteo'])

    # Armando la tabla de registros totales por fuente

    df_fuente = df_normalizada.groupby(['fuente']).sum(['conteo'])

    # Armando la tabla de cantidad de pantallas, butacas y espacios INCAA por provincia

    df_cines_suma = dfs['salas_de_cine'][['Provincia','Pantallas','Butacas','espacio_INCAA']].convert_dtypes()
    df_cines_suma = df_cines_suma.rename(columns = {'Pantallas':'pantallas',
                                                   'Butacas':'butacas',
                                                   'Provincia':'provincia'},inplace = False)
    df_cines_suma1 = df_cines_suma.groupby(['provincia']).sum(['pantallas','butacas'])
    df_cines_suma2 = df_cines_suma[['provincia','espacio_INCAA']].replace('',np.nan).groupby(['provincia']).count()
    df_cines_suma1['espacio_INCAA'] = df_cines_suma2
    df_cines_suma1

    # Reiniciando todos los índices

    df_cines_suma1 = df_cines_suma1.reset_index()
    df_provincia_categoría = df_provincia_categoría.reset_index()
    df_registros_totales = df_registros_totales.reset_index()
    df_fuente = df_fuente.reset_index()

    log.info('Se crearon las tablas con las consultas requeridas')

    return df_cines_suma1, df_provincia_categoría, df_registros_totales, df_fuente