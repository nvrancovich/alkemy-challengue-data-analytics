from request.request import download_and_save
from process.process import normalize
from models.models import Base, provincia_categoria_conteo, registros_totales, fuentes_conteo, cines_suma
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from logger.logger import log
from decouple import config
import sys

HOST = config('HOST')
DB = config('DB')
USER = config('USER')
PASS = config('PASS')

print(HOST, DB, USER, PASS)

if __name__ == '__main__':

    # Se descargan las tablas y se guardan en sus respectivos directorios

    dfs = download_and_save()

    # Se procesan las tablas para generar una tabla normalizada y se hacen las consultas requeridas

    df_cines_suma1, df_provincia_categoría, df_registros_totales, df_fuente = normalize(dfs)

    # Se exportan las tablas equivalentes a las consultas requeridas a una base de datos PostgreSQL

    try:
        engine = create_engine(f'postgresql://{USER}:{PASS}@{HOST}/{DB}')
        Session = sessionmaker(engine)
        session = Session()

        log.debug('Se creo una sesión para subir las tablas a la base de datos alkemy en PostgreSQL')

        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)

        for i in df_registros_totales.index:
            session.add(registros_totales(categoria=df_registros_totales['categoría'][i],
                                          conteo=int(df_registros_totales['conteo'][i])))

        for i in df_provincia_categoría.index:
            session.add(provincia_categoria_conteo(provincia=df_provincia_categoría['provincia'][i],
                                                   categoria=df_provincia_categoría['categoría'][i],
                                                   conteo=int(df_provincia_categoría['conteo'][i])))

        for i in df_fuente.index:
            session.add(fuentes_conteo(fuente=df_fuente['fuente'][i],
                                       conteo=int(df_fuente['conteo'][i])))

        for i in df_cines_suma1.index:
            session.add(cines_suma(provincia=df_cines_suma1['provincia'][i],
                                   pantallas=int(df_cines_suma1['pantallas'][i]),
                                   butacas=int(df_cines_suma1['butacas'][i]),
                                   espacio_INCAA=int(df_cines_suma1['espacio_INCAA'][i])))

        # Se suben los cambios en las tablas y se cierra la sesion

        session.commit()
        session.close()
        log.debug(f'Se cerró la conexión y el programa se ejecuto correctamente')
    except Exception as e:
        log.debug(f'Hubo un problema y la conexión a la base de datos falló. El error: {e}')
        