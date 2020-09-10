import numpy as np
import numpy.polynomial.polynomial as poly
import location as loc
import parameters as param

#data=np.genfromtxt("datos2.txt")

#data=np.array([[1,384.257893191,473.623016329,424.805570569,400.815191151,275.660551443,460.326759712,1597939196315,-1,-1,-1,-1,-1,-1,-1,-1,-1],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112],[1,-1,-1,-1,-1,-1,-1,-1,0.213421,-0.046935,0.529423,2.950227,0.037296,-1.357316,1597939143486,1597939143840,1597939192112]])

def print_process_info(fTheta,fX,fZ,bxRed,cpdRed,bxBlue,cpdBlue,bxGreen,cpdGreen,fThetaFromCamera,fXFromCamera,fZFromCamera,ibuffer,nRobot,nCamera):
    print("fTheta: "+str(fTheta)+" fX: "+str(fX)+" fZ: "+str(fZ))
    print("xRed: "+str(bxRed) +"cpdRed: "+str(cpdRed)+ \
            "xBlue: "+str(bxBlue)+ " cpdBlue: "+str(cpdBlue)+ \
            "xGreen: "+str(bxGreen)+" cpdGreen: "+str(cpdGreen))
    print("fThetaFromCamera: "+str(fThetaFromCamera)+" fXFromCamera: "+str(fXFromCamera)+" fZFromCamera: "+str(fZFromCamera))
    print("Processed buffer "+str(ibuffer)+" nRobot: "+str(nRobot)+" nCamera : "+str(nCamera))
    print("##############################################################")
    
    
def update_process_info(fTheta,fX,fZ,bxRed,cpdRed,bxBlue,cpdBlue,bxGreen,cpdGreen,fThetaFromCamera,fXFromCamera,fZFromCamera,ibuffer,nRobot,nCamera):
    param.fTheta = fTheta
    param.fX = fX
    param.fZ = fZ
    param.bxRed = bxRed
    param.cpdRed = cpdRed
    param.bxBlue = bxBlue
    param.cpdBlue = cpdBlue
    param.bxGreen = bxGreen
    param.cpdGreen = cpdGreen
    param.fThetaFromCamera = fThetaFromCamera
    param.fXFromCamera = fXFromCamera
    param.fZFromCamera = fZFromCamera
    param.ibuffer = ibuffer
    param.nRobot = nRobot
    param.nCamera = nCamera
    
    param.counter += 1
    
    a = fThetaFromCamera
    b = fTheta
    aa = fXFromCamera/1000
    bb = fX
    aaa = fZFromCamera/1000
    bbb = fZ
    if a<b:
        param.dif_fTheta = b-a
    else:
        param.dif_fTheta = a-b
    if aa<bb:
        param.dif_fX = bb-aa
    else:
        param.dif_fX = aa-bb
    if aaa<bbb:
        param.dif_fZ = bbb-aaa
    else:
        param.dif_fZ = aaa-bbb


