import pyodbc 
from connection import *

#SELECT QUERIES
query_select_estados='SELECT * FROM estados'
query_select_municipios='SELECT * FROM municipios'
query_select_cines='SELECT * FROM cines'
query_select_peliculas='SELECT * FROM peliculas'

#ADD QUERIES
query_insert_estados="insert into estados values('Nuevo Leon')"

#UPDATE QUERIES

#DELETE QUERIES

conn = pyodbc.connect(
    "DSN=SQLExpressODBC",
    autocommit=True
)

if conn:
    print("We're connected")
    new_data=Connection.add(conn,query_insert_estados)
    data_estados=Connection.read(conn,query_select_estados)
    print(data_estados)

else: 
    print("You're not connected")