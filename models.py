from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

Base = declarative_base()

class provincia_categoria_conteo(Base):
    __tablename__ = 'provincia_categoria_conteo'
    
    provincia = Column(String(), primary_key=True)
    categoria = Column(String(), primary_key=True)
    conteo = Column(Integer())
    fecha_carga = Column(DateTime(), default=datetime.now())

class registros_totales(Base):
    __tablename__ = 'registros_totales'
    
    categoria = Column(String(), primary_key=True)
    conteo = Column(Integer())
    fecha_carga = Column(DateTime(), default=datetime.now())
    
class fuentes_conteo(Base):
    __tablename__ = 'fuentes_conteo'
    
    fuente = Column(String(), primary_key=True)
    conteo = Column(Integer())
    fecha_carga = Column(DateTime(), default=datetime.now())

class cines_suma(Base):
    __tablename__ = 'cines_suma'
    
    provincia = Column(String(), primary_key=True)
    pantallas = Column(Integer())
    butacas = Column(Integer())
    espacio_INCAA = Column(Integer())
    fecha_carga = Column(DateTime(), default=datetime.now())