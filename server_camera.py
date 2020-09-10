#encoding: utf-8
import socket
import threading
import time
from time import time
from dato import * # Importamos la clase Dato.
import buffers as buffers
import cv2

def dibujar(mask, color, font, frame):
	contornos,_=cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	xx=-1
	yy=-1
	for c in contornos:
		area = cv2.contourArea(c)
		if area > 1500:
			M = cv2.moments(c)
			if M['m00'] == 0 : M['m00'] = 1
			x = int(M['m10']/M['m00'])
			y = int(M['m01']/M['m00'])
			xx = float(M['m10']/M['m00'])
			yy = float(M['m01']/M['m00'])
			nuevoContorno = cv2.convexHull(c)
			cv2.circle(frame, (x,y), 7, color, -1)
			cv2.putText(frame, '(x: ' + str(x) + ', y: ' + str(y) + ')', (x+10,y), font, 0.75, (0,255,0), 1, cv2.LINE_AA)
			cv2.drawContours(frame, [nuevoContorno], 0, color, 3)
			return xx, yy
	return xx, yy

def inicio_server_camera():
	# Captura cam.
	cap = cv2.VideoCapture(0)

	# Nucleo para aplicar transformaciones morfologicas.
	kernel = np.ones((3,3), np.uint8)

	# Color rojo.
	redBajo1 = np.array([1,150,10], np.uint8)
	redAlto1 = np.array([8,255,255], np.uint8)

	redBajo2 = np.array([175,150,10], np.uint8)
	redAlto2 = np.array([179,255,255], np.uint8)

	# Color azul.
	azulBajo = np.array([100,100,20], np.uint8)
	azulAlto = np.array([125,255,255], np.uint8)

	# Color verde.
	verdeBajo = np.array([40,40,20], np.uint8)
	verdeAlto = np.array([75,255,255], np.uint8)

	# Tipo de fuente.
	font = cv2.FONT_HERSHEY_SIMPLEX


	while True:
		ret, frame = cap.read()
	  
		if ret==True:

			frameHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
			maskRed1 = cv2.inRange(frameHSV, redBajo1, redAlto1)
			maskRed2 = cv2.inRange(frameHSV, redBajo2, redAlto2)
			maskRed = cv2.add(maskRed1, maskRed2)
			maskBlue = cv2.inRange(frameHSV, azulBajo, azulAlto)
			maskGreen = cv2.inRange(frameHSV, verdeBajo, verdeAlto)

			maskRed = cv2.dilate(maskRed, kernel) # 2. Dilate
			maskBlue = cv2.dilate(maskBlue, kernel) # 2. Dilate
			maskGreen = cv2.morphologyEx(maskGreen, cv2.MORPH_OPEN, kernel) # 3. Opening
			maskGreen = cv2.dilate(maskGreen, kernel) # 2. Dilate


			Ax, Ay = dibujar(maskRed, (0,0,255), font, frame)
			Bx, By = dibujar(maskBlue, (255,0,0), font, frame)
			Cx, Cy = dibujar(maskGreen, (0,255,0), font, frame)
			hora_captura = int(time() * 1000)
			if Ax!=-1 and Ay!=-1 or Bx!=-1 and By!=-1 or Cx!=-1 and Cy!=-1:
				recv2 = '0;' + str(Ax) + ';' + str(Ay) + ';' + str(Bx) + ';' + str(By) + ';' + str(Cx) + ';' + str(Cy) + ';' + str(hora_captura) + ';'
				buffers.lock.acquire()
				try:
					dato2 = parse(recv2)
					buffers.lista_buffer(dato2)
				finally:
					buffers.lock.release()

		cv2.imshow('Ventana Basica', frame) # Visualizamos ventana frame.
		if cv2.waitKey(1) & 0xFF == ord('q'): # Cerramos la aplicacion con la tecla 'q'.
			break
			
	cap.release()
	cv2.destroyAllWindows()
	print 'FINALIZADO: thread_cam'
	
	"""while True:
		hora_llegada = int(time() * 1000)
		buffers.lock.acquire()
		try:
			recv1 = "0;384.257893191;473.623016329;424.805570569;400.815191151;275.660551443;460.326759712;1597939196315;-1;-1;-1;-1;-1;-1;-1;-1;-1"
			dato = parse(recv1)
			#print "Camera - Hora de llegada: " + str(hora_llegada)
			#dato.imprimir()
			buffers.lista_buffer(dato)
		finally:
			buffers.lock.release()"""
