import cv2
from deepface import DeepFace
from playsound import playsound

races = {"asian": 0, "indian": 0, "black": 0, "white": 0, "middle eastern": 0, "latino hispanic": 0}
slurs = {"asian": "asian", "indian": "indian", "black": "black", "white": "white", "middle eastern": "middle_eastern", "latino hispanic": "latino"}
# Initialize the webcam
cap = cv2.VideoCapture(0)
actual_dominant = ""
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
                        actual_dominant = dominant_race
                        print(f"{actual_dominant} detected with confidence {race_confidence}")
                        
                        exit_flag = True
                        
              
                        #actual_slur = slurs[dominant_race]
                        
                
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

#Play the slur

slur = slurs[actual_dominant]
print(slur)
mp3_file = f"mp3sounds/{slur}.mp3"
playsound(mp3_file)
  

cap.release()
cv2.destroyAllWindows()
