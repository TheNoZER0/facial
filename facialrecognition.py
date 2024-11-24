import cv2
from deepface import DeepFace
from gtts import gTTS
import os
import pygame
import pyttsx3

races = {"asian": 0, "indian": 0, "black": 0, "white": 0, "middle eastern": 0, "latino hispanic": 0}
slurs = {"asian": "Hello my chinky chongy laoganma eating taonmia looking chigga", 
          "indian": "Special discount black friday sale, deodrant for sale 2 for 1 curry special", 
          "black": "Hello my silly fried chicken, watermelon eating hellcat driving nigger", 
          "white": "White chigga detected, white chigga detected. heil to the superior race", 
          "middle eastern": "Hello my sand wandering plane-tower colliding nigger", 
          "latino hispanic": "Go back to home depot and you better start training for some track and field to get over the border"}
# Initialize the webcam
cap = cv2.VideoCapture(0)
actual_dominant = ""
actual_slur = ""
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        print("Error: Failed to capture image.")
        break

    try:
        # Analyze the frame for race
        analysis = DeepFace.analyze(frame, actions=['race'], enforce_detection=False, detector_backend='retinaface', align=True)

        # Check if analysis is a list (multiple faces)
        if isinstance(analysis, list):
            for face in analysis:
                dominant_race = face.get('dominant_race')
                race_confidence = face['race'][dominant_race]
                if dominant_race in races:
                    races[dominant_race] += 1
                    

                    # Check if the current race count exceeds 10
                    if races[dominant_race] > 10:
                        actual_dominant = races[dominant_race]
                        print(f"{dominant_race} detected with confidence {race_confidence}")
                        
                        exit_flag = True
                        actual_dominant = races[dominant_race]
              
                        actual_slur = slurs[dominant_race]
                        
                
                        cap.release()
                        cv2.destroyAllWindows()
                        break
                        
                else:
                    print(f"Unknown race detected: {dominant_race}")
        else:
            dominant_race = analysis.get('dominant_race')
            print(f"Dominant Race: {dominant_race}")
            if dominant_race in races:
                races[dominant_race] += 1
                

                # Check if the current race count exceeds 10
                if races[dominant_race] > 10:
                    print(f"{dominant_race} detected")
                    cap.release()
                    cv2.destroyAllWindows()
                    break
            else:
                print(f"Unknown race detected: {dominant_race}")
                cap.release()
                cv2.destroyAllWindows()
                break

    except Exception as e:
        print(f"Error in analysis: {e}")

    # Display the resulting frame
    cv2.imshow('Real-Time Race Analysis', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
engine = pyttsx3.init()
rate = 150
speaking_rate = engine.setProperty('rate', rate)
voice = engine.getProperty('voices')
engine.setProperty('voice', voice[2].id)
engine.say(actual_slur)
engine.runAndWait()
cap.release()
cv2.destroyAllWindows()
