#Author: Emanuel Camarena
#Slack: emanuelc.dev

import pyodbc 
from connection import *
from datetime import date, datetime

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
    data_peliculas=Connection.read(conn,'select peliculas_nombre from peliculas')
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

#Resuelve la hora a la que será la película
def get_time(duration_time,movie_schedule):
    new_time = []
    if duration_time[1] + int(movie_schedule[6])> 59:
        time_temp = duration_time[1] + int(movie_schedule[6])
        time_temp -= 60
        duration_time[0] += 1
        new_time.append(duration_time[0]+int(movie_schedule[6]))
        new_time.append(time_temp)
        return new_time
    else:
        new_time.append(duration_time[0]+int(movie_schedule[6]))
        new_time.append(duration_time[1]+int(movie_schedule[7]))
        return new_time

def get_duration(start,finish_hour,finish_minute):
    duration = 0
    finish = []
    finish.append(finish_hour)
    finish.append(finish_minute)
    while start[0] != finish [0]:
        start[0] += 1
        duration += 60
    
    diference = (start[0] - finish [0])
    if diference > 0: 
        (start[0] - finish [0]) * (-1)
    duration += diference
    return duration


#Verifica si la película puede ser agregada
def time_verifier(duration_minutes,movie_schedule,data_movie):
    time_compare = []
    movie_schedule_temp = movie_schedule
    time_compare.append(data_movie[0])
    time_compare.append(data_movie[1])
    date_compare = data_movie[2]
    sala_compare = data_movie[3]
    if len(movie_schedule_temp) != 0:
        while len(movie_schedule_temp) != 0:
            movie_to_check = movie_schedule_temp.pop()
            if sala_compare == movie_to_check[11]:
                if str(date_compare) == str(movie_to_check[4]):
                    time_to_verify = get_time(duration_minutes,movie_to_check)
                    #TIME ENTERED MUST BE HIGHER THAN THE ONE FOUND
                    if time_to_verify[0] < time_compare[0]:
                            pass
                    #TIME ENTERED IS THE SAME, THIS WILL VALIDATE THAT MINUTES ARE NOT CROSSING
                    elif time_to_verify[0] == time_compare[0]:
                        if time_to_verify[1] <= time_compare[1]:
                            pass
                        else:
                            print("Se cruzan las películas, vuelva a intentarlo con otro horario")
                            return False
                    #IF movie is EARLY
                    else:
                        between_movies = get_duration(time_compare,movie_to_check[6],int(movie_to_check[7]))
                        break_minutes = movie_to_check[5]+30 < between_movies
                        if break_minutes:
                            pass
                        else:
                            print("Se cruzan las películas, vuelva a intentarlo con otro horario")
                            return False
                        #check if it can be plaid before start
                        # if time_compare[0] <= movie_to_check[6]:
                        #     print("TIME COMPARE: ",time_compare[0],"TYPE: ",type(time_compare[0]))
                        #     print("MOVIE CHECK: ",movie_to_check[6],"TYPE: ",type(movie_to_check[6]))
                        #     print("STATUS: ",time_compare[0] == movie_to_check[6])
                        #     if time_compare[0] <= movie_to_check[6]:
                        #         if time_compare[0] == movie_to_check[6]:
                        #             if time_compare[1] >= movie_to_check[7]:
                        #                 print("Se cruzan las películas, vuelva a intentarlo con otro horario")
                        #                 return False
                        #             else:
                        #                 pass
                        #         else:
                        #             pass
                        #     else:
                        #         print("Se cruzan las películas, vuelva a intentarlo con otro horario")
                        #         return False                                   
                        # else:
                        #     print("Se cruzan las películas, vuelva a intentarlo con otro horario")
                        #     return False
    else:
        print("Se cruzan las películas, vuelva a intentarlo con otro horario")
        return False
    return True
    
