import numpy as np
###########################################################################################
# This library contains python function for  "pose" resolving problems
# from data comming from:
# a) An on board sensor detecting fiducial or other type of markers or references, where
# the sensed data is given in form of Rodrigues vector and translation vector
# b) An external in-placement fixed sensor tracking visual beacons: in this case three beacons
# (red, green and blue)
#########################################################################################
######################################################################
# Auxiliary functions
######################################################################
# vector2DAngle -> Angle of vector
# normalizeAngle -> Conversion to the 0 - 2*pi range
# rotx -> Rotation matrix for x axis
# roty -> Rotation matrix for y axis
# rotz -> Rotation matrix for z axis

def vector2DAngle(r):
    # angle = vector2DAngle(r)
    # returned angle is between -np.pi and np.pi
    # angle is meassured from the x axis, counter - clockwise
    n=np.linalg.norm(r)
    if(n==0):
        return 0.0
    vec=r/n
    if(vec[0]!=0):
        alfa=np.arctan(abs(vec[1])/abs(vec[0]))
    else:
        if(vec[1]>0):
            return np.pi/2
        else:
            return -np.pi/2
        
    if(vec[0] > 0 and vec[1]>=0):
        return alfa
    if(vec[0] <0 and vec[1]>=0):
        return np.pi-alfa
    if(vec[0] < 0 and vec[1]<0):
        return -(np.pi-alfa)
    if(vec[0]>0 and vec[1]<0):
        return -alfa
    return 0.0

def normalizeAngle(angle):
    # nangle=normalizeAngle(angle)
    # Normalize angle between 0 and 2*pi
    n=angle/(2*np.pi)
    angle=angle-np.fix(n)*2*np.pi
    if(angle < 0):
        return (2*np.pi-abs(angle))
    return angle

def rotx(gamma):
    #R=rotx(gamma)
    # Rotation matrix around x axis (RHS)
    #gamma: rotation angle (radians)
    #R: rotatin matrix 
    R=np.array([[1,0,0],[0,np.cos(gamma),-np.sin(gamma)],[0,np.sin(gamma),np.cos(gamma)]])
    return R

def roty(beta):
    #R=roty(gamma)
    # Rotation matrix around y axis (RHS)
    #gamma: rotation angle (radians)
    #R: rotatin matrix 
    R=np.array([[np.cos(beta),0,np.sin(beta)],[0,1,0],[-np.sin(beta),0,np.cos(beta)]])
    return R

def rotz(alfa):
    #R=rotz(gamma)
    # Rotation matrix around z axis (RHS)
    #gamma: rotation angle (radians)
    #R: rotatin matrix 
    R=np.array([[np.cos(alfa),-np.sin(alfa),0],[np.sin(alfa),np.cos(alfa),0],[0,0,1]])
    return R

##############################################################################
# Rodrigues vector auxiliary functions: 
##############################################################################
# infofromrvec: separate angle from axis information in Rodriges vector
# rfromrvec: get roation matrix from rodrigues vector
# rvecfromr: get Rodrigues vector from rotation matrix
# compose2rvecs: compose two rotations expressed as Rodrigues vectors

def infofromrvec(rvec):
    # (angle,vec)=infofromrvec(rvec)
    # rvec: Rodrigues vector
    # angle: rotation angle obtained from the norm of rvec
    # returned angle is given in the range 0 to 2pi
    # vec: rotation axis described as a unitary vector (column) (RHS)
    # In case of 0 degrees rotation x axis is returned
    angle=np.linalg.norm(rvec)
    if(angle!=0):
        vec = rvec/angle
        vec.shape=(3,1)
    else:
        vec=np.array([1.0,0.0,0.0])
        vec.shape=(3,1)
    angle=normalizeAngle(angle)
    return(angle,vec)

def rfromrvec(rvec):
    # R=rfromrvec(rvec)
    # rvec: Rodrigues vector
    # R: Rotation matrix obtained from Rodrigues formula.
    angle,vec = infofromrvec(rvec)
    M=np.array([[0,-vec[2,0],vec[1,0]],[vec[2,0],0.0,-vec[0,0]],[-vec[1,0],vec[0,0],0.0]]);
    R=np.cos(angle)*np.identity(3)+(1-np.cos(angle))*np.matmul(vec,vec.transpose())+np.sin(angle)*M
    return R

