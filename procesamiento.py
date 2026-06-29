import numpy as np
import datetime as dt

def recibir_imagen(matriz_img, tope=60, esquina=20):
    alto = matriz_img.shape[0]
    ancho = matriz_img.shape[1]

    # ESQUINAS
    sup_izq = matriz_img[0:esquina, 0:esquina]
    sup_der = matriz_img[0:esquina, ancho-esquina:ancho]
    inf_izq = matriz_img[alto-esquina:alto, 0:esquina]
    inf_der = matriz_img[alto-esquina:alto, ancho-esquina:ancho]

    #todas las esquinas en una sola matriz
    fondo = np.concatenate([
        sup_izq.reshape(-1, 3),
        sup_der.reshape(-1, 3),
        inf_izq.reshape(-1, 3),
        inf_der.reshape(-1, 3)
    ])

    #promedio de color de las esquinas (fondo) R, G, B
    promedio = np.mean(fondo, axis=0)

    #verificar el fondo de la imagen
    diferencia = matriz_img.astype(np.int32) - promedio
    distancia = np.sqrt(np.sum(diferencia ** 2, axis=2))

    #clasificar los pixeles como fondo o no fondo
    mascara = distancia > tope
    #True = objeto, False = fondo

    return mascara

def reemplazar_fondo(matriz_img, mascara, matriz_fondo):
    if matriz_img.shape != matriz_fondo.shape:
        chato = "Error: Las imagenes no tienen las mismas dimensiones."
        print(chato)
        return 
    

    resultado = matriz_fondo.copy()
    resultado[mascara] = matriz_img[mascara] #escribe sobre los pixeles del objeto
    
    return resultado

def coordenadas_objeto(mascara):
    suma = int(mascara.sum())
    
    #ubicacion del objeto mediante filas y columnas
    filas, columnas = np.where(mascara)
    cordenadas = []
    for i in range(len(filas)):
        cordenadas.append((filas[i], columnas[i]))

    return cordenadas, suma

def reporte(mascara, nombre_archivo):
  
    try:
        cordenadas, suma = coordenadas_objeto(mascara)
        ahora = dt.datetime.now()
        reporte_n = f"reporte_{ahora.strftime('%d%m%Y_%H%M%S')}.txt"

        with open(reporte_n, 'w') as arch: #abrimos y creamos
          arch.write(f"Nombre del archivo: {nombre_archivo}\n")
          arch.write(f"Cantidad de pixeles del objeto: {suma}\n")
          arch.write("Coordenadas de los pixeles del objeto:\n")
          #salto para poner coordenadas despues
          for fila, columna in cordenadas:
              arch.write(f"({fila}, {columna})\n")
            
        
        print(f"Reporte generado: {reporte_n}")
        return reporte_n
    
    except Exception as e:
        print(f"Error al generar el reporte: {e}")
        return
