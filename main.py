#Author: Emanuel Camarena
#Slack: emanuelc.dev

import pyodbc 
from connection import *
from datetime import date, datetime

class Cola:
    def __init__(self):
        self.items = []

    def estaVacia(self):
        return self.items == []

    def agregar(self, item):
        self.items.insert(0,item)

    def avanzar(self):
        return self.items.pop()

    def tamano(self):
        return len(self.items)

    def vacio(self):
        while len(self.items) != 0:
            self.items.pop()
        return len(self.items) == 0



class Pila:
     def __init__(self):
         self.items = []

     def estaVacia(self):
         return self.items == []

     def incluir(self, item):
         self.items.append(item)

     def extraer(self):
         return self.items.pop()

     def inspeccionar(self):
         return self.items[len(self.items)-1]

     def tamano(self):
         return len(self.items)

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
    print("Estás conectado correctamente a la BD")
    data_cartelera_disponible=Connection.read(conn,query_vista_cartelera_actual)
    data_usuarios_disponible=Connection.read(conn,query_vista_usuarios)
    data_peliculas=Connection.read(conn,'select peliculas_nombre from peliculas')

else: 
    print("NO estás conectado correctamente a la BD")

def binarySearch(arr, x): 
    l = 0
    r = len(arr) 
    while (l <= r): 
        m = l + ((r - l) // 2) 
  
        res = (x == arr[m]) 
  
        # Revisa si X está presente a la mitad 
        if (res == 0): 
            return m - 1
  
        #Si X es mas grande, ignora la mitad izquierda 
        if (res > 0): 
            l = m + 1
  
        # Si X es mas pequeño, ignora la mitad derecha 
        else: 
            r = m - 1
  
    return -1

def log_in(entrada_usuario,entrada_password,data_usuarios_disponible):
    usuario_encontrado=''
    for i in range(len(data_usuarios_disponible)):
        if data_usuarios_disponible[i][2]==entrada_usuario:
            usuario_encontrado=data_usuarios_disponible[i]
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
        return list(new_time)
    else:
        new_time.append(duration_time[0]+int(hour))
        new_time.append(duration_time[1]+int(min))
        return list(new_time)

#Inserta nuevo registro a cartelera
def insert_new_cartelera(new_schedule,movie_selected,id_pelicula,id_municipio):
    query_id_municipio = str("SELECT id_municipios FROM municipios WHERE municipio_nombre='"+str(id_municipio)+"'")
    municipio = Connection.read(conn,query_id_municipio)
    duration_time = convert_time(movie_selected[0][5])
    final_time= get_new_schedule(duration_time,new_schedule[0],new_schedule[1])
    query_insert_cartelera = "INSERT INTO cartelera VALUES("+ str(id_pelicula+1) +","+str(municipio[0][0])+",'"+str(new_schedule[2])+"','"+str(new_schedule[0])+"','"+str(new_schedule[1])+"','"+str(final_time[0])+"','"+str(final_time[1])+"',"+str(1)+","+str(new_schedule[3])+")"
    Connection.add(conn,query_insert_cartelera)
    print("La pelicula fue agregada a cartelera exitosamente")

def insert_one_cartelera(new_schedule,movie_selected,id_pelicula,id_municipio):
    query_id_municipio = str("SELECT id_municipios FROM municipios WHERE municipio_nombre='"+str(id_municipio)+"'")
    municipio = Connection.read(conn,query_id_municipio)
    duration_time = convert_time(movie_selected)
    final_time= get_new_schedule(duration_time,new_schedule[0],new_schedule[1])
    query_insert_cartelera = str("INSERT INTO cartelera VALUES("+ str(id_pelicula) +","+str(municipio[0][0])+",'"+str(new_schedule[2])+"','"+str(new_schedule[0])+"','"+str(new_schedule[1])+"','"+str(final_time[0])+"','"+str(final_time[1])+"',"+str(1)+","+str(new_schedule[3])+")")
    Connection.add(conn,query_insert_cartelera)
    print("La pelicula fue agregada a cartelera exitosamente")

#Modifica el registro de alguna pelicula en cartelera
def insert_modify_cartelera(new_schedule,movie_selected,schedule_selected):
    pass

#Revisa si el registro de duracion de peliculas puede ser agregado y modifica los horarios de todas las peliculas
def time_verifier_modify():
    pass

#Esta Función solo agrega las películas pero no a la cartelera
def insert_pelicula(new_pelicula):
    query_agregar_pelicula = str('INSERT INTO peliculas VALUES ('+"'"+new_pelicula[0]+"',"+str(new_pelicula[1])+",'"+new_pelicula[2]+"','"+new_pelicula[3])+"')"
    Connection.add(conn,query_agregar_pelicula)
    print("La pelicula fue agregada a cartelera exitosamente")
    print("La pelicula será reflejada al siguiente inicio")

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
                        new_pelicula.append(input('Ingrese el tipo de la película: '))
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
                                        data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                        insert_new_cartelera(time_compare,data_cartelera_consulta,opcion_pelicula-1,municipio_usuario)
                                    else:
                                        break
                                else:
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
                                    query_time = "SELECT peliculas_minutos from peliculas WHERE id_peliculas = " + str(opcion_pelicula-1)
                                    time_consult = Connection.read(conn,query_time)
                                    time = time_consult[0][0]
                                    insert_one_cartelera(time_compare,time,opcion_pelicula-1,municipio_usuario)
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
                                query_delete_cartelera = "DELETE FROM cartelera  WHERE cartelera_pelicula = " + str(opcion_pelicula -1)
                                query_delete_pelicula = "DELETE FROM peliculas WHERE id_peliculas = " + str(opcion_pelicula -1)
                                Connection.delete(conn,query_delete_cartelera)
                                Connection.delete(conn,query_delete_pelicula)
                                print("La pelicula fue eliminada correctamente")
                                print("Los cambios se reflejarán al siguiente log-in")
                                break                     
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
                                        while(opcion_cartelera < 1 or opcion_cartelera > len(data_cartelera_consulta)):
                                            consultarPelicula(data_cartelera_consulta)
                                            print('----------------------------------------------')
                                            opcion_cartelera = int(input("Respuesta: "))
                                    else:
                                        print("La pelicula no se encuentra en la cartelera")
                                        break

                                    pelicula_cartelera = data_cartelera_consulta.pop(opcion_cartelera-1)
                                    query_delete_cartelera = "DELETE FROM cartelera  WHERE cartelera_pelicula = " + str(opcion_cartelera -1) + " AND cartelera_dia = '" + str(pelicula_cartelera[4])+"' AND cartelera_inicio = "+str(pelicula_cartelera[6])
                                    Connection.delete(conn,query_delete_cartelera)    
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
                                pelicula = data_cartelera_consulta[0][0]
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
                                                        status = True
                                                        new_schedule = []
                                                        new_cartelera = []
                                                        try:
                                                            i=0
                                                            data_cartelera_consulta=Connection.read(conn,query_busqueda_pelicula)
                                                            data_cartelera_temp = data_cartelera_consulta
                                                            duration_minutes = int(input("Ingrese la nueva duración de la pelicula: "))
                                                            new_duration = convert_time(duration_minutes)
                                                            while len(data_cartelera_temp) != 0:
                                                                data_to_send = data_cartelera_temp.pop()
                                                                new_schedule.append(get_new_schedule(new_duration,data_to_send[6],int(data_to_send[7])))
                                                                list(new_schedule)
                                                                data_to_send[9]=str(new_schedule[i][1])
                                                                data_to_send[8]=new_schedule[i][0]
                                                                new_cartelera.append(data_to_send)
                                                                data_to_send = []
                                                                i+=1
                                                            cola = Cola()
                                                            item = Cola()
                                                            while len(new_cartelera) != 0:
                                                                cartelera_temp = new_cartelera.pop()
                                                                cola.agregar(cartelera_temp)
                                                                item.agregar(cartelera_temp)
                                                            tamano = cola.tamano()
                                                            if tamano >= 2:                                                                
                                                                while tamano >= 2:
                                                                    item_temp = item.avanzar()
                                                                    temp_time1=item_temp[8]
                                                                    temp_time2=int(item_temp[9])
                                                                    new_time_compare = []
                                                                    new_time_compare.append(temp_time1)
                                                                    new_time_compare.append(temp_time2)
                                                                    item_temp = item.avanzar()
                                                                    temp_time1=item_temp[6]
                                                                    temp_time2=int(item_temp[7])
                                                                    new_duration_time = get_duration(new_time_compare,temp_time1,temp_time2)
                                                                    tamano = item.tamano()
                                                                    if new_duration_time >= 30:
                                                                        pass
                                                                    else:
                                                                        status = False
                                                                        break
                                                                if status == True:
                                                                    j = 0
                                                                    query_time = "UPDATE peliculas SET peliculas_minutos = " + str(duration_minutes) + " WHERE peliculas_nombre = '" + str(pelicula) + "'"
                                                                    Connection.edit(conn,query_time)
                                                                    municipio_query = "select id_municipios from municipios WHERE municipio_nombre = '" + str(encontrado[5]) + "'"
                                                                    municipio_select = Connection.read(conn,municipio_query)
                                                                    municipio = municipio_select[0][0]
                                                                    while len(new_schedule) != 0:
                                                                        temp_new_schedule = new_schedule.pop()
                                                                        query_time = "UPDATE cartelera SET cartelera_minutos_final = " + str(temp_new_schedule[1]) + " WHERE cartelera_pelicula = " + str(opcion_modificar-1) + "" + " AND cartelera_municipio = " + str(municipio) + " AND cartelera_final = " + str(temp_new_schedule[0])
                                                                        Connection.edit(conn,query_time)
                                                                        j += 1
                                                                    print("La pelicula fue modificada exitosamente")
                                                                    break                                                                
                                                                else:
                                                                    print("La nueva duración hace que los horarios se cruzen")
                                                                    print("Intente de nuevo con una duración menor")
                                                                    break
                                                            else:
                                                                query_time = "UPDATE peliculas SET peliculas_minutos = " + str(duration_minutes) + " WHERE peliculas_nombre = '" + str(pelicula) + "'"
                                                                Connection.edit(conn,query_time)
                                                                break
                                                        except ValueError:
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
                                            except ValueError:
                                                print("Ingrese los datos en el formato requerido")
                                                break 
                                    else:
                                        print("La pelicula no se encuentra en la cartelera")
                                        break
                                except ValueError:
                                    print("Ingrese los datos en el formato requerido")
                                    break               
                            else:
                                print("Escoja una opción válida")
                                print("Intente mas tarde")
                                break 
                        except ValueError:
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
                                if len(data_cartelera_consulta) != 0:
                                    consultarPelicula(data_cartelera_consulta)
                                    break
                                else:
                                    print("La pelicula no cuenta con ningún horario")
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
                                get_movie_time = data_cartelera_consulta[0][5]
                                movie_time = get_movie_time    
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

#Recursividad
def array_tipo_pelicula(array_peliculas,tipo_pelicula):
    tipo =  tipo_pelicula
    array = array_peliculas
    if len(array) != 0:
        pelicula = array.pop()
        if tipo == pelicula[4]:
            query_pelicula = "SELECT * FROM  vistaCarteleraActual WHERE peliculas_type = '" + str(tipo) + "' AND municipio_nombre = '" + str(encontrado[5]) + "'"
            pelicula_found = Connection.read(conn,query_pelicula)
            if len(pelicula_found) != 0:
                data_temp = pelicula_found.pop()
                print("")
                print("-------------------------------------------------------------")
                print("Pelicula: ", data_temp[0])
                print("Estado:   ", data_temp[3])
                print("Municipio: ", data_temp[2])
                print("Horario: ", str(data_temp[6])+":"+str(data_temp[7]) + " - " + str(data_temp[8])+":"+str(data_temp[9]))
                print("Sala: ", str(data_temp[11]))
                print("-------------------------------------------------------------")
                print("")
            else:
                pass
            return array_tipo_pelicula(array,tipo)
        else:
            return array_tipo_pelicula(array,tipo)
    else:
        pass

def menu_cliente(data_customer):
    print("-------------------------------------------------------------------")
    print("Bienvenido Cliente: ",data_customer[0]," ",data_customer[1])
    print('Sucursal Preferida: ', data_customer[5])
    print('Estado: ',data_customer[4])
    print(" ")
    opcion_menu=1
    id_municipio = data_customer[4]
    #query_id_municipio = str("SELECT id_estados FROM estados WHERE estados_nombre = '"+str(id_municipio)+"'")
    #estado_id_temp = Connection.read(conn,query_id_municipio)
    #estado_id = estado_id_temp[0][0]
    query_info_peliculas = "SELECT * FROM vistaCarteleraActual WHERE estados_nombre = '" + str(id_municipio) + "' AND cartelera_status = 1"
    data_cartelera_disponible = Connection.read(conn,query_info_peliculas)
    while(opcion_menu!=7):
        try:
            print()
            print('Seleccione alguna de las siguientes Opciones: ')
            print('1.- Buscar película por nombre')  #DONE
            print('2.- Buscar película por clasificación') #DONE
            print('3.- Buscar película por género') #Working
            print('4.- Ordenar cartelera (A y D)') #Done
            print('5.- Consultar película')   #DONE
            print('6.- Consultar cartelera')  #DONE
            print('7.- Salir')
            opcion_menu=int(input('Respuesta: '))
            if opcion_menu > 0 and opcion_menu <= 6:
                #Binary Search
                if opcion_menu == 1:
                    binary = 0
                    data_to_verify = []
                    data_cartelera = []
                    clasificacion_answer=input("Ingrese la pelicula a buscar: ")
                    if len(data_cartelera_disponible) > 0:
                        while len(data_cartelera_disponible) != 0:
                            data = data_cartelera_disponible.pop()
                            for i in range(10):
                                data_to_verify.append(data[i])
                                if i == 9:
                                    count_found = data_to_verify.count(clasificacion_answer)
                                    if count_found != 0:
                                        data_cartelera.append(data_to_verify)
                            binary = binarySearch(data_to_verify,clasificacion_answer)
                            if binary == 4:
                                while len(data_cartelera) != 0:
                                    data_temp = data_cartelera.pop()
                                    print("")
                                    print("-------------------------------------------------------------")
                                    print("Pelicula: ", data_temp[0])
                                    print("Estado:   ", data_temp[3])
                                    print("Municipio: ", data_temp[2])
                                    print("Horario: ", str(data_temp[6])+":"+str(data_temp[7]) + " - " + str(data_temp[8])+":"+str(data_temp[9]))
                                    print("Sala: ", str(data_temp[11]))
                                    print("-------------------------------------------------------------")
                                    print("")
                            data_to_verify = []
                elif opcion_menu == 2:
                    data_to_verify = []
                    data_cartelera = []
                    #Listas - Count
                    clasificacion_answer=input("Ingrese la clasificación de la pelicula a buscar: ")
                    if len(data_cartelera_disponible) > 0:
                        while len(data_cartelera_disponible) != 0:
                            data = data_cartelera_disponible.pop()
                            for i in range(11):
                                data_to_verify.append(data[i])
                                if i == 10:
                                    count_found = data_to_verify.count(clasificacion_answer)
                                    if count_found != 0:
                                        data_cartelera.append(data_to_verify)
                            data_to_verify = []
                        while len(data_cartelera) != 0:
                            data_temp = data_cartelera.pop()
                            print("")
                            print("-------------------------------------------------------------")
                            print("Pelicula: ", data_temp[0])
                            print("Estado:   ", data_temp[3])
                            print("Municipio: ", data_temp[2])
                            print("Horario: ", str(data_temp[6])+":"+str(data_temp[7]) + " - " + str(data_temp[8])+":"+str(data_temp[9]))
                            print("Sala: ", str(data_temp[11]))
                            print("")
                    else:
                        print("No existe ninguna pelicula con esa clasificación")
                        print("")
                        
                elif opcion_menu == 3:
                    tipo_pelicula = input("Ingrese el tipo de peliculas a buscar: ")
                    query_peliculas = "SELECT * FROM peliculas"
                    array_peliculas = Connection.read(conn,query_peliculas)
                    array_tipo_pelicula(array_peliculas,tipo_pelicula)    
                elif opcion_menu == 4:
                    new_data = []
                    while len(data_peliculas) != 0:
                        data_temp = data_peliculas.pop()
                        data_insert = data_temp[0]
                        new_data.append(data_insert)
                    n = len(new_data)
                    quickSort(new_data,1,n-1)
                    search = Pila()
                    while len(new_data) != 0:
                        movie_search = new_data.pop(0)
                        query_info_peliculas = "SELECT * FROM vistaCarteleraActual WHERE estados_nombre = '" + str(id_municipio) + "' AND cartelera_status = 1 AND peliculas_nombre = '" + str(movie_search) + "'"
                        result_found = Connection.read(conn,query_info_peliculas)
                        if len(result_found) != 0:
                            while len(result_found) != 0:
                                temp_result = result_found.pop(0)
                                for i in range(12):
                                    search.incluir(temp_result[i])
                                vacio = search.estaVacia()
                                if vacio == False:
                                    search.extraer()
                                    print("")
                                    print("-------------------------------------------------------------")
                                    print("Pelicula: ", temp_result[0])
                                    print("Estado:   ", temp_result[3])
                                    print("Municipio: ", temp_result[2])
                                    print("Horario: ", str(temp_result[6])+":"+str(temp_result[7]) + " - " + str(temp_result[8])+":"+str(temp_result[9]))
                                    print("Sala: ", str(temp_result[11]))
                                    print("-------------------------------------------------------------")
                                    print("")
                        else:
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
                                if len(data_cartelera_consulta) != 0:
                                    consultarPelicula(data_cartelera_consulta)
                                    break
                                else:
                                    print("La pelicula no cuenta con ningún horario")
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
print("Día de hoy es: ",d1)
while (encontrado != 0):
    try:
        entrada_usuario=int(input('Ingrese su usuario o "0" para salir: '))
        if entrada_usuario == 0:
            print('Gracias por utilizar nuestro servicio, vuelva pronto')
            break
        else:
            entrada_password=input('Ingrese su contraseña: ')
            encontrado=log_in(entrada_usuario,entrada_password,data_usuarios_disponible)
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