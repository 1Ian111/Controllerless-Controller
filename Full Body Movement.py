import cv2
import sys
import mediapipe as mp
import time
from pynput.keyboard import Key, Controller
import Out_of_Bounds
import subprocess
keyboard = Controller()
jumping = False
OOB = Out_of_Bounds.OutOfBoundsWindow()
crouchingDown = False
lookingUp = False
correctPosition = True
oldPosition = False
rightPressed = False
leftPressed = False
shiftPressed = False
lshiftPressed = False
rshiftPressed = False
startPressed = True
lFootPressed = False
rFootPressed = False
footPressStartTime = 0
startTime = 0
leftTime = 0
rightTime = 0
jumpTime = 0
prevFootL = 0
prevFootR = 0
prevKnuckleR = 100
currentMessage = ""
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap.set(cv2.CAP_PROP_FPS, 30)

mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(static_image_mode=False, model_complexity=0)

def checkPosition():
    global currentMessage, correctPosition, oldPosition
    oldPosition = correctPosition
    correctPosition = True
    if(abs(lshoulderx - rshoulderx) > .15):
        if(currentMessage == "Too Close"):
            pass
        else:
            print("Too Close")
        currentMessage = "Too Close"
        correctPosition = False
    if(lshoulderx >= .95):
        if(currentMessage == "Too Far Left"):
            pass
        else:
            print("Too Far Left")
        currentMessage = "Too Far Left"
        correctPosition = False
    if(rshoulderx <= .05):
        if(currentMessage == "Too Far Right"):
            pass
        else:
            print("Too Far Right")
        currentMessage = "Too Far Right"
        correctPosition = False
    if correctPosition == True:
        if(currentMessage == "Just Right!"):
            pass
        else:
            print("Just Right!")
        currentMessage = "Just Right!"
    return correctPosition
def toggleMenu():
    if(abs(lelbowx - relbowx) <= .05 and abs(lelbowy - relbowy) <= .04 and abs(lwristy - rwristy) <= .1 and abs(lwristx - rwristx) >= .05 and abs(lelbowx - nosex) <=.2 and abs(relbowx - nosex) <=.2):
        if(-.1 < (lwristy - lelbowy) < -.05 and -.1 < (lwristy - relbowy) < -.05):
            if(-.1 < (rwristy - lelbowy) < -.05 and -.1 < (rwristy - relbowy) < -.05):
                subprocess.Popen(["python", r"C:\Users\smith\Downloads\New folder\GUI_EXPO2.py"])
                sys.exit()

def jump():
    global prevFootL, prevFootR, jumping, jumpTime
    
    if not jumping and (lfootindy - prevFootL) >= 0.015 and (rfootindy - prevFootR) >= 0.015:
        keyboard.press(' ')
        jumping = True
        jumpTime = time.time()

    # Release after .6 seconds
    if jumping and (time.time() - jumpTime >= .6):
        keyboard.release(' ')
        jumping = False
    prevFootL = lfootindy
    prevFootR = rfootindy

#def actionButton():
    global shiftPressed
    if(abs(rwristx - relbowx) <= 0.08 and abs(relbowx - rshoulderx) <= 0.08 and abs(rwristy - relbowy) <= 0.08 and abs(relbowy - rshouldery) <= 0.08):
        if not shiftPressed:
            keyboard.press(Key.shift)
            shiftPressed = True
    else:
        if shiftPressed:
            keyboard.release(Key.shift)
            shiftPressed = False
def actionButton():
    global shiftPressed
    if(abs(rwristx - relbowx) <= 0.08 and abs(relbowx - rshoulderx) <= 0.08 and abs(rwristy - relbowy) <= 0.08 and abs(relbowy - rshouldery) <= 0.08):
        if rwristz < relbowz - 0.15 and rwristz < rshoulderz - 0.15:
            if not shiftPressed:
                keyboard.press(Key.shift)
                shiftPressed = True
    else:
        if shiftPressed:
            keyboard.release(Key.shift)
            shiftPressed = False
def right():
    global rightPressed, rFootPressed, rshiftPressed, rightTime, footPressStartTime
    current_time = time.time()

    if rhipx <= 0.35:
        if rFootPressed:
            keyboard.release('d')
            rFootPressed = False

        if not rightPressed:
            keyboard.press('d')
            rightPressed = True
    else:
        if rightPressed and not rFootPressed:
            keyboard.release('d')
            rightPressed = False

        if rfootindx <= 0.35:
            if not rFootPressed and (current_time - rightTime >= 1.0):
                keyboard.press('d')
                footPressStartTime = current_time
                rFootPressed = True
                rightTime = current_time

        if rFootPressed and (current_time - footPressStartTime >= 0.1):
            keyboard.release('d')
            rFootPressed = False

    if rhipx <= 0.25:
        if not rshiftPressed:
            keyboard.press(Key.shift)
            rshiftPressed = True
    elif rshiftPressed:
        keyboard.release(Key.shift)
        rshiftPressed = False