#Converts minutes to time (hours, minutes)
def convert_time(duration_minutes):
    array_duration = []
    hours = 0
    minutes = 0
    if duration_minutes > 59:
        while duration_minutes > 59:
            duration_minutes -= 60
            hours += 1
        minutes = duration_minutes
        array_duration.append(hours)
        array_duration.append(minutes)
        return array_duration
    else:
        array_duration.append(hours)
        minutes = duration_minutes
        array_duration.append(minutes)
        return array_duration

def convert_minus_time(duration_minutes):
    array_duration = []
    hours = 0
    minutes = 0
    if duration_minutes > 59:
        while duration_minutes > 59:
            duration_minutes -= 60
            hours -= 1
        minutes = duration_minutes * -1
        array_duration.append(hours)
        array_duration.append(minutes)
        return array_duration
    else:
        array_duration.append(hours)
        minutes = duration_minutes
        array_duration.append(minutes)
        return array_duration

#Obtiene la ultima hora
def get_new_schedule(duration_time,hour,min):
    new_time = []
    if duration_time[1] + int(min)> 59:
        time_temp = duration_time[1] + int(hour)
        time_temp -= 60
        duration_time[0] += 1
        new_time.append(duration_time[0]+int(hour))
        new_time.append(time_temp)
        return new_time
    else:
        new_time.append(duration_time[0]+int(hour))
        new_time.append(duration_time[1]+int(min))
        return new_time

#Inserta nuevo registro a cartelera
def insert_new_cartelera(new_schedule,movie_selected,id_pelicula,id_municipio):
    query_id_municipio = str("SELECT id_municipios FROM municipios WHERE municipio_nombre='"+str(id_municipio)+"'")
    municipio = Connection.read(conn,query_id_municipio)
    duration_time = convert_time(movie_selected[0][5])
    final_time= get_new_schedule(duration_time,new_schedule[0],new_schedule[1])
    query_insert_cartelera = str("INSERT INTO cartelera VALUES("+ str(id_pelicula) +","+str(municipio[0][0])+",'"+str(new_schedule[2])+"','"+str(new_schedule[0])+"','"+str(new_schedule[1])+"','"+str(final_time[0])+"','"+str(final_time[1])+"',"+str(1)+","+str(new_schedule[3])+")")
    print("QUERY IS: "+query_insert_cartelera)
    #Connection.add(conn,query_insert_cartelera)

#Modifica el registro de alguna pelicula en cartelera
def insert_modify_cartelera(new_schedule,movie_selected,schedule_selected):
    pass

#Revisa si el registro de duracion de peliculas puede ser agregado y modifica los horarios de todas las peliculas
def time_verifier_modify():
    pass

#Esta Función solo agrega las películas pero no a la cartelera
def insert_pelicula(new_pelicula):
    query_agregar_pelicula = str('INSERT INTO peliculas VALUES ('+"'"+new_pelicula[0]+"',"+str(new_pelicula[1])+",'"+new_pelicula[2]+"')")
    Connection.add(conn,query_agregar_pelicula)

def check_modificar_hora():
    pass

def seleccion_menu(tipo_usuario):
    if(tipo_usuario == 1):
        pass
    else:
        pass

def partition(arr, low, high):
    i = (low-1)
    pivot = arr[high]
 
    for j in range(low, high):
        if arr[j] <= pivot:

            i = i+1
            arr[i], arr[j] = arr[j], arr[i]
 
    arr[i+1], arr[high] = arr[high], arr[i+1]
    return (i+1)

def quickSort(arr, low, high):
    if len(arr) == 1:
        return arr
    if low < high:
        pi = partition(arr, low, high)
        quickSort(arr, low, pi-1)
        quickSort(arr, pi+1, high)

def consultarCartelera(data_cartelera):
    if len(data_cartelera)==0:
         print('----------------------------')
    else:
        data_pelicula = data_cartelera.pop()
        print('--------------------------------------')
        if str(data_pelicula[4]) == str('2020-10-10'):
            print('Pelicula: ', data_pelicula[0])
            print('Clasificación:',data_pelicula[1])
            print('Duración: ',data_pelicula[5],'minutos')
            print('Horario: ',int(data_pelicula[6]),':',data_pelicula[7],' - ',int(data_pelicula[8]),':',data_pelicula[9]) 
            consultarCartelera(data_cartelera)