def rvecfromr(R):
    # rvec=rvecfromr(R)
    # R: rotation matrix (RHS)
    # rvec: Rodrigues vector
    tol=1e-7
    # From Rodrigues formula:
    M=(R-R.transpose())/2
    rx=M[2,1]
    ry=M[0,2]
    rz=M[1,0]
    r=np.array([rx,ry,rz])
    r.shape=(3,1)
    n=np.linalg.norm(r)
    # Flag to mark the special case of R very near identity
    diagones=0

    if(abs(R[0,0]-1)<tol and abs(R[1,1]-1)<tol and abs(R[2,2]-1)<tol):
        diagones=1
    # Detecting very small rotation angles:
    if(abs(n)<tol and diagones==1 and abs(R[0,1])<tol and abs(R[0,2])<tol and abs(R[1,2])<tol ):
         return np.array([0.0,0.0,0.0])
 
    #Special cases theta = 0 or pi
    if(abs(n)<tol): # Deeming the special case Theta=pi, Theta=0
        rx=1.0
        ry=1.0
        rz=1.0
        # Avoiding numerical problems:
        if(R[1,1]<-1):
            ry=0.0
        if(R[0,0]<-1):
            rx=0.0
        if(R[2,2]<-1):
            rz=0.0
        #rx and ry and rz differente from 0
        if(rx!=0 and ry!=0 and rz!=0):
            rx=np.sqrt(0.5*(R[0,0]+1))
            ry=np.sqrt(0.5*(R[1,1]+1))
            rz=np.sqrt(0.5*(R[2,2]+1))
            if(R[0,1]<0):
                rx=-rx
            if(R[1,2]<0):
                rz=-rz
            return np.pi*np.array([rx,ry,rz])
        if(rx!=0 and ry!=0):
            rx=np.sqrt(0.5*(R[0,0]+1))
            ry=np.sqrt(0.5*(R[1,1]+1))
            if(R[0,1]<0):
                rx=-rx
            return np.pi*np.array([rx,ry,rz])
        if(ry!=0 and rz!=0):
            rz=np.sqrt(0.5*(R[2,2]+1))
            ry=np.sqrt(0.5*(R[1,1]+1))
            if(R[1,2]<0):
                rz=-rz
            return np.pi*np.array([rx,ry,rz])
        if(rx!=0 and rz!=0):
            rx=np.sqrt(0.5*(R[0,0]+1))
            rz=np.sqrt(0.5*(R[2,2]+1))
            if(R[0,2]<0):
                rz=-rz
            return np.pi*np.array([rx,ry,rz])
        return np.pi*np.array([rx,ry,rz])

    # General case for theta
    r=r/n
    stheta=0.0
    if(rx!=0):
        stheta=rx/r[0]
    else:
        if(ry!=0):
            stheta=ry/r[1]
        else:
            if(rz!=0):
                stheta=rz/r[2]
    # Avoiding numerical problems
    if(stheta>1):
        stheta=1
    if(stheta<-1):
        stheta=-1
    theta=np.arcsin(stheta)
    # Solving sin(theta)=sin(pi-theta)
    Rtrial1=rfromrvec(theta*r)
    Rtrial2=rfromrvec((np.pi-theta)*r)
    diff1=np.linalg.norm(R-Rtrial1)
    diff2=np.linalg.norm(R-Rtrial2)
    if(diff2<diff1):
        theta=np.pi-theta

    return theta*r

def compose2rvecs(rvec1,rvec2):
    # rvec=compose2rvecs(rvec1,rvec2)
    # rvec1 is first Rodrigues vector to apply, then rvec2 Rodrigues vector
    # rvec: Resulting Rodrigues vector
    # R is obtained considering a vector as a column matrix.
    R1=rfromrvec(rvec1)
    R2=rfromrvec(rvec2)
    R=np.matmul(R2,R1)
    rvec=rvecfromr(R)
    return rvec

###########################################################################################
# Pose resolution functions
# getPose: get the pose from on board sensor for fixed markers and marker geometric info
# projectPoseZX: given a 3D rotation gets the resulting rotion angle of the z axis in xy, zx o yz planes (RHS)
# printPose: Pretty-print of on board sensor information for fixed marker 

def getPose(rvecp, tp, rvecMarker, tMarker):
    # (rvec,tc,R)=getPose(revecp,tp,rvecMarker,tMarker)
    # Get the pose from on board sensor for marker and marker geometric information
    # rvecp: Rodrigues vector comming from sensor. It represents geometric rotation of
    # the marker in the on board sensor reference system
    # tp: Displacement vector coming from sensor. It represents geometric displacement of
    # the marker in the on board sensor reference system
    # rvecMarker: Rodrigues vector representing geometric rotation of the marker
    # in the external fixed reference system
    # tMarker: Displacement vector representing geometric displacement of the marker in
    # the external fixed reference system
    #  Output:
    # rvec: Rodrigues vector representing geometric rotation of the on board sensor in
    # the external fixed reference system
    # tc: Vector representing geometric displacement of the on board sensor in the external fixed
    # reference system.
    # R: rotation matrix equivalent to rvec
    RMarker=rfromrvec(rvecMarker)
    Rp=rfromrvec(rvecp)
    #Rinv=np.matmul(RMarker,Rp.transpose())
    Rinv=np.matmul(RMarker.transpose(),Rp)
    t=np.matmul(Rinv,tp)
    tc=tMarker-t
    R=Rinv.transpose()
    rvec = rvecfromr(R)
    return (rvec,tc,R)

