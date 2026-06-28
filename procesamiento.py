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
    
    #me voy a dormir papus, chatisimo