def simulation(data):
    #print(data)
    #print("Registers: "+str(data.shape[0]))
    #print("Fields: "+str(data.shape[1]))

    fxlinfit=poly.Polynomial(param.coefs) #Polynomial function obtained from regression to estimate x

    # Processing each buffer
    ibuffer=0
    #for ibuffer in range(nbuffers):
    #print("###########################################")
    #print("Data from buffer "+str(ibuffer))
    indstart=ibuffer*param.bufferSize
    # Get the buffer
    databuffer=data[indstart:(indstart+param.bufferSize),0:data.shape[1]]
    # Select registers comming from the robot and estimate time correction
    selectRobotRegisters = databuffer[:,param.rType]==1
    buffer_robotType=databuffer[selectRobotRegisters,:]
    diffTimes = buffer_robotType[:,param.rTimeArrival]-buffer_robotType[:,param.rTimeSend]
    diffTime = np.mean(diffTimes)
    # Add new column, copy rTimeCamera values for camera registers and
    # corrected times for robot registers
    column = databuffer[:,param.rTimeCamera]
    column.shape=(param.bufferSize,1)
    databuffer=np.append(databuffer,column,axis=1)
    databuffer[selectRobotRegisters,param.rTimeEvent]=databuffer[selectRobotRegisters,param.rTimeRobot]+diffTime
    # We get those events that area in the same time window of the first one.
    delta = databuffer[:,param.rTimeEvent]-databuffer[0,param.rTimeEvent]
    inTimeInterval = delta<=param.maxTimeInterval
    databuffer=databuffer[inTimeInterval,:]
    # Separate registers: fiducial system  - camera system
    selectRobotRegisters = databuffer[:,param.rType]==1
    dataRobot=databuffer[selectRobotRegisters,:]
    dataCamera = databuffer[np.logical_not(selectRobotRegisters),:]
    #Calculations
    #General parameters
    nRobot = dataRobot.shape[0]
    nCamera = dataCamera.shape[0]
    nOutOfInterval = param.bufferSize-databuffer.shape[0]
    #deltaTime = databuffer[-1,rTimeEvent]-databuffer[0,rTimeEvent]
    #Fiducial markers measurements
    dataFiducial = np.zeros((nRobot,10))
    #print("Fiducial location info. for "+str(nRobot)+" events:")
    #Process each obtained fiducial register
    for irobot in range(dataRobot.shape[0]):
        rvec2=np.array([dataRobot[irobot,param.rRVec2X],dataRobot[irobot,param.rRVec2Y],dataRobot[irobot,param.rRVec2Z]])
        tvec2=np.array([dataRobot[irobot,param.rTVec2X],dataRobot[irobot,param.rTVec2Y],dataRobot[irobot,param.rTVec2Z]])
        fiducialMarker = 0  #TODO: this should be obtained from data 
        rvec1=param.fiducialRVec[fiducialMarker]
        tvec1=param.fiducialTVec[fiducialMarker]
        [rvec3,tvec3,R3]=loc.getPose(rvec2,tvec2,rvec1,tvec1)
        theta=loc.projectPose(rvec3,2,0)
        dataFiducial[irobot,0]=theta
        dataFiducial[irobot,1]=tvec3[0]
        dataFiducial[irobot,2]=tvec3[2]
        dataFiducial[irobot,3]=fiducialMarker
        dataFiducial[irobot,4:7]=rvec3.transpose()
        dataFiducial[irobot,7:10]=tvec3.transpose()
        #print(str(dataFiducial[irobot,0:3]))
    #Aggregate of fiducial processed registers
    if(nRobot>0):
        fTheta=np.nanmean(dataFiducial[:,0])
        fX=np.nanmean(dataFiducial[:,1])
        fZ=np.nanmean(dataFiducial[:,2])
    else:
        fTheta=np.nan
        fX=np.nan
        fZ=np.nan
    #Camera measurements
    #0,1,2: Is ball detected?
    dataBallLocation=np.zeros((nCamera,15))
    #print("Camera location info. for "+str(nCamera)+" events:")
    #Process each obtained camera register
    
    #Initialize data use Camera
    cpdRed=np.nan
    cpdBlue=np.nan
    cpdGreen=np.nan
    xRed=np.nan
    xBlue=np.nan
    xGreen=np.nan
    for icamera in range(dataCamera.shape[0]):
        red=np.array([dataCamera[icamera,param.rRedX],dataCamera[icamera,param.rRedY]])
        blue=np.array([dataCamera[icamera,param.rBlueX],dataCamera[icamera,param.rBlueY]])
        green=np.array([dataCamera[icamera,param.rGreenX],dataCamera[icamera,param.rGreenY]])
        #Initialize
        cpdRed=np.nan
        cpdBlue=np.nan
        cpdGreen=np.nan
        xRed=np.nan
        xBlue=np.nan
        xGreen=np.nan
        #Check which balls were detected
        if(red[0]==-1 or red[1]==-1):
            dataBallLocation[icamera,0]=0
        else:
            dataBallLocation[icamera,0]=1

        if(blue[0]==-1 or blue[1]==-1):
            dataBallLocation[icamera,1]=0
        else:
            dataBallLocation[icamera,1]=1

        if(green[0]==-1 or green[1]==-1):
            dataBallLocation[icamera,2]=0
        else:
            dataBallLocation[icamera,2]=1

        if(dataBallLocation[icamera,0]):
            y=-(red[1]-param.cy)
            cpdRed=param.k1*(1+param.k2*param.k3*y)/(param.k2-param.k3*y)
            x=red[0]-param.cx
            xRed=fxlinfit(x)
        if(dataBallLocation[icamera,1]):
            y=-(blue[1]-param.cy)
            x=blue[0]-param.cx
            cpdBlue=param.k1*(1+param.k2*param.k3*y)/(param.k2-param.k3*y)
            xBlue=fxlinfit(x)
        if(dataBallLocation[icamera,2]):
            y=-(green[1]-param.cy)
            x=green[0]-param.cx
            cpdGreen=param.k1*(1+param.k2*param.k3*y)/(param.k2-param.k3*y)
            xGreen=fxlinfit(x)
        dataBallLocation[icamera,3]=xRed
        dataBallLocation[icamera,4]=cpdRed
        dataBallLocation[icamera,5]=xBlue
        dataBallLocation[icamera,6]=cpdBlue
        dataBallLocation[icamera,7]=xGreen
        dataBallLocation[icamera,8]=cpdGreen
    #Agregate of processed camera registers
    if(nCamera>0):
        #print(str(dataBallLocation))
        bxRed=np.nanmean(dataBallLocation[:,3])
        bzRed=np.nanmean(dataBallLocation[:,4])
        vRed=np.array([bxRed,bzRed])
        bxBlue=np.nanmean(dataBallLocation[:,5])
        bzBlue=np.nanmean(dataBallLocation[:,6])
        vBlue=np.array([bxBlue,bzBlue])
        bxGreen=np.nanmean(dataBallLocation[:,7])
        bzGreen=np.nanmean(dataBallLocation[:,8])
        vGreen=np.array([bxGreen,bzGreen])
        [fThetaFromBR,fThetaFromRG,fThetaFromBG]=loc.getOrientationFromBeacons(vRed,vBlue,vGreen,param.posr0,param.posb0,param.posg0)
        fThetaFromCamera = np.mean(np.array([fThetaFromBR,fThetaFromRG,fThetaFromBG]))
        vFromR=loc.getPositionFromBeacon(param.posOnBoardReference,param.posr0,vRed,fThetaFromCamera)
        vFromB=loc.getPositionFromBeacon(param.posOnBoardReference,param.posb0,vBlue,fThetaFromCamera)
        vFromG=loc.getPositionFromBeacon(param.posOnBoardReference,param.posg0,vGreen,fThetaFromCamera)
        fXFromCamera=np.nanmean([vFromR[0],vFromG[0],vFromB[0]])
        fZFromCamera=np.nanmean([vFromR[1],vFromG[1],vFromB[1]])
    else:
        bxRed=np.nan
        bzRed=np.nan
        bxBlue=np.nan
        bzBlue=np.nan
        bxGreen=np.nan
        bzGreen=np.nan
        fThetaFromCamera=np.nan
        fXFromCamera=np.nan
        fZFromCamera=np.nan
        
    #print_process_info(fTheta,fX,fZ,bxRed,cpdRed,bxBlue,cpdBlue,bxGreen,cpdGreen,fThetaFromCamera,fXFromCamera,fZFromCamera,ibuffer,nRobot,nCamera)
    update_process_info(fTheta,fX,fZ,bxRed,cpdRed,bxBlue,cpdBlue,bxGreen,cpdGreen,fThetaFromCamera,fXFromCamera,fZFromCamera,ibuffer,nRobot,nCamera)

