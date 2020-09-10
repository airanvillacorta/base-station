#encoding: utf-8
import numpy as np

class Dato:
	tipo = -1
	rVecsX = -1
	rVecsY = -1
	rVecsZ = -1
	tVecsX = -1
	tVecsY = -1
	tVecsZ = -1
	time_cap_mvl = -1
	time_salida_mvl = -1
	time_llegada_mvl = -1
	time_cap_cam = -1
	Ax = -1
	Ay = -1
	Bx = -1
	By = -1
	Cx = -1
	Cy = -1

	def __init__(self):
		pass
		
	def imprimir(self):
		return str(self.tipo) + " " + str(self.Ax) + " " + str(self.Ay) + " " + str(self.Bx) + " " + str(self.By) + " " + str(self.Cx) + " " + str(self.Cy) + " " + str(self.time_cap_cam) + " " + str(self.tVecsX) + " " + str(self.tVecsY) + " " + str(self.tVecsZ) + " " + str(self.rVecsX) + " " + str(self.rVecsY) + " " + str(self.rVecsZ) + " " + str(self.time_cap_mvl) + " " + str(self.time_salida_mvl) + " " + str(self.time_llegada_mvl) + "\n"

	def arreglo(self):
		arreglo = np.array([self.tipo, self.Ax, self.Ay, self.Bx, self.By, self.Cx, self.Cy, self.time_cap_cam, self.tVecsX, self.tVecsY, self.tVecsZ, self.rVecsX, self.rVecsY, self.rVecsZ, self.time_cap_mvl, self.time_salida_mvl, self.time_llegada_mvl])
		return arreglo


# Datos recibidos. tipo;Ax;Ay;Bx;By;Cx;Cy;time_cap_cam;tVecsX;tVecsY;tVecsZ;rVecsX;rVecsY;rVecsZ;time_cap_mvl;time_salida_mvl;time_llegada_mvl;
def parse(cadena): 
	buf = ""
	count = 0

	if cadena[0] == "1": # Recibido desde el móvil. 1;-1;-1;-1;-1;-1;-1;1597916024485;-1;-1;-1;-1;-1;-1;-1;-1;-1;
		d1 = Dato()
		for i in cadena:
			if i == ";":
				count = count + 1
				if count == 1:
					d1.tipo = int(buf)
				elif count == 9:
					d1.tVecsX=float(buf)
				elif count == 10:
					d1.tVecsY=float(buf)
				elif count == 11:
					d1.tVecsZ=float(buf)
				elif count == 12:
					d1.rVecsX=float(buf)
				elif count == 13:
					d1.rVecsY=float(buf)
				elif count == 14:
					d1.rVecsZ=float(buf)
				elif count == 15:
					d1.time_cap_mvl=int(buf)
				elif count == 16:
					d1.time_salida_mvl=int(buf)
				elif count == 17:
					d1.time_llegada_mvl=int(buf)

				buf = ""
				continue
			buf = buf + i

		return d1
		
	elif cadena[0] == "0": # Recibido desde la cámara. 0;-1;-1;-1;-1;-1;-1;1597916024485;-1;-1;-1;-1;-1;-1;-1;-1;-1;
		d2 = Dato()
		for i in cadena:
			if i == ";":
				count = count + 1
				if count == 1:
					d2.tipo = int(buf)
				elif count == 2:
					d2.Ax=float(buf)
				elif count == 3:
					d2.Ay=float(buf)
				elif count == 4:
					d2.Bx=float(buf)
				elif count == 5:
					d2.By=float(buf)
				elif count == 6:
					d2.Cx=float(buf)
				elif count == 7:
					d2.Cy=float(buf)
				elif count == 8:
					d2.time_cap_cam=int(buf)

				buf = ""
				continue
			buf = buf + i

		return d2
