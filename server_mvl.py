#encoding: utf-8
import socket
import threading
import time
from time import time
from dato import * # Importamos la clase Dato.
import buffers as buffers

def inicio_server_mvl():
	hostMACAddress = 'B8:27:EB:F7:2E:49'
	port = 1
	backlog = 1
	size = 2048
	s = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
	s.bind((hostMACAddress,port))
	s.listen(backlog)
	try:
		client = 0
		client, address = s.accept()
		while 1:
			recv1 = client.recv(size)
			if recv1:
				hora_llegada = int(time() * 1000)
				recv1 = recv1 + str(hora_llegada) + ';'
				buffers.lock.acquire()
				try:
					dato1 = parse(recv1)
					buffers.lista_buffer(dato1)
					client.send(recv1)
				finally:
					buffers.lock.release()
				#print ('Datos recibidos', recv1)
	except:	
		#print("Closing socket")
		if client != 0:	
			client.close()
		s.close()
	print 'FINALIZADO: thread_server'
	
	"""while True:
		hora_llegada = int(time() * 1000)
		buffers.lock.acquire()
		try:
			recv1 = "1;-1;-1;-1;-1;-1;-1;-1;0.213421;-0.046935;0.529423;2.950227;0.037296;-1.357316;1597939143486;1597939143840;1597939192112"
			dato = parse(recv1)
			#print "Mvl - Hora de llegada: " + str(hora_llegada)
			#dato.imprimir()
			#buffers.lista_buffer(dato)
		finally:
			buffers.lock.release()"""
