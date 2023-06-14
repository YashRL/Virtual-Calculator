# Virtual Calculator by Yash Rawal
import cv2
from cvzone.HandTrackingModule import HandDetector
import time
class Button:
    def __init__(self, pos, width, height, value):
        self.pos = pos
        self.width = width
        self.height = height
        self.value = value

    def draw(self, img):
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (225, 225, 225), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0] + 40, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)

    def checkClick(self, x, y):
        if self.pos[0]<x<self.pos[0] + self.width and self.pos[1]<y<self.pos[1] + self.height:
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (255, 255, 255), cv2.FILLED)
            cv2.rectangle(img, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (50, 50, 50), 3)
            cv2.putText(img, self.value, (self.pos[0] + 20, self.pos[1] + 60), cv2.FONT_HERSHEY_PLAIN, 3, (0, 0, 0), 3)
            return True
        else:
            return False



# Camera
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)
detector = HandDetector(detectionCon=0.8, maxHands=1)


#Creating Buttons
buttonListValues = [['7','8','9','*'],
                    ['4','5','6','-'],
                    ['1','2','3','+'],
                    ['0','/','.','=']]

buttonList = []

for x in range(4):
    for y in range(4):
        xpos = x*70 + 70
        ypos = y*70 + 150
        buttonList.append(Button((xpos,ypos),70,70, buttonListValues[y][x]))

# Variables
myEquation = ''

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)

    # Detection of Hand
    hands, img = detector.findHands(img, flipType=False)

    # Draw all Buttons
    cv2.rectangle(img, (70,70), (70 + 280, 70 + 70), (225, 225, 225), cv2.FILLED)
    cv2.rectangle(img, (70,70), (70 + 280, 70 + 70), (50, 50, 50), 3)


    for button in buttonList:
        button.draw(img)

    # Check for Hand
    if hands:
        lmList = hands[0]['lmList']
        length, _, img = detector.findDistance(lmList[8][:2], lmList[12][:2], img) #The cvzone is updated so know we have to give 3 dimentional values

        #print(length)                                                              #just add [:2] to lmList to make it work
        x, y = lmList[8][:2]
        if length<40:
            for i,button in enumerate(buttonList):
               if button.checkClick(x,y):
                   myValue = buttonListValues[int(i%4)][int(i/4)]
                   if myValue == "=":
                       myEquation = str(eval(myEquation))
                   else:
                       myEquation += myValue
               time.sleep(0.01)

    # To avoid Duplications

    # Display Result
    cv2.putText(img, myEquation, (80 , 120), cv2.FONT_HERSHEY_PLAIN, 3, (50, 50, 50), 3)

    cv2.imshow("Image", img)
    cv2.waitKey(1)