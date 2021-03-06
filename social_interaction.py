import hangman
import pandas as pd
import numpy as np

import random
# import motion
import almath

from global_settings import *
from naoqi import ALProxy
from naoqi import ALBroker
from naoqi import ALModule

from optparse import OptionParser
from hangman_speechevent import SpeechEventModule

import time

# NAO's IP address
NAO_IP = "169.254.95.24"
NAO_IP = "10.0.1.5"
NAO_PORT = 9559

# Initialize proxies
if NAO_AVAILABLE:
    global tts
    global memory
    tts = ALProxy("ALTextToSpeech", NAO_IP, NAO_PORT)
    tts.enableNotifications()
    motionProxy = ALProxy("ALMotion", NAO_IP, NAO_PORT)
    postureProxy = ALProxy("ALRobotPosture", NAO_IP, NAO_PORT)
    
def nao_speech(possible_sentences, nao_available=True):
    """
    Let Nao randomly select one of the possible sentences and speak them out loud
    """
    if nao_available:
        tts.say("\\bound=S\\\\rspd=75\\" + random.choice(possible_sentences))
    else:
        print(random.choice(possible_sentences))

def StiffnessOn(proxy):
    # We use the "Body" name to signify the collection of all joints
    pNames = "Body"
    pStiffnessLists = 1.0
    pTimeLists = 1.0
    motionProxy.stiffnessInterpolation(pNames, pStiffnessLists, pTimeLists)

def move_right_arm(rawTargetCoordinateList, timeFactor=1, isAbsolute=False):
	
	# Set NAO in Stiffness On
	StiffnessOn(motionProxy)

	# Get NAOs space
	space = motion.FRAME_ROBOT

	useSensor = False
	effectorInit = np.array(motionProxy.getPosition("RArm", space, useSensor))

	targetCoordinateList = (effectorInit + np.array(rawTargetCoordinateList)).tolist()

	# Since the line above does not seem to work
	targetCoordinateList = rawTargetCoordinateList

	effectorList = ["RArm"]

	# Enable Whole Body Balancer
	isEnabled  = True
	motionProxy.wbEnable(isEnabled)

	# Legs are constrained fixed
	stateName  = "Fixed"
	supportLeg = "Legs"
	motionProxy.wbFootState(stateName, supportLeg)

	# Constraint Balance Motion
	isEnable   = True
	supportLeg = "Legs"
	motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

	axisMaskList = [almath.AXIS_MASK_VEL] # for "RArm"

	# Determine the time stamps for the movements of the arm
	timesList  = [
		[timeFactor * (i+1) for i in range(len(targetCoordinateList[0]))]
		] # for "RArm" in seconds

	 # called cartesian interpolation
	motionProxy.positionInterpolations(effectorList, space, targetCoordinateList,
	                             axisMaskList, timesList, isAbsolute)

	# Deactivate whole body
	isEnabled    = False
	motionProxy.wbEnable(isEnabled)

def move_both_arms(rawTargetCoordinateList, timeFactor=1, isAbsolute=False):
	
	# Set NAO in Stiffness On
	StiffnessOn(motionProxy)

	# Get NAOs space
	space = motion.FRAME_ROBOT

	useSensor = False
	effectorInit = np.array(motionProxy.getPosition("RArm", space, useSensor))

	targetCoordinateList = (effectorInit + np.array(rawTargetCoordinateList)).tolist()

	# Since the line above does not seem to work
	targetCoordinateList = rawTargetCoordinateList

	effectorList = ["RArm", "LArm"]

	# Enable Whole Body Balancer
	isEnabled  = True
	motionProxy.wbEnable(isEnabled)

	# Legs are constrained fixed
	stateName  = "Fixed"
	supportLeg = "Legs"
	motionProxy.wbFootState(stateName, supportLeg)

	# Constraint Balance Motion
	isEnable   = True
	supportLeg = "Legs"
	motionProxy.wbEnableBalanceConstraint(isEnable, supportLeg)

	axisMaskList = [almath.AXIS_MASK_VEL,
					almath.AXIS_MASK_VEL,] # for "RArm"

	# Determine the time stamps for the movements of the arm
	timesList  = [
		[timeFactor * (i+1) for i in range(len(targetCoordinateList[0]))],
		[timeFactor * (i+1) for i in range(len(targetCoordinateList[1]))]
		] # for "RArm" in seconds

	 # called cartesian interpolation
	motionProxy.positionInterpolations(effectorList, space, targetCoordinateList,
	                             axisMaskList, timesList, isAbsolute)

	# Deactivate whole body
	isEnabled    = False
	motionProxy.wbEnable(isEnabled)

