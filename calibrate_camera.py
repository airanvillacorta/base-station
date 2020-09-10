import numpy as np
#import matplotlib.pyplot as plt
from pathlib import Path
import numpy.polynomial.polynomial as poly
import pandas as pd


name_file_calibration_x = "datosxy.csv"
name_file_calibration_y = "./data.csv"

def calibration_x():
	global name_file_calibration_x

	# Camera setting parameters.
	cy = 360 # Sensor de 1280x720
	cx = 640
	path=Path(".")
	fileName=name_file_calibration_x
	df=np.genfromtxt(path / fileName)
	xp=df[:,3]-cx
	xp.shape=(df.shape[0],1)
	xg=df[:,1]
	xg.shape=(df.shape[0],1)
	sign = xp/np.abs(xp)
	xg=xg*sign
	matxx=np.append(xp,xg,axis=1)
	coefs=poly.polyfit(matxx[:,0],matxx[:,1],3)

	print "# Calibration Data. From pixel x coordinate to spacial position (x axis):"
	print "Polynomial coeffcients: " + str(coefs)
	print "\n###--- CONFIGURE THE VALUES IN THE parameters.py FILE ---###"

def calibration_y():
	global name_file_calibration_y

	# Camera setting parameters.
	alfa = 21*np.pi/180  
	hc = 535
	cy = 360 # Sensor de 1280x720
	cx = 640
	# Values initial of algorithm
	k2=np.tan(alfa)
	k1 = hc
	k3ini=1
	niter=50
	# Datos
	df = pd.read_csv(name_file_calibration_y,' ')
	y=-(df['Y']-cy) # Inversion: distancias mayores deben dar lugar a valores mayores
	k3=k3ini
	delta=0.1
	for i in range(niter):
	    k3y=(df['Dist']*(k2-k3*y)/k1 -1)/k2
	    ak3 = k3y/y
	    k3=k3+delta*(ak3.mean()-k3)

	pred = k1*(1+k2*k3*y)/(k2-k3*y)

	print "# Camera setting parameters."
	print "alfa = " + str(alfa)
	print "hc = " + str(hc)
	print "cy = " + str(cy)
	print "cx = " + str(cx)
	print "# Calibration Data. From pixel y coordinate to distance from camera base:"
	print "k1 = " + str(k1)
	print "k2 = " + str(k2)
	print "k3 = " + str(k3)