def consultarPelicula(data_cartelera):
    print('----------------------------------------------')
    print('                  PELICULA    ')
    print('Pelicula: ', data_cartelera[0][0])
    print('Clasificación:',data_cartelera[0][1])
    print('Duración: ',data_cartelera[0][5],'minutos')
    for i in range(len(data_cartelera)):
        if data_cartelera[i][10] == 1:
            print('----------------------------------------------')
            print('               OPCION    ',i+1)
            print('Sucursal: ',data_cartelera[i][2])
            print('Día: ',data_cartelera[i][4])
            print('Horario: ',int(data_cartelera[i][6]),':',data_cartelera[i][7],' - ',int(data_cartelera[i][8]),':',data_cartelera[i][9])
            

def menu_administrador(data_admin):
    opcion_menu=1
    print("Bienvenido Admin: ",data_admin[0]," ",data_admin[1])
    print("Sucursal: ", data_admin[5])
    while(opcion_menu!=9):
        try:
            print()
            print('Seleccione alguna de las siguientes Opciones: ')
            print('1.- Alta de Película')
            print('2.- Alta de Horario')
            print('3.- Baja de Película')
            print('4.- Baja de Horario')
            print('5.- Modificar Película')
            print('6.- Consultar Película')
            print('7.- Consultar Cartelera')
            print('8.- Modificar Cartelera')
            print('9.- Cerrar sesión')
            opcion_menu=int(input('Respuesta: '))
            if opcion_menu > 0 and opcion_menu <= 7:
                #Opción 1
                if opcion_menu == 1:
                    try:
                        new_pelicula = []
                        new_pelicula.append(input('Ingrese el nombre de la película: '))
                        new_pelicula.append(int(input('Igrese la duración en minutos de la pelicula: ')))
                        new_pelicula.append(input('Ingrese la clasificación de la película: '))
                        insert_pelicula(new_pelicula)
                    except:
                        print("Uno o mas valores ingresados son erroneos, vuelva a intentarlo")
                        break
                #Opcion 2
                elif opcion_menu == 2:
                    time_compare = []
                    data_temp1=25
                    data_temp2=60
                    municipio_usuario = encontrado[5]
                    n = len(data_peliculas)
                    quickSort(data_peliculas, 0, n-1)
                    opcion_pelicula=1
                    while(opcion_pelicula!=0):
                        try:
                            print('Seleccione la pelicula a agregar: ')
                            for i in range(len(data_peliculas)):
                                print(i+1,'.-',data_peliculas[i][0])
                            print('0.- Salir')
                            opcion_pelicula=int(input('Respuesta: '))
                            if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas):
                                busqueda_pelicula = str("select * from vistaCarteleraActual where peliculas_nombre = '"+str(data_peliculas[opcion_pelicula-1][0])+"'"+" AND cartelera_status = 1 AND municipio_nombre ='" + municipio_usuario+"'")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                if len(data_cartelera_consulta) != 0:
                                    movie_time = data_cartelera_consulta[0][5]    
                                    duration_time = convert_time(movie_time+30)
                                    try:
                                        while(data_temp1 >= 25 or data_temp1<0 or data_temp2 >= 60 or data_temp2 < 0):
                                            data_temp1=int(input("Inserte la hora de la pelicula HH: "))
                                            data_temp2=int(input("Inserte la hora de la pelicula MM: "))
                                            date_compare=str(input("Inserte la fecha de la pelicula YYYY-MM-DD: "))
                                            sala_compare=int(input("Ingrese el numero de sala: "))
                                            if data_temp1 > 25 or data_temp1>0 or data_temp2 < 60 or data_temp2 > 0:
                                                time_compare.append(data_temp1)
                                                time_compare.append(data_temp2)
                                                time_compare.append(date_compare)
                                                time_compare.append(sala_compare)
                                        if data_temp1 > 25 or data_temp1<0 and data_temp2 > 60 or data_temp2 < 0:
                                            print("Los horarios tienen que ser ingresados en un formato de 24 hrs")
                                            print("!!! Vuelva a intentarlo !!!!")
                                    except:
                                        print("Ingrese los datos de forma numerica con el formato especificado")
                                    status=time_verifier(duration_time,data_cartelera_consulta,time_compare)
                                    if status:
                                        pass
                                        # data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                        # insert_new_cartelera(time_compare,data_cartelera_consulta,opcion_pelicula-1,municipio_usuario)
                                    else:
                                        break
                                else:
                                    data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)

                                break
                            elif opcion_pelicula == 0:
                                print()
                                print('--------------------')
                                print('Regresando al menú anterior')
                                print('--------------------')
                                print()
                            else:
                                print()
                                print('------------------------------')
                                print('La opción ingresada no existe')
                                print('------------------------------')
                                print()
                        except ValueError:
                            print()
                            print('*******************************')
                            print('Ingrese una opción numerica')
                            print('*******************************')
                #Opcion 3
                elif opcion_menu == 3:
                    municipio_usuario = encontrado[5]
                    n = len(data_peliculas)
                    quickSort(data_peliculas, 0, n-1)
                    opcion_pelicula=1
                    while(opcion_pelicula!=0):
                        try:
                            print('Seleccione la pelicula a eliminar: ')
                            for i in range(len(data_peliculas)):
                                print(i+1,'.-',data_peliculas[i][0])
                            print('0.- Salir')
                            opcion_pelicula=int(input('Respuesta: '))
                            if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas):
                                query_delete_cartelera = str("DELETE FROM cartelera  WHERE cartelera_pelicula = " + opcion_pelicula -1)
                                query_delete_pelicula = str("DELETE FROM peliculas WHERE id_peliculas = " + opcion_pelicula -1)
                                Connection.delete(conn,query_delete_cartelera)
                                Connection.delete(conn,query_delete_pelicula)
                                print("La pelicula fue eliminada correctamente")                       
                        except:
                            print("Ingrese los datos en el formato requerido")
                            break
                #Opción 4
                elif opcion_menu == 4:
                    opcion_cartelera = 1
                    municipio_usuario = encontrado[5]
                    n = len(data_peliculas)
                    quickSort(data_peliculas, 0, n-1)
                    opcion_pelicula=1
                    while(opcion_pelicula!=0):
                        try:
                            print('Seleccione la pelicula a eliminar: ')
                            for i in range(len(data_peliculas)):
                                print(i+1,'.-',data_peliculas[i][0])
                            print('0.- Salir')
                            opcion_pelicula=int(input('Respuesta: '))
                            if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas):
                                busqueda_pelicula = str("select * from vistaCarteleraActual where peliculas_nombre = '"+str(data_peliculas[opcion_pelicula-1][0])+"'"+" AND cartelera_status = 1")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                try:
                                    if len(data_cartelera_consulta) != 0:
                                        while(opcion_cartelera <= 1 or opcion_cartelera > len(data_cartelera_consulta)+1):
                                            consultarPelicula(data_cartelera_consulta)
                                            print('----------------------------------------------')
                                            opcion_cartelera = int(input("Respuesta: "))
                                    else:
                                        print("La pelicula no se encuentra en la cartelera")
                                        break

                                    pelicula_cartelera = data_cartelera_consulta.pop(opcion_cartelera-1)
                                    print("PELICULA CARTELERA: ",pelicula_cartelera)
                                    print("OPCION CARTELERA: ",opcion_cartelera)
                                    query_delete_cartelera = str("DELETE FROM cartelera  WHERE cartelera_pelicula = " + str(opcion_cartelera -1) + " AND cartelera_dia = '" + str(pelicula_cartelera[4])+"' AND cartelera_inicio = "+str(pelicula_cartelera[6]))
                                    print(query_delete_cartelera)
                                    #Connection.delete(conn,query_delete_cartelera)    
                                    print("La pelicula fue eliminada correctamente")   
                                except:
                                    print("Ingrese los datos en el formato requerido")
                                    break
                            else:
                                print("Escoja una opción válida")
                                print("Intente mas tarde")
                                break             
                        except:
                            print("Ingrese los datos en el formato requerido")
                            break
                #Opción 5
                elif opcion_menu == 5:
                    municipio_usuario = encontrado[5]
                    n = len(data_peliculas)
                    quickSort(data_peliculas, 0, n-1)
                    opcion_pelicula=1
                    while(opcion_pelicula!=0):
                        try:
                            print('Seleccione la pelicula a modificar: ')
                            for i in range(len(data_peliculas)):
                                print(i+1,'.-',data_peliculas[i][0])
                            print('0.- Salir')
                            opcion_pelicula=int(input('Respuesta: '))
                            if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas):
                                busqueda_pelicula = str("select * from vistaCarteleraActual where peliculas_nombre = '"+str(data_peliculas[opcion_pelicula-1][0])+"'"+" AND cartelera_status = 1")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                try:
                                    if len(data_cartelera_consulta) != 0:
                                        sample_info = data_cartelera_consulta.pop()
                                        opcion_modificar = 1
                                        while opcion_modificar != 0:
                                            try:
                                                print("Ingrese valor a modificar")
                                                print("1.- Nombre")
                                                print("2.- Minutos")
                                                print("3.- Clasificación")
                                                print("0.- Salir")
                                                opcion_modificar = int(input("Respuesta: "))
                                                if opcion_modificar <= 3 and opcion_modificar >= 0:
                                                    if opcion_modificar == 1:
                                                        old_name = sample_info[0]
                                                        new_name = input("Ingrese el nuevo nombre: ")
                                                        query_name = "UPDATE peliculas SET peliculas_nombre = '" + str(new_name) + "' WHERE peliculas_nombre = '" + str(old_name) + "'"
                                                        Connection.edit(conn,query_name)
                                                        print("La pelicula fue modificada exitosamente")
                                                        break
                                                    elif opcion_modificar == 2:
                                                        try:
                                                            print("INFO: ", data_cartelera_consulta)
                                                            duration_minutes = int(input("Ingrese la nueva duración de la pelicula: "))
                                                            new_duration = convert_time(duration_minutes)
                                                            data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                                            while len(data_cartelera_consulta) != 0:
                                                                pass
                                                        except:
                                                            print("Ingrese los datos en el formato requerido")
                                                            break 
                                                        break
                                                    elif opcion_modificar == 3: 
                                                        old_name = sample_info[0]
                                                        new_class = input("Ingrese la nueva clasificación: ")
                                                        query_name = "UPDATE peliculas SET peliculas_clasificacion = '" + str(new_class) + "' WHERE peliculas_nombre = '" + str(old_name) + "'"
                                                        Connection.edit(conn,query_name)
                                                        print("La pelicula fue modificada exitosamente")
                                                        break
                                                    else:
                                                        print("Saliendo del menú")
                                                        break
                                                else:
                                                    print("La opción no existe, vuelvalo a intentar")
                                            except:
                                                print("Ingrese los datos en el formato requerido")
                                                break 
                                    else:
                                        print("La pelicula no se encuentra en la cartelera")
                                        break
                                except:
                                    print("Ingrese los datos en el formato requerido")
                                    break               
                            else:
                                print("Escoja una opción válida")
                                print("Intente mas tarde")
                                break 
                        except:
                            print("Ingrese los datos en el formato requerido")
                            break    
                #Opción 6
                elif opcion_menu == 6:
                    n = len(data_peliculas)
                    quickSort(data_peliculas, 0, n-1)
                    opcion_pelicula=1
                    while(opcion_pelicula!=0):
                        try:
                            print('Seleccione la pelicula a buscar: ')
                            for i in range(len(data_peliculas)):
                                print(i+1,'.-',data_peliculas[i][0])
                            print('0.- Salir')
                            opcion_pelicula=int(input('Respuesta: '))
                            if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas): 
                                busqueda_pelicula = str("select * from vistaCarteleraActual where peliculas_nombre = '"+str(data_peliculas[opcion_pelicula-1][0])+"'"+" AND cartelera_status = 1")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                print(busqueda_pelicula)
                                print("DATA:" , data_cartelera_consulta)
                                consultarPelicula(data_cartelera_consulta)
                                break
                            elif opcion_pelicula == 0:
                                print()
                                print('--------------------')
                                print('Regresando al menú anterior')
                                print('--------------------')
                                print()
                            else:
                                print()
                                print('------------------------------')
                                print('La opción ingresada no existe')
                                print('------------------------------')
                                print()
                        except ValueError:
                            print()
                            print('*******************************')
                            print('Ingrese una opción numerica')
                            print('*******************************')
                #Opción 7
                elif opcion_menu == 7:
                    estado_usuario = encontrado[4]
                    data_ciudades = str("select municipio_nombre from vistaMunicipios where estados_nombre ='"+estado_usuario+"'")
                    query_data_ciudades = ''.join(data_ciudades)
                    data_ciudades = Connection.read(conn,query_data_ciudades)
                    n = len(data_ciudades)
                    print("Sorted array is:",data_ciudades)
                    quickSort(data_ciudades, 0, n-1)
                    opcion_ciudad=1
                    while(opcion_ciudad!=0):
                        try:
                            print('Seleccione la ciudad a buscar: ')
                            for i in range(len(data_ciudades)):
                                print(i+1,'.-',data_ciudades[i][0])
                            print('0.- Salir')
                            opcion_ciudad=int(input('Respuesta: '))
                            if opcion_ciudad > 0 and opcion_ciudad <= len(data_ciudades): 
                                busqueda_pelicula = str("select * from vistaCarteleraActual where municipio_nombre = '"+str(data_ciudades[opcion_ciudad-1][0])+"'")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                print('------------------------------------------------')
                                print('Sucursal: ',data_cartelera_consulta[0][2])
                                print('Día: ',d2)
                                consultarCartelera(data_cartelera_consulta)
                                break
                            elif opcion_ciudad == 0:
                                print()
                                print('--------------------')
                                print('Regresando al menú anterior')
                                print('--------------------')
                                print()
                            else:
                                print()
                                print('------------------------------')
                                print('La opción ingresada no existe')
                                print('------------------------------')
                                print()
                        except ValueError:
                            print()
                            print('*******************************')
                            print('Ingrese una opción numerica')
                            print('*******************************')
                else:
                    print()
                    print('------------------------------')
                    print('La opción ingresada no existe')
                    print('------------------------------')
                    print()
            elif opcion_menu == 8:
                temp_option = []
                time_compare = []
                data_temp1=25
                data_temp2=60
                municipio_usuario = encontrado[5]
                n = len(data_peliculas)
                quickSort(data_peliculas, 0, n-1)
                opcion_pelicula=1
                while(opcion_pelicula!=0):
                    try:
                        print('Seleccione la pelicula a modificar: ')
                        for i in range(len(data_peliculas)):
                            print(i+1,'.-',data_peliculas[i][0])
                        print('0.- Salir')
                        opcion_pelicula=int(input('Respuesta: '))
                        if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas):
                            busqueda_pelicula = str("select * from vistaCarteleraActual where peliculas_nombre = '"+str(data_peliculas[opcion_pelicula-1][0])+"'"+" AND cartelera_status = 1 AND municipio_nombre ='" + municipio_usuario+"'")
                            query_busqueda_pelicula = ''.join(busqueda_pelicula)
                            data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)                        
                            if len(data_cartelera_consulta) != 0:
                                seleccion_pelicula = -1
                                i=1
                                #Mostrar Cartelera
                                try:
                                    while seleccion_pelicula < 0 or seleccion_pelicula > len(data_cartelera_consulta)+1:
                                        print("Seleccione la opción de pelicula a modificar: ")
                                        consultarPelicula(data_cartelera_consulta)
                                        print("--------------------------------------------")
                                        print("OPCIÓN 0:  SALIR")
                                        seleccion_pelicula = int(input("Respuesta: "))
                                        if seleccion_pelicula < 0 or seleccion_pelicula > len(data_cartelera_consulta)+1:
                                            print("Ingrese un número entre las opciones mostradas")
                                        else:
                                            temp_option.append(data_cartelera_consulta.pop(seleccion_pelicula-1))
                                            break
                                except ValueError:
                                    print("Ingrese los caracteres en el formato establecido")
                                    print("Intente de nuevo más tarde")
                                    break
                                #data_cartelera_consulta =  
                                movie_time = data_cartelera_consulta[5]    
                                duration_time = convert_time(movie_time+30)
                                try:
                                    while(data_temp1 >= 25 or data_temp1<0 or data_temp2 >= 60 or data_temp2 < 0):
                                        data_temp1=int(input("Inserte la hora de la pelicula HH: "))
                                        data_temp2=int(input("Inserte la hora de la pelicula MM: "))
                                        date_compare=str(input("Inserte la fecha de la pelicula YYYY-MM-DD: "))
                                        sala_compare=int(input("Ingrese el numero de sala: "))
                                        if data_temp1 > 25 or data_temp1>0 or data_temp2 < 60 or data_temp2 > 0:
                                            time_compare.append(data_temp1)
                                            time_compare.append(data_temp2)
                                            time_compare.append(date_compare)
                                            time_compare.append(sala_compare)
                                    if data_temp1 > 25 or data_temp1<0 and data_temp2 > 60 or data_temp2 < 0:
                                        print("Los horarios tienen que ser ingresados en un formato de 24 hrs")
                                        print("!!! Vuelva a intentarlo !!!!")
                                except:
                                    print("Ingrese los datos de forma numerica con el formato especificado")
                                status=time_verifier(duration_time,data_cartelera_consulta,time_compare)
                                if status:
                                    data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                    insert_new_cartelera(time_compare,data_cartelera_consulta,opcion_pelicula-1,municipio_usuario)
                                else:
                                    data_cartelera_consulta.append(temp_option[0])
                                    break
                            else:
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                            break
                        elif opcion_pelicula == 0:
                            print()
                            print('--------------------')
                            print('Regresando al menú anterior')
                            print('--------------------')
                            print()
                        else:
                            print()
                            print('------------------------------')
                            print('La opción ingresada no existe')
                            print('------------------------------')
                            print()
                    except ValueError:
                        print()
                        print('*******************************')
                        print('Ingrese una opción numerica')
                        print('*******************************')
            #Opción 9
            elif opcion_menu == 9:
                print()
                print('--------------------')
                print('Cerró su sesión')
                print('--------------------')
                print()
            else:
                print()
                print('------------------------------')
                print('La opción ingresada no existe')
                print('------------------------------')
                print()
        except ValueError:
            print()
            print('*******************************')
            print('Ingrese una opción numerica')
            print('*******************************')