def greeting(nao_available=True):

	# Start social interaction
	nao_speech(["Finally someone who wants to play with me"], nao_available)


        if nao_available:
        
            # Send NAO to Pose Init
            postureProxy.goToPosture("StandInit", 0.7)  

            move_right_arm([
                    [	# Right arm
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.5], # target 4 for "RArm"
                    [0.17, 0.00, 0.09, 0.00, 0.00, 0.5], # target 4 for "RArm"
                    [0.17, 0.00, 0.10, 0.00, 0.00, 0.5], # target 4 for "RArm"
                    [0.17, 0.00, 0.08, 0.00, 0.00, 0.5], # target 4 for "RArm"
                ]
            ],
            timeFactor=0.7)

	nao_speech(["Hi, my name is Naomi, who are you?"], nao_available)

        if nao_available:
        
            move_right_arm([
                    [	# Right arm
                    [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, -0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                    [0.00, 0.00, +0.02, 0.00, 0.00, 0.00], # target 4 for "RArm"
                ]
            ],
            timeFactor=0.5)

	nao_speech(["Nice to meet you"], nao_available)
	nao_speech(["Let's play the hang man game"], nao_available)

        if nao_available:

            move_right_arm([
                    [
                    [0.00, 0.00, 0.00, 0.00, 0.00, 0.00],
                    [-0.11, 0.00, -0.09, 0.00, 0.00, -0.5],
                    ]
            ])
        
	# Send NAO to Pose Init
	nao_speech(["Let me sit down first, I'm an old lady"], nao_available)

        if nao_available:
	    postureProxy.goToPosture("Sit", 0.3)  

def wave():
	# Choregraphe bezier export in Python.
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([ 0.80000, 1.56000, 2.24000, 2.80000, 3.48000, 4.60000])
	keys.append([ [ 0.29602, [ 3, -0.26667, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.17032, [ 3, -0.25333, 0.11200], [ 3, 0.22667, -0.10021]], [ -0.34059, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -0.05987, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.19333, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -0.01078, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("HeadYaw")
	times.append([ 0.80000, 1.56000, 2.24000, 2.80000, 3.48000, 4.60000])
	keys.append([ [ -0.13503, [ 3, -0.26667, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.35133, [ 3, -0.25333, 0.04939], [ 3, 0.22667, -0.04419]], [ -0.41576, [ 3, -0.22667, 0.00372], [ 3, 0.18667, -0.00307]], [ -0.41882, [ 3, -0.18667, 0.00307], [ 3, 0.22667, -0.00372]], [ -0.52007, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -0.37587, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowRoll")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ -1.37902, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ -1.29005, [ 3, -0.25333, -0.03454], [ 3, 0.22667, 0.03091]], [ -1.18267, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -1.24863, [ 3, -0.18667, 0.02055], [ 3, 0.22667, -0.02496]], [ -1.31920, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -1.18421, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowYaw")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ -0.80386, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.69188, [ 3, -0.25333, -0.01372], [ 3, 0.22667, 0.01227]], [ -0.67960, [ 3, -0.22667, -0.01227], [ 3, 0.18667, 0.01011]], [ -0.61057, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.75324, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ -0.67040, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHand")
	times.append([ 1.48000, 4.52000])
	keys.append([ [ 0.00416, [ 3, -0.49333, 0.00000], [ 3, 1.01333, 0.00000]], [ 0.00419, [ 3, -1.01333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderPitch")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ 1.11824, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.92803, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.94030, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ 0.86207, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.89735, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ 0.84212, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderRoll")
	times.append([ 0.72000, 1.48000, 2.16000, 2.72000, 3.40000, 4.52000])
	keys.append([ [ 0.36352, [ 3, -0.24000, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.22699, [ 3, -0.25333, 0.02572], [ 3, 0.22667, -0.02301]], [ 0.20398, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ 0.21779, [ 3, -0.18667, -0.00670], [ 3, 0.22667, 0.00813]], [ 0.24847, [ 3, -0.22667, 0.00000], [ 3, 0.37333, 0.00000]], [ 0.22699, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LWristYaw")
	times.append([ 1.48000, 4.52000])
	keys.append([ [ 0.14722, [ 3, -0.49333, 0.00000], [ 3, 1.01333, 0.00000]], [ 0.11961, [ 3, -1.01333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowRoll")
	times.append([ 0.64000, 1.40000, 1.68000, 2.08000, 2.40000, 2.64000, 3.04000, 3.32000, 3.72000, 4.44000])
	keys.append([ [ 1.38524, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.24241, [ 3, -0.25333, 0.00000], [ 3, 0.09333, 0.00000]], [ 0.34907, [ 3, -0.09333, -0.09496], [ 3, 0.13333, 0.13565]], [ 0.93425, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.68068, [ 3, -0.10667, 0.14138], [ 3, 0.08000, -0.10604]], [ 0.19199, [ 3, -0.08000, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.26180, [ 3, -0.13333, -0.06981], [ 3, 0.09333, 0.04887]], [ 0.70722, [ 3, -0.09333, -0.10397], [ 3, 0.13333, 0.14852]], [ 1.01927, [ 3, -0.13333, -0.06647], [ 3, 0.24000, 0.11965]], [ 1.26559, [ 3, -0.24000, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowYaw")
	times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 3.72000, 4.44000])
	keys.append([ [ -0.31298, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ 0.56447, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.39113, [ 3, -0.22667, 0.03954], [ 3, 0.18667, -0.03256]], [ 0.34818, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ 0.38192, [ 3, -0.22667, -0.03375], [ 3, 0.13333, 0.01985]], [ 0.97738, [ 3, -0.13333, 0.00000], [ 3, 0.24000, 0.00000]], [ 0.82678, [ 3, -0.24000, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHand")
	times.append([ 1.40000, 3.32000, 4.44000])
	keys.append([ [ 0.01490, [ 3, -0.46667, 0.00000], [ 3, 0.64000, 0.00000]], [ 0.01492, [ 3, -0.64000, 0.00000], [ 3, 0.37333, 0.00000]], [ 0.00742, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderPitch")
	times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 4.44000])
	keys.append([ [ 0.24702, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ -1.17193, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ -1.08910, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -1.26091, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -1.14892, [ 3, -0.22667, -0.11198], [ 3, 0.37333, 0.18444]], [ 1.02015, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderRoll")
	times.append([ 0.64000, 1.40000, 2.08000, 2.64000, 3.32000, 4.44000])
	keys.append([ [ -0.24241, [ 3, -0.21333, 0.00000], [ 3, 0.25333, 0.00000]], [ -0.95419, [ 3, -0.25333, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.46024, [ 3, -0.22667, 0.00000], [ 3, 0.18667, 0.00000]], [ -0.96033, [ 3, -0.18667, 0.00000], [ 3, 0.22667, 0.00000]], [ -0.32832, [ 3, -0.22667, -0.04750], [ 3, 0.37333, 0.07823]], [ -0.25008, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RWristYaw")
	times.append([ 1.40000, 3.32000, 4.44000])
	keys.append([ [ -0.31298, [ 3, -0.46667, 0.00000], [ 3, 0.64000, 0.00000]], [ -0.30377, [ 3, -0.64000, -0.00920], [ 3, 0.37333, 0.00537]], [ 0.18250, [ 3, -0.37333, 0.00000], [ 3, 0.00000, 0.00000]]])

	try:
	  motionProxy.angleInterpolationBezier(names, times, keys);
	except BaseException, err:
	  print err

	postureProxy.goToPosture("Sit", 1)  


def winner_move():
	# Choregraphe bezier export in Python.
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.03839, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.03686, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.03686, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.03839, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("HeadYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.05987, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.05833, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.05833, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.05833, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnklePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.92189, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.92189, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.92189, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.92258, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnkleRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.00004, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.00004, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.00004, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.04598, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.05518, [ 3, -0.13333, 0.00920], [ 3, 0.10667, -0.00736]], [ -0.12114, [ 3, -0.10667, 0.01227], [ 3, 0.50667, -0.05829]], [ -0.26687, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.78392, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.78852, [ 3, -0.13333, 0.00460], [ 3, 0.10667, -0.00368]], [ -0.94959, [ 3, -0.10667, 0.00097], [ 3, 0.50667, -0.00460]], [ -0.95419, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHand")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.01680, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.01681, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.01681, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.01682, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -1.59992, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -1.53589, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -1.53589, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -1.53589, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.24088, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.24088, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.24088, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.24088, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipYawPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.56907, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.56907, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.57061, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.57061, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LKneePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 1.10137, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 1.10290, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 1.10290, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 1.10290, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.59515, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.13342, [ 3, -0.13333, 0.35367], [ 3, 0.10667, -0.28294]], [ -1.31468, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.59975, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.01683, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.26994, [ 3, -0.13333, -0.16704], [ 3, 0.10667, 0.13363]], [ 0.91882, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.09362, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LWristYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.62890, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.65958, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.51385, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.84212, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnklePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.92198, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.92351, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.92351, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.92198, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnkleRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.00004, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.00004, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.00004, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.28843, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.28843, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 0.22247, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.72562, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.98018, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.98939, [ 3, -0.13333, -0.00920], [ 3, 0.10667, 0.00736]], [ 1.05382, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.84519, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHand")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.01682, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.01683, [ 3, -0.13333, -0.00000], [ 3, 0.10667, 0.00000]], [ 0.01685, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.01685, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -1.53251, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -1.53097, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -1.53404, [ 3, -0.10667, 0.00027], [ 3, 0.50667, -0.00127]], [ -1.53558, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.18250, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.18250, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.18250, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.18250, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipYawPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.56907, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.56907, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.57061, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.57061, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RKneePitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 1.03396, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 1.03549, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ 1.03549, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 1.03549, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderPitch")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ 0.67193, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ 0.17952, [ 3, -0.13333, 0.34231], [ 3, 0.10667, -0.27385]], [ -1.17654, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ 0.83914, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderRoll")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -0.11356, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -0.49246, [ 3, -0.13333, 0.15028], [ 3, 0.10667, -0.12022]], [ -0.92504, [ 3, -0.10667, 0.00000], [ 3, 0.50667, 0.00000]], [ -0.19639, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RWristYaw")
	times.append([ 1.00000, 1.40000, 1.72000, 3.24000])
	keys.append([ [ -1.20423, [ 3, -0.33333, 0.00000], [ 3, 0.13333, 0.00000]], [ -1.20423, [ 3, -0.13333, 0.00000], [ 3, 0.10667, 0.00000]], [ -0.82840, [ 3, -0.10667, -0.00388], [ 3, 0.50667, 0.01841]], [ -0.80999, [ 3, -0.50667, 0.00000], [ 3, 0.00000, 0.00000]]])

	try:
	  motionProxy.angleInterpolationBezier(names, times, keys);
	except BaseException, err:
	  print err

	postureProxy.goToPosture("Sit", 1)  	


def loser_move():
 # Choregraphe bezier export in Python.
	names = list()
	times = list()
	keys = list()

	names.append("HeadPitch")
	times.append([ 1.00000])
	keys.append([ [ 0.51385, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("HeadYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.14424, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnklePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.92258, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LAnkleRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.02297, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.51231, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LElbowYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.00618, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHand")
	times.append([ 1.00000])
	keys.append([ [ 0.01680, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.55237, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.05527, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LHipYawPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.02314, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LKneePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.49391, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderPitch")
	times.append([ 1.00000])
	keys.append([ [ 0.48317, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LShoulderRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.26994, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("LWristYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.51700, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnklePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.92198, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RAnkleRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.00004, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowRoll")
	times.append([ 1.00000])
	keys.append([ [ 0.53694, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RElbowYaw")
	times.append([ 1.00000])
	keys.append([ [ -0.46791, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHand")
	times.append([ 1.00000])
	keys.append([ [ 0.01681, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.54785, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.13648, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RHipYawPitch")
	times.append([ 1.00000])
	keys.append([ [ -1.02314, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RKneePitch")
	times.append([ 1.00000])
	keys.append([ [ 0.40042, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderPitch")
	times.append([ 1.00000])
	keys.append([ [ 0.48172, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RShoulderRoll")
	times.append([ 1.00000])
	keys.append([ [ -0.09208, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	names.append("RWristYaw")
	times.append([ 1.00000])
	keys.append([ [ 0.13648, [ 3, -0.33333, 0.00000], [ 3, 0.00000, 0.00000]]])

	try:
		motionProxy.angleInterpolationBezier(names, times, keys);
	except BaseException, err:
		print err

	time.sleep(1)
	postureProxy.goToPosture("Sit", 1)  	
    
