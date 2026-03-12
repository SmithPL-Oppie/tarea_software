import json
import os
from datetime import datetime #Extraemos el libro datetime de su libreria
 
ARCHIVO = "tareas_administrativas.json"
 
"""
Funcionalidades del sistema:
-Agregar, leer, actualizar y borrar tareas.
-Las tareas van a cortar con un id.
-Validación de fechas con la libreria datetime.
-Manejo de errores (try except).
-Menú.
-Arranque automatizado segun el archivo.
-Prioridades en las tareas.
"""
 
#Función para cargar tareas
def cargar_tareas():
    if os.path.exists(ARCHIVO):
        with open(ARCHIVO,"r") as archivo:
            return json.load(archivo)
    return []

#Función para guardar tareas
def guardar_tarea(tareas):
    with open(ARCHIVO, "w") as archivo:
        json.dump(tareas, archivo, indent=4)#Indent te ayuda a corregir la identacion de tu json
 
#Función para validar prioridad
def validar_prioridad(prioridad):
    prioridades_validas = ["Alta","Media","Baja"]
    if prioridad.capitalize() in prioridades_validas:
        return prioridad.capitalize()
    else:
        print("Prioridad invalida. Use Alta, Media o Baja")
        return None
 
#Función para crear ID
def generar_id(tareas):
    if not tareas:
        return 1
    return max(t["id"] for t in tareas) + 1 #Busca el id mayor existente y luego crea uno nuevo sumandole 1
 
#Función para validar fecha
def validar_fecha(fecha):
    #Usamos manejo de errores para no detener el programa(try-except)
    try: #Ejecuta el codigo, realiza el intento (try)
        fecha_agregada = datetime.strptime(fecha, "%Y-%m-%d").date()#Cambiar el formato string a date
        #Evaluamos si el usuario ingresa una fecha pasada
        if fecha_agregada < datetime.now().date(): #datetime.now().date() es un metodo para obtener la fecha actual
            print("Solo se permite fecha(s) actual o posteriores")
            return None
        return fecha_agregada.strftime("%Y-%m-%d")#Convierte el dato date a string
    except ValueError: #Si ocurre un error, ejecuta esto
        print("Formato inválido. Ingrese YYYY-MM-DD")
        return None
 
#Función de crear tarea
def crear_tarea(tareas):
    descripcion = input("Descripción: ")
    responsable = input("Responsable: ")
    while True:
        fecha = input("Fecha limite(YYYY-MM-DD): ")
        fecha_validada = validar_fecha(fecha)
        if fecha_validada:
            break
    while True:
        prioridad = input("Prioridad(Alta/Media/Baja): ")
        prioridad_validada = validar_prioridad(prioridad)
        if prioridad_validada:
            break
    tarea = {
        "id":generar_id(tareas),
        "descripcion": descripcion,
        "fecha_limite":fecha_validada,
        "responsable": responsable,
        "prioridad": prioridad_validada,
        "estado":"Pendiente"
        }
    tareas.append(tarea)
    guardar_tarea(tareas)
    print("Tarea generada exitosamente")
 
#Función visualizar tareas
def visualizar_tareas(tareas):
    #Evaluamos si no hay tareas
    if not tareas:
        print("No hay tareas registradas")
        return
    #Almacenamos la fecha actual
    fecha_actual = datetime.now().date()
    #Recorremos nuestro json y convertimos nuestro key fecha limite a date
    for tarea in tareas:
        fecha_tarea = datetime.strptime(tarea["fecha_limite"], "%Y-%m-%d").date() #Nuevamente transformamos nuestro dato fecha string a date
        #Calculamos cuantos dias restan para la tarea
        dias_restantes = (fecha_tarea - fecha_actual).days
        #Creamos una variable vacia para almacenar un estado extra
        estado_auto = ""
        #Evaluamos los dias restantes y de acuerdo a su condición, un estado extra
        if dias_restantes < 0:
            estado_auto = "Tarea vencida."
        elif dias_restantes <= 3:
            estado_auto = "Proximo a vencer."
        #Mostramos nuestros datos dentro del archivo json
        print("-------------------------------")
        print(f"ID: {tarea['id']}")
        print(f"Descripción: {tarea['descripcion']}")
        print(f"Fecha Limite: {tarea['fecha_limite']}({dias_restantes} dias){estado_auto}")
        print(f"Responsable: {tarea['responsable']}")
        print(f"Prioridad: {tarea['prioridad']}")
        print(f"Estado: {tarea['estado']}")
        print("-------------------------------")
        
#Actualizar tarea
def actualizar_tarea(tareas):
    #Evaluamos si el usuario agrega correctamente el ID
    try:
        id_tarea = int(input("Ingresa el ID de la tarea: "))
    except ValueError:
        print("ID inválido")
        return
    #Buscamos las tareas
    for tarea in tareas:
        #Validamos si el id de la tarea existe
        if tarea["id"] == id_tarea:
            tarea["descripcion"] = input("Nueva descripción: ")
            tarea["responsable"] = input("Nuevo Responsable: ")
            #agregamos cambios a nuestros validadores (fecha - prioridad)
            while True:
                nueva_fecha = input("Nueva fecha limite(YYYY-MM-DD): ")
                fecha_validada = validar_fecha(nueva_fecha)
                if fecha_validada: #Si es correcto, se almacena la vecha fecha validada
                    tarea["fecha_limite"] = fecha_validada
                    break
            while True:
                nueva_prioridad = input("Nueva prioridad(Alta/Media/Baja): ")
                prioridad_validada = validar_prioridad(nueva_prioridad)
                if prioridad_validada:#Si es correcto, se almacena la nueva prioridad validada
                    tarea["prioridad"] = prioridad_validada
                    break
            tarea["estado"] = input("Estado (Pendiente/Completo): ")
            guardar_tareas(tareas)
            print("Tarea actualizada.")
            return
    print("Tarea no encontrada.")

#Menú
def menu():
    tareas = cargar_tareas()
    while True:
        print("----- Gestor de tareas -----")
        print("1. Crear tarea")
        print("2. Mostrar tarea")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Salir")
        opcion = input("Selecciona una opción: ")
        if opcion == "1":
            crear_tarea(tareas)
        elif opcion == "2":
            visualizar_tareas(tareas)
        elif opcion == "5":
            break
        else:
            print("Opción invalida.")
 
if __name__ == "__main__": #El código solo se ejecuta si el archivo está en uso
    menu()
 
 
    

 
