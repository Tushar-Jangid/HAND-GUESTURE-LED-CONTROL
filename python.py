import cv2
import mediapipe as np
import serial
import time

arduino = serial.Serial(port ='COM3',baudrate=9600,timeout=1)
time.sleep(2)

mp_hands = mp.solution.hands
hands = mp_hand.Hands()
mp_drowing = mp.solution.drowing_untils

def detect_figures(image,hand_landmarks):
    fingure_tipes = [8,12,16,20]
    thumb_tip = 4
    fingure_states = [0,0,0,0]

    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        fingure_states[0] = 1

    for idx, tip in enumerate(fingure_tipes):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            fingure_states[idx + 1] = 1

    return fingure_states

cap = cv2,VideoCapture(0)

while cap.isOpened():
    success,image = cap.read()
    if not success:
        break

    image = cv2.cvtColor(cv2.filp(image,1),cv2.COLOR_BGR2RGB)
    result = hands.process(image)
    image = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drowing.draw_landmarks(image,hand_landmarks,mp_hands.HAND_CONNECTIONS)
            fingure_states = detect_figures(image,hand_landmarks)
            arduino.write(str(fingure_states).encode())
            print(f"Figure states: {fingure_states}")

    cv2.imshow('Hand Tracking',image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
arduino.close()