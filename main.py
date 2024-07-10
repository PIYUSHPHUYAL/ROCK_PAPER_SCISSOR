import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import time, random


cap = cv2.VideoCapture(1)
cap.set(3,640)
cap.set(4,480)

detector = HandDetector(maxHands=1)

timer = 0
stateResult = False
startGame = False
scores = [0,0] #[AI,PLAYER]

while True:
    imageBackground = cv2.imread("images/background.png")
    success, img = cap.read()
    # flipped_img = cv2.flip(img, 1)  # 1 for horizontal flipping
    # imageScaled = cv2.resize(img,(0,0),None,0.655,0,655)
    imageScaled = cv2.resize(img, (289, 312), 
               interpolation = cv2.INTER_LINEAR)
    #find hands
    hands, img = detector.findHands(imageScaled)

    if startGame:

        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imageBackground, str(int(timer)), (674,74), cv2.FONT_HERSHEY_PLAIN, 5, (255,133,0),3)

        if timer>3:
            stateResult = True
            timer = 0

            if hands:
                playerMove = None
                hand = hands[0]
                fingers = detector.fingersUp(hand)
                if fingers == [0,0,0,0,0]:
                    playerMove = 1
                if fingers == [1,1,1,1,1]:
                    playerMove = 2  
                if fingers == [0,1,1,0,0]:
                    playerMove = 3

                randomNumber = random.randint(1,3)
                imageAI = cv2.imread(f"images/{randomNumber}.png",cv2.IMREAD_UNCHANGED)    
                imageBackground = cvzone.overlayPNG(imageBackground,imageAI,(49,155))

                # Player Wins
                if (playerMove == 1 and randomNumber == 3) or \
                            (playerMove == 2 and randomNumber == 1) or \
                            (playerMove == 3 and randomNumber == 2):
                        scores[1] += 1
 
                    # AI Wins
                if (playerMove == 3 and randomNumber == 1) or \
                            (playerMove == 1 and randomNumber == 2) or \
                            (playerMove == 2 and randomNumber == 3):
                        scores[0] += 1

                print(playerMove)   
                # print(fingers)

    imageBackground[155:154+313, 433:433+289] = imageScaled

    if stateResult:
        imageBackground = cvzone.overlayPNG(imageBackground, imageAI, (49,155))

    cv2.putText(imageBackground, str(scores[0]), (281,154), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0),3)
    cv2.putText(imageBackground, str(scores[1]), (666,153), cv2.FONT_HERSHEY_PLAIN, 5, (0,0,0),3)



    # cv2.imshow("Image", img)
    cv2.imshow("Background",imageBackground)
    # cv2.imshow("Scaled", imageScaled)
    key = cv2.waitKey(1)
    if key == ord('s'):
      startGame = True
      initialTime = time.time()
      stateResult = False
  