def menu_cliente(data_customer):
    print("Bienvenido Cliente: ",data_customer[0]," ",data_customer[1])
    print('Sucursal Preferida: ', data_customer[5])
    print('Estado: ',data_customer[4])
    opcion_menu=1
    while(opcion_menu!=7):
        try:
            print()
            print('Seleccione alguna de las siguientes Opciones: ')
            print('1.- Buscar película por nombre')
            print('2.- Buscar película por clasificación')
            print('3.- Buscar película por género')
            print('4.- Ordenar cartelera (A y D)')
            print('5.- Consultar película')
            print('6.- Consultar cartelera')
            print('7.- Salir')
            opcion_menu=int(input('Respuesta: '))
            if opcion_menu > 0 and opcion_menu <= 6:
                if opcion_menu == 1:
                    pass
                elif opcion_menu == 2:
                    pass
                elif opcion_menu == 3:
                    pass
                elif opcion_menu == 4:
                    pass

                #Opción 5
                elif opcion_menu == 5:
                    n = len(data_peliculas)
                    quickSort(data_peliculas, 0, n-1)
                    opcion_pelicula=1
                    while(opcion_pelicula!=0):
                        try:
                            print('Seleccione la pelicula a buscar: ')
                            for i in range(len(data_peliculas)):
                                print(i+1,'.-',data_peliculas[i][0])
                            print('0.- Salir')
                            opcion_pelicula=int(input('Respuesta: '))
                            if opcion_pelicula > 0 and opcion_pelicula <= len(data_peliculas): 
                                busqueda_pelicula = str("select * from vistaCarteleraActual where peliculas_nombre = '"+str(data_peliculas[opcion_pelicula-1][0])+"'"+" AND cartelera_status = 1")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                print(busqueda_pelicula)
                                print("DATA:" , data_cartelera_consulta)
                                consultarPelicula(data_cartelera_consulta)
                                break
                            elif opcion_pelicula == 0:
                                print()
                                print('--------------------')
                                print('Regresando al menú anterior')
                                print('--------------------')
                                print()
                            else:
                                print()
                                print('------------------------------')
                                print('La opción ingresada no existe')
                                print('------------------------------')
                                print()
                        except ValueError:
                            print()
                            print('*******************************')
                            print('Ingrese una opción numerica')
                            print('*******************************')

                #Opción 6
                elif opcion_menu == 6:
                    estado_usuario = encontrado[4]
                    data_ciudades = str("select municipio_nombre from vistaMunicipios where estados_nombre ='"+estado_usuario+"'")
                    query_data_ciudades = ''.join(data_ciudades)
                    data_ciudades = Connection.read(conn,query_data_ciudades)
                    n = len(data_ciudades)
                    print("Sorted array is:",data_ciudades)
                    quickSort(data_ciudades, 0, n-1)
                    opcion_ciudad=1
                    while(opcion_ciudad!=0):
                        try:
                            print('Seleccione la ciudad a buscar: ')
                            for i in range(len(data_ciudades)):
                                print(i+1,'.-',data_ciudades[i][0])
                            print('0.- Salir')
                            opcion_ciudad=int(input('Respuesta: '))
                            if opcion_ciudad > 0 and opcion_ciudad <= len(data_ciudades): 
                                busqueda_pelicula = str("select * from vistaCarteleraActual where municipio_nombre = '"+str(data_ciudades[opcion_ciudad-1][0])+"'")
                                query_busqueda_pelicula = ''.join(busqueda_pelicula)
                                data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                print('------------------------------------------------')
                                print('Sucursal: ',data_cartelera_consulta[0][2])
                                print('Día: ',d2)
                                consultarCartelera(data_cartelera_consulta)
                                break
                            elif opcion_ciudad == 0:
                                print()
                                print('--------------------')
                                print('Regresando al menú anterior')
                                print('--------------------')
                                print()
                            else:
                                print()
                                print('------------------------------')
                                print('La opción ingresada no existe')
                                print('------------------------------')
                                print()
                        except ValueError:
                            print()
                            print('*******************************')
                            print('Ingrese una opción numerica')
                            print('*******************************')
                else:
                    print()
                    print('------------------------------')
                    print('La opción ingresada no existe')
                    print('------------------------------')
                    print()
            elif opcion_menu == 7:
                print()
                print('--------------------')
                print('Cerró su sesión')
                print('--------------------')
                print()
            else:
                print()
                print('------------------------------')
                print('La opción ingresada no existe')
                print('------------------------------')
                print()
        except ValueError:
            print()
            print('*******************************')
            print('Ingrese una opción numerica')
            print('*******************************')

encontrado = 1
today = date.today()
d1 = today.strftime("%Y-%m-%d")
d2 = today.strftime("%d-%m-%Y")
print(d1)
while (encontrado != 0):
    try:
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
                print('Intente de nuevo o ingrese "0" para salir del programa')
    except ValueError:
        print()
        print('************************************************')
        print('Recuerde que tiene que ser un valor numerico')
        print('Si no cuenta con el contacte al administrador')
        print('************************************************')
        print()