def projectPoseZX(rvec):
    # theta=projectPoseZX(rvec)
    # rvec: Rodrigues vector representing a geometric rotation.
    # theta: The projected angle between the rotated 2D vector and the original z axis 
    # of the rotated z axis.
    # theta is given normalized between 0 and 2 pi.
    R=rfromrvec(rvec)
    k=np.array([0.0,0.0,1.0]) # z unitary vector
    k.shape=(3,1)
    kp=np.matmul(R.transpose(),k)
    ind1=2
    ind2=0
    #Special cases
    if(kp[ind2]==0 and kp[ind1]>0):
        return 0.0
    if(kp[ind2]==0 and kp[ind1]<0):
        return np.pi
    if(kp[ind2]>0 and kp[ind1]==0):
        return np.pi/2
    if(kp[ind2]<0 and kp[ind1]==0):
        return 3*np.pi/2
    if(kp[ind2]==0 and kp[ind1]==0):
        return 0.0
    atan=np.arctan(abs(kp[ind1])/abs(kp[ind2]))
    if(kp[ind2]>0 and kp[ind1]>0):
        atan= np.pi/2 - atan
    if(kp[ind2]<0 and kp[ind1]>0):
        atan= atan-np.pi/2
    if(kp[ind2]<0 and kp[ind1]<0):
        atan= -np.pi/2-atan
    if(kp[ind2]>0 and kp[ind1]<0):
        atan= np.pi/2+atan
    return normalizeAngle(atan)

def printPose(rv2,tv2,rvec1,tvec1):
    ####################################################
    # printPose(rvec2,tvec2,rvec1,tvec1)
    # rvec2:  Rodrigues vector given by the on board marker sensor representing
    # rotation of the marker in the sensor reference system
    # tvec2: Displacement vector given by the on board marker sensor representing
    # marker position in the sensor reference system
    # rvec1: Rodrigues vector representing marker rotation in the fixed reference system
    # tvec1: Displacement vector representing marker position in the fixed reference system
    [rvec3,tvec3,R3]=getPose(rv2,tv2,rvec1,tvec1)
    angle,axis=infofromrvec(rvec3)
    print("Test 1: ")
    print("Rvec from robot:"+str(rv2))
    print("Tvec from robot:"+str(tv2))
    print("Robot location from fixed reference frame:")
    print("==========================================")
    print("Rotation: Angle: "+str(angle)+" Axis: "+str(axis))
    print("Displacement: " + str(tvec3))
    theta=projectPoseZX(rvec3)
    print("ZX Plane Projected angle: "+str(theta))
    ####################################################

##################################################################
# Functions for Pose information from visual beacons detection
# getOrientationFromBeacons: get rotation of the system from the detected position
# of three beacons and the 0 degree rotation 0 displacement of the system 
# getPositionFromBeacons: get position of a reference point in the system  given the 
# position of this point in non-rotated zero displacement situation, the position of the
# beacon on the same situation and the measured position of the beacon and the measured rotation
# of the system

def getOrientationFromBeacons(vRed,vBlue,vGreen, posR0, posB0, posG0):
    # (dBR,dRG,dBG)=getOrientationFromBeacons(vRed,vBlue,vGreen,posR0,posB0,posG0)
    # vRed,vBlue,vGreen: vectors 2D with position of red, blue and green beacons
    # The triangle of beacons is: Red - Blue - Green, clockwise
    # posR0, posB0, posG0: position of beacons for 0 degrees of rotation
    # Output:
    # Three rotation angle estimations (clockwise)
    # dBR: clockwise rotation calculated from variation of vector from the blue to the red beacon.
    # dRG: clockwise rotation calculated from variation of vector from the red to the green beacon.
    # dBG: clockwise rotation calculated from variation of vector from the blue to the green beacon.
    # Dependencies: this function depends on vector2DAngle.
    vbr=vRed-vBlue
    refbr=posR0-posB0
    thetaBR=vector2DAngle(vbr)
    thetaRefBR=vector2DAngle(refbr)
    deltaThetaBR=normalizeAngle(thetaRefBR-thetaBR)
    vrg=vGreen-vRed
    refrg=posG0-posR0
    thetaRG=vector2DAngle(vrg)
    thetaRefRG=vector2DAngle(refrg)
    deltaThetaRG=normalizeAngle(thetaRefRG-thetaRG)
    vbg=vGreen-vBlue
    refbg=posG0-posB0
    thetaBG=vector2DAngle(vbg)
    thetaRefBG=vector2DAngle(refbg)
    deltaThetaBG=normalizeAngle(thetaRefBG-thetaBG)
    return (deltaThetaBR, deltaThetaRG, deltaThetaBG)

def getPositionFromBeacon(posOnBoardReference,posr0,v,theta):
    # vref=getPositionFromBeacon(posOnBoardReference,posr0,v,theta)
    # Inpput:
    # posOnBoardReference: 2d vector with the position of the reference point onboard.
    # posr0: 2d vector with the position of the beacon for 0 degrees rotation.
    # v: 2d vector with the measured position of the beacon.
    # theta: rotation angle
    posOnBoardReference.shape=(2,1)
    posr0.shape=(2,1)
    v.shape=(2,1)
    delta=posOnBoardReference-posr0
    delta.shape=(2,1)
    alfa=theta
    R=np.array([[np.cos(alfa),np.sin(alfa)],[-np.sin(alfa),np.cos(alfa)]])
    deltarot=np.matmul(R,delta)
    vref=v+deltarot
    return vref
