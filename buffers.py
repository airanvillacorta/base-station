#encoding: utf-8
from dato import * # Importamos la clase Dato.

# Elementos de los Buffers.
l1 = [] # Contendrá una cantidad determinada de elementos tipo Dato.
l2 = []
buf_act = 1 # Disponible para meter datos.
buf_lib = -1 # Indica el buffer libre para que se procese: 1 -> l1 , 2 -> l2

look = "" # Contiene el bloqueador de hilos compartido.

def lista_buffer(dato):
	global l1, l2, buf_act, buf_lib

	if buf_act == 1 and len(l1) < 10:
		l1.append(dato)
	elif buf_act == 1 and len(l1) == 10:
		if buf_lib == -1:
			buf_act = 2
			l2.append(dato)
			buf_lib = 1
	elif buf_act == 2 and len(l2) < 10:
		l2.append(dato)
	elif buf_act == 2 and len(l2) == 10:
		if buf_lib == -1:
			buf_act = 1
			l1.append(dato)
			buf_lib = 2
