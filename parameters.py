#encoding: utf-8
import numpy as np

##---------- Parameters GUI.
counter = 0
close = False
# Datos procesados
fTheta = np.nan
fX = np.nan
fZ = np.nan
bxRed = np.nan
cpdRed = np.nan
bxBlue = np.nan
cpdBlue = np.nan
bxGreen = np.nan
cpdGreen = np.nan
fThetaFromCamera = np.nan
fXFromCamera = np.nan
fZFromCamera = np.nan
ibuffer = np.nan
nRobot = np.nan
nCamera = np.nan

dif_fTheta = np.nan
dif_fX = np.nan
dif_fZ = np.nan

##---------- Parameters Process Data.
# Fields
rType=0
rRedX=1
rRedY=2
rBlueX=3
rBlueY=4
rGreenX=5
rGreenY=6
rTimeCamera=7
rTVec2X=8
rTVec2Y=9
rTVec2Z=10
rRVec2X=11
rRVec2Y=12
rRVec2Z=13
rTimeRobot=14
rTimeSend=15
rTimeArrival=16
rTimeEvent=17
#Buffer Size
bufferSize=10
#Maximum time interval to consider events (ms) 
maxTimeInterval=5000
#Fiducial markers parameters:
fiducialRVec=np.array([[0.0,0.0,np.pi]])
#fiducialTVec=np.array([[0.0,0.65,0.0]])
fiducialTVec=np.array([[0.0,0.53,0.0]])
#nbuffers=int(data.shape[0]/bufferSize)
#Camera setting parameters
alfa=45*np.pi/180 #Camera angle
#hc=650 #Camera height
hc=535
cy=360
cx=640 #Center of sensor (1280x720)
#Robot setting parameters
posr0=np.array([0.0,100.0]) # x z of the red ball coordinates in mm
posb0=np.array([100.0,-100.0]) # x z of the blue ball coordinates in mm
posg0=np.array([-100.0,-100.0]) # x z of the green ball coordinates in mm 
posOnBoardReference=np.array([0.0,0.0])
posOnBoardSensor=np.array([0.0,0.0])
#Constants in transformation formula (from pixels to camera space)
#From pixel y coordinate to distance from camera base
k2=np.tan(alfa)
k1=hc
k3=0.00103115
#From pixel x coordinate to spacial position (x axis)
coefs=[-4.23114630e+01, 1.55369776e+00,1.77375302e-04,-2.30734064e-06]
