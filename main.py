import pyodbc 
from connection import *

#SELECT QUERIES
query_select_estados='select * from estados'
query_select_municipios='select * from municipios'
query_select_peliculas='select * from peliculas'

#ADD QUERIES
query_insert_estados="insert into estados values('Nuevo Leon')"

#UPDATE QUERIES
query_update_estados="update estados set estado_nombre = 'Nuevo Leon' where id_estado=1"
#DELETE QUERIES

#QUERY VISTAS
query_vista_cartelera_actual="select * from vistaCarteleraActual"
query_vista_usuarios = "select * from vistaUsuarios"

conn = pyodbc.connect(
    "DSN=SQLExpressODBC",
    autocommit=True
)

if conn:
    print("We're connected")
    data_cartelera_disponible=Connection.read(conn,query_vista_cartelera_actual)
    data_usuarios_disponible=Connection.read(conn,query_vista_usuarios)
    print(data_cartelera_disponible)
    print(data_usuarios_disponible)

else: 
    print("You're not connected")

def log_in(entrada_usuario,entrada_password,data_usuarios_disponible):
    usuario_encontrado=''
    for i in range(len(data_usuarios_disponible)):
        if data_usuarios_disponible[i][2]==entrada_usuario:
            usuario_encontrado=data_usuarios_disponible[i]
    print('Usuario encontrado: ',usuario_encontrado)
    if usuario_encontrado == '':
        print('Usuario es inexistente, intente de nuevo')
        return 0
    else:
        if usuario_encontrado[3]==entrada_password:
            return usuario_encontrado
        else:
            print('La contraseña es incorrecta, intente de nuevo')
            return 0


def seleccion_menu(tipo_usuario):
    if(tipo_usuario == 1):
        pass
    else:
        pass

def menu_administrador(data_admin):
    print("Bienvenido Admin: ",data_admin[0]," ",data_admin[1])
    print("Sucursal: ", data_admin[5])
    print("Usuario es admin")

def menu_cliente(data_customer):
    print("Usuario es cliente")

encontrado = 1
while (encontrado != 0):
    entrada_usuario=int(input('Ingrese su usuario o "0" para salir: '))
    if entrada_usuario == 0:
        print('Gracias por utilizar nuestro servicio, vuelva pronto')
        break
    else:
        entrada_password=input('Ingrese su contraseña: ')
        encontrado=log_in(entrada_usuario,entrada_password,data_usuarios_disponible)
        print(encontrado)
        if encontrado != 0:
            if encontrado[6] == 1:
                menu_administrador(encontrado)
            else:
                menu_cliente(encontrado)
        else:
            print('Intente de nuevo o ingrese "0" para salir')        