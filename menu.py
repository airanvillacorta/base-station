#encoding: utf-8
from tkinter2 import gui # Importamos el método gui de la interfaz gráfica.
import threading
import parameters as param # Importamos los parámetros de configuración.
import time
import processdata as process_data # Importamos los métodos de procesamiento de los datos.
import numpy as np
from dato import * # Importamos la clase Dato.
import buffers as buffers
import server_mvl as mvl
import server_camera as camera
import calibrate_camera as calibra_cam # Importamos los parámetros de calibración de cámara externa.

save = False # Opción para guardado de datos de simulación.

# Método del menú.
def option():
    num=-1
    while True:
        print ("\n------. Main .------")
        print ("1) Data simulation visualization.")
        print ("2) Display and save simulation data.")
        print ("3) Camera calibration.")
        print ("4) Show Parameters.")
        print ("5) Exit")
        try:
            num = int(input("Insert an option: "))
            print ("----------------------------")
            return num
        except:
            print("Error: You must enter a valid option.")

        print ("----------------------------")
     
    return num

# Métodos que muestra los parámetros actuales.
def show_parameters():
    f = open ('parameters.py','r')
    mensaje = f.read()
    print(mensaje)
    f.close()
    
def server_mvl():
    mvl.inicio_server_mvl()

def server_camera():
    camera.inicio_server_camera()

# Método que realiza la simulación de los buffers.
def simulation_data():
    global save

    if save == True:
        archivo = open("salida-simulacion.txt", "w")

    while True:
        if buffers.buf_lib == 1 and len(buffers.l1) == 10:
            #print "Buffer 1 - "
            i = 0
            arreglo = np.zeros((10,17), dtype=float)
            while i < 10: # Recorremos el buffer.
                if save == True:
                    archivo.write(buffers.l1[i].imprimir())
                arreglo[i] = buffers.l1[i].arreglo()
                i+=1
            
            process_data.simulation(arreglo)
            buffers.l1 = []
            buffers.buf_lib = -1

        elif buffers.buf_lib == 2 and len(buffers.l2) == 10:
            #print "Buffer 2 - "
            i = 0
            arreglo = np.zeros((10,17), dtype=float)
            while i < 10: # Recorremos el buffer.
                if save == True:
                    archivo.write(buffers.l2[i].imprimir())
                arreglo[i] = buffers.l2[i].arreglo()
                i+=1
            
            process_data.simulation(arreglo)
            buffers.l2 = []
            buffers.buf_lib = -1
            
        if param.close:
            if save == True:
                archivo.close()
                save = False
            break


# Main del programa principal.
def main():
    global save
    
    value_option = 0
    buffers.lock = threading.Lock()
     
    while True:
        value_option = option()
     
        if value_option == 1:
            print ("Option 1. Data simulation visualization")
            thread_mvl = threading.Thread(target=server_mvl)
            thread_camera = threading.Thread(target=server_camera)
            thread_simulation = threading.Thread(target=simulation_data)
            thread_mvl.start()
            thread_camera.start()
            thread_simulation.start()
            gui()
            
        elif value_option == 2:
            print ("Option 2. Display and save simulation data")
            save = True
            thread_mvl = threading.Thread(target=server_mvl)
            thread_camera = threading.Thread(target=server_camera)
            thread_simulation = threading.Thread(target=simulation_data)
            thread_mvl.start()
            thread_camera.start()
            thread_simulation.start()
            gui()

        elif value_option == 3:
            print ("Option 3. Camera calibration\n")
            calibra_cam.calibration_y()
            calibra_cam.calibration_x()
            
        elif value_option == 4:
            print ("Option 4. Show Parameters.\n")
            show_parameters()
            
        elif value_option == 5:
            break
        else:
            print ("You must enter an option betwen 1 and 5")
     
    print ("Quit")

# Hacemos que la primera función en ejecutarse sea el Main.
if __name__== "__main__":
    main()
