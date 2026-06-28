#aquí importaremos las imágenes
#importamos librerías
import os    #para trabjar con la capreta de imágenes
from PIL import Image    #para abrir y manipular imágenes
import numpy as np    #importamos numpy agregando alias 

#constantes
CARPETA_IMAGENES = "Imágenes"
CARPETA_FONDOS = "Fondos"
FORMATOS_VALIDOS = (".png",".jpg", ".jpeg")


def lista_imagenes(carpeta):
     #manejo de error por si la carpeta no existe
    if not os.path.isdir(carpeta): 
        print(f"Error: La carpeta '{carpeta}' no existe.")
        return[]
    
    #guardamos una lista con todos los archivos dentro de carpeta
    archivos = os.listdir(carpeta) 
    
    imagenes = [a for a in archivos if a.lower().endswith(FORMATOS_VALIDOS)]
    return sorted(imagenes)

def cargar_imagen(ruta):
    try:
        if not os.path.isfile(ruta):
            print(f"Error: El archivo '{ruta}' no existe.")
            return None
        
        if not ruta.lower().endswith(FORMATOS_VALIDOS):
            print(f"Error: Formato inválido para '{ruta}', Use PNG o JPG")
            return None
        
        imagen = Image.open(ruta)
        imagen = imagen.convert("RGB") #para asegurar solo 3 canales
        return np.array(imagen)
    
    except Exception as error:
        print(f"Error: No se pudo cargar la imagen '{ruta}'")
        return None
    
def selecion_imagen_principal():
    imagenes_disponibles = lista_imagenes(CARPETA_IMAGENES)
    
    if not imagenes_disponibles:
        print(f"Error: No hay imágenes disponibles en '{CARPETA_IMAGENES}'.")
        return None, None
    print("\nSeleccione una de las siguientes imágenes:")
    i = 1
    for nombre in imagenes_disponibles:
        print(f"  {i}. {nombre}")
        i += 1
        
    while True:
        entrada = input("\nIngrese el número de la imagen que desea procesar").strip()
        
        if not entrada.isdigit():
            print("Error: Debe ingresar un número entero. Intente de nuevo.")
            continue
        
        opcion = int(entrada)
        if opcion < 1 or opcion > len(imagenes_disponibles):
            print(f"Error: Ingrese un número entre 1 y {len(imagenes_disponibles)}")
            continue
        
        nombre_elegido = imagenes_disponibles[opcion - 1]
        ruta_completa = os.path.join(CARPETA_IMAGENES, nombre_elegido)
        matriz = cargar_imagen(ruta_completa)
        
        if matriz is None:
            print("No se pudo cargar la imagen seleccionada :(. Intente con otra.")
            continue
        return nombre_elegido, matriz
    
def fondos_alternativos():
    fondos_disponibles = lista_imagenes(CARPETA_FONDOS)
    
    if len(fondos_disponibles) < 2:
        print(f"Error: Se necesitan al menos 2 imágenes en {CARPETA_FONDOS}.")
        return[]
    
    felegido = fondos_disponibles[:2] #los 2 primeros en orden alfabetico
    resultado = []
    
    for nombre in felegido:
        ruta = os.path.join(CARPETA_FONDOS, nombre)
        matriz = cargar_imagen(ruta)
        
        if matriz is None:
            print(f"Error: No se pudo cargar el fondo '{nombre}'.")
            return[]
        resultado.append((nombre, matriz))
    return resultado
