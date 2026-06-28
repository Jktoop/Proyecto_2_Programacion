import numpy as np #redimensionar imagen
import matplotlib.pyplot as plt #ventana grafica
from matplotlib.widgets import Button #botones de la ventana grafica
import datetime as dt #para el archivo de reporte
from PIL import Image #resize y guardar imagen

from imagenes import selecion_imagen_principal, fondos_alternativos, cargar_imagen
from procesamiento import recibir_imagen, reemplazar_fondo, coordenadas_objeto, reporte

#crear los botones y ventana
# a comer

def inicio():
    print("Iniciando el super editor de fondos")
    nombre_img, img_original = selecion_imagen_principal()  # pide a usuario la imagen con la funcion de imagenes.py
    
    if img_original is None:
        print("Error: No se pudo cargar la imágen principal. cerrando programa, bye")
        return
    
    alto = img_original.shape[0]
    ancho = img_original.shape[1]
    
    lista_fondos = fondos_alternativos()
    if len(lista_fondos) < 2:
        print("Error: Fondos insuficientes en la carpeta, no se puede continuar.")
        return
    
    nombre_f1, matrizf1 = lista_fondos[0]
    nombre_f2, matrizf2 = lista_fondos[1]
    
    mascara = recibir_imagen(img_original)
    
    pil_f1 = Image.fromarray(matrizf1).resize((ancho,alto))
    f1_listo = np.array(pil_f1)
    
    pil_f2 = Image.fromarray(matrizf2).resize((ancho,alto))
    f2_listo = np.array(pil_f2)
    
    img_con_f1 = reemplazar_fondo(img_original, mascara, f1_listo)
    img_con_f2 = reemplazar_fondo(img_original, mascara, f2_listo)
    
    imagenes_app = {"Original": img_original, "Fondo 1": img_con_f1, "Fondo 2": img_con_f2}
    
    opcion_actual = {"ver": "original"}  # diccionario pa saber que img está mirando el user en pantalla
    
    # config de ventana grafica
    fig, eje_graf = plt.subplots(figsize=(8,6))
    plt.subplots_adjust(bottom=0.25)  # asignamos margen pa los botones
    
    pantalla = eje_graf.imshow(imagenes_app["Original"])
    eje_graf.set_title("Mostrando imagen original")
    eje_graf.axis("off")
    
    def cambiar_imagen(nombre):
        opcion_actual["ver"] = nombre
        pantalla.set_data(imagenes_app[nombre]) 
        eje_graf.set_title(f"Mostrando {nombre}")
        fig.canvas.draw_idle() # refresca la ventana grafica
        
    def click_original(event):
        cambiar_imagen("Original")
    
    def click_fondo1(event):
        cambiar_imagen("Fondo 1")
    
    def click_fondo2(event):
        cambiar_imagen("Fondo 2")
        
    def click_guardar(event):
        # marca de tiempo con fecha y hora exacta
        fecha_hora = dt.datetime.now().strftime("%d%m%Y_%H%M%S")
        nombre_final = f"resultado_{opcion_actual['ver']}_{fecha_hora}.png" 
        
        # sacamos la matriz que se está viendo y la guardamos como PNG
        matriz_actual = imagenes_app[opcion_actual["ver"]]
        Image.fromarray(matriz_actual).save(nombre_final)
        
        eje_graf.set_title(f"Guardado como: {nombre_final}")
        fig.canvas.draw_idle()
        
    def click_reporte(event):
        nombre_txt = reporte(mascara, nombre_img)
        eje_graf.set_title(f"Reporte creado: {nombre_txt}")
        fig.canvas.draw_idle()
        
    
    eje_boton1 = plt.axes([0.05, 0.05, 0.15, 0.08])
    eje_boton2 = plt.axes([0.23, 0.05, 0.15, 0.08])
    eje_boton3 = plt.axes([0.41, 0.05, 0.15, 0.08])
    eje_boton4 = plt.axes([0.59, 0.05, 0.15, 0.08])
    eje_boton5 = plt.axes([0.77, 0.05, 0.15, 0.08])
    
    btn_orig = Button(eje_boton1, "Original")
    btn_f1 = Button(eje_boton2, "Fondo 1")
    btn_f2 = Button(eje_boton3, "Fondo 2")
    btn_save = Button(eje_boton4, "Guardar")
    btn_rep = Button(eje_boton5, "Reporte")
    
    btn_orig.on_clicked(click_original)
    btn_f1.on_clicked(click_fondo1)
    btn_f2.on_clicked(click_fondo2)
    btn_save.on_clicked(click_guardar)
    btn_rep.on_clicked(click_reporte)
    
    # muestra la ventana en pantalla y pausa el codigo hasta q la cierren
    plt.show()
    
if __name__ == "__main__":
    inicio()