def left():
    global leftPressed, lFootPressed, lshiftPressed, leftTime, footPressStartTime
    current_time = time.time()

    if lhipx >= 0.65:
        if lFootPressed:
            keyboard.release('a')
            lFootPressed = False

        if not leftPressed:
            keyboard.press('a')
            leftPressed = True
    elif lfootindx >= 0.65:
        if not lFootPressed and (current_time - leftTime >= 1.0):
            keyboard.press('a')
            footPressStartTime = current_time
            lFootPressed = True
            leftTime = current_time

        if lFootPressed and (current_time - footPressStartTime >= 0.1):
            keyboard.release('a')
            lFootPressed = False
    else:
        if leftPressed and not lFootPressed:
            keyboard.release('a')
            leftPressed = False

    if lhipx >= 0.75:
        if not lshiftPressed:
            keyboard.press(Key.shift)
            lshiftPressed = True
    else:
        if lshiftPressed:
            keyboard.release(Key.shift)
            lshiftPressed = False
def down():
    global crouchingDown
    if nosey >= .3:
        if not crouchingDown:
            keyboard.press('s')
            crouchingDown = True
    else:
        if crouchingDown:
            keyboard.release('s')  
            crouchingDown = False
def up():
    global lookingUp
    if(lindexy <= leyeiny and rindexy <= leyeiny):
        if not lookingUp:
            keyboard.press('w')
            lookingUp = True
    else:
        if lookingUp:
            keyboard.release('w')
            lookingUp = False

def start(): 
    global startPressed, startTime
    if(abs(lindexy - rindexy) <= .1 and abs(lwristy - rwristy) <= .1 and abs(rwristx - lwristx) > .4):
        if startPressed == False and (time.time() - startTime) >= 0.5:
            keyboard.press(Key.enter)
            startPressed = True
            startTime = time.time()
    else:
        if startPressed:
            keyboard.release(Key.enter)
            startPressed = False

while True:
    ret, frame = cap.read()
    cv2.imshow("Hand Gesture", frame)
    if not ret:
        break

    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = pose.process(image_rgb)

    if results.pose_landmarks:
        mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

        nosex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].x
        leyeinx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].x
        leyex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE].x
        leyeoutx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_OUTER].x
        reyeinx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE_INNER].x
        reyex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].x
        reyeoutx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_OUTER].x
        learx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].x
        rearx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].x
        lmouthx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].x
        rmouthx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].x
        lshoulderx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].x
        rshoulderx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].x
        lelbowx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].x
        relbowx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].x
        lwristx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].x
        rwristx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].x
        lpinkyx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].x
        rpinkyx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].x
        lindexx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].x
        rindexx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].x
        lthumbx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_THUMB].x
        rthumbx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].x
        lhipx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].x
        rhipx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].x
        lkneex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].x
        rkneex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].x
        lanklex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].x
        ranklex = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].x
        lheelx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].x
        rheelx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].x
        lfootindx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].x
        rfootindx = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].x

        nosey = results.pose_landmarks.landmark[mp_pose.PoseLandmark.NOSE].y
        leyeiny = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_INNER].y
        leyey = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE].y
        leyeouty = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_OUTER].y
        reyeiny = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE_INNER].y
        reyey = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EYE].y
        reyeouty = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EYE_OUTER].y
        leary = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_EAR].y
        reary = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_EAR].y
        lmouthy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_LEFT].y
        rmouthy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.MOUTH_RIGHT].y
        lshouldery = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].y
        rshouldery = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].y
        lelbowy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].y
        relbowy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].y
        lwristy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].y
        rwristy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].y
        lpinkyy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].y
        rpinkyy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].y
        lindexy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].y
        rindexy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].y
        lthumby = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_THUMB].y
        rthumby = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_THUMB].y
        lhipy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP].y
        rhipy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP].y
        lkneey = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE].y
        rkneey = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE].y
        lankley = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE].y
        rankley = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE].y
        lheely = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HEEL].y
        rheely = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HEEL].y
        lfootindy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_FOOT_INDEX].y
        rfootindy = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_FOOT_INDEX].y

        rindexz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_INDEX].z
        lindexz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_INDEX].z
        rpinkyz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_PINKY].z
        lpinkyz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_PINKY].z
        lwristz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST].z
        rwristz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST].z
        lelbowz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW].z
        relbowz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW].z
        lshoulderz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER].z
        rshoulderz = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER].z
        



        #hugging left wrist -.03, right writst -.01
        #X left wrist -.09, right wrist -.085
        #if checkPosition():
            #print("left wrist elbow " + str(lwristy - lelbowy))
            #print("right wrist elbow " + str(rwristy - lelbowy))
        #Left High Right Low
        toggleMenu()
        if checkPosition() == True:
            if(oldPosition == False):
                OOB.hide()
            jump()
            actionButton()
            right()
            left()
            down()
            up()
            start()
        else:
            OOB.show()
                 
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break


cap.release()
cv2.destroyAllWindows() 