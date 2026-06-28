import numpy as np #redimensionar imagen
import matplotlib.pyplot as plt #ventana grafica
from matplotlib.widgets import Button #botones de la ventana grafica
import datetime as dt #para el archivo de reporte
from PIL import Image #resize y guardar imagen

from imagenes import selecion_imagen_principal, fondos_alternativos, cargar_imagen
from procesamiento import recibir_imagen, reemplazar_fondo, coordenadas_objeto, reporte

#crear los botones y ventana
# a comer