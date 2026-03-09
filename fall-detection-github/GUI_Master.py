
import mediapipe as mp # Import mediapipe
import cv2 # Import opencv
import pandas as pd
import numpy as np
import os
import playsound
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline 
from sklearn.preprocessing import StandardScaler 
from sklearn.linear_model import LogisticRegression, RidgeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.metrics import accuracy_score # Accuracy metrics 
import pickle
import requests
import time

mp_drawing = mp.solutions.drawing_utils # Drawing helpers
mp_holistic = mp.solutions.holistic # Mediapipe Solutions

with open('body_language_rf.pkl', 'rb') as f:
    model = pickle.load(f)
print(model)




import smtplib
from email.message import EmailMessage
import imghdr
import sqlite3

def mail():
    # Read the ID from the file
    with open("id.txt", "r") as f:
        user_id = f.read().strip()  # Remove extra whitespace/newlines
    
    try:
        user_id = int(user_id)  # Ensure ID is an integer
    except ValueError:
        print("Error: ID in id.txt is not a valid integer.")
        return
    
    # Database Connection
    db_path = "evaluation.db"  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch Email
    query = "SELECT Email FROM admin_registration WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()  # Fetch single record

    conn.close()  # Close DB connection

    if result:
        reciever_email = result[0]  # Extract email from tuple
        print("Email:", reciever_email)
    else:
        print(f"No email found for ID: {user_id}")
        return
    
    # Email Configuration
    sender_email = "pragati.code@gmail.com"
    password = "grqheqzoutabdfzd"  # Use an App Password for better security

    new_message = EmailMessage()
    new_message['Subject'] = "Fall Detected - Immediate Assistance Required"
    new_message['From'] = sender_email
    new_message['To'] = reciever_email
    new_message.set_content("Alert: A fall has been detected. Please respond promptly.")

    # Attach Image
    try:
        with open('abc.png', 'rb') as f:
            image_data = f.read()
            image_type = imghdr.what(f.name)
            image_name = f.name

        new_message.add_attachment(image_data, maintype='image', subtype=image_type, filename=image_name)
    except FileNotFoundError:
        print("Error: Image 'abc.png' not found. Email will be sent without an image.")

    # Send Email
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, password)              
            smtp.send_message(new_message)
        print("Email sent successfully!")
    except smtplib.SMTPAuthenticationError:
        print("Error: Authentication failed. Check your email/password settings.")
    except smtplib.SMTPException as e:
        print(f"SMTP error occurred: {e}")
   
        



    
import requests
import sqlite3
def send_sms():
    
    # Read the ID from the file
    with open("id.txt", "r") as f:
        user_id = f.read().strip()  # Remove extra whitespace/newlines

    try:
        user_id = int(user_id)  # Ensure ID is an integer
    except ValueError:
        print("Error: ID in id.txt is not a valid integer.")
        

    # Database Connection
    db_path = "evaluation.db"  
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Fetch Email
    query = "SELECT Phoneno FROM admin_registration WHERE id = ?"
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()  # Fetch single record

    conn.close()  # Close DB connection

    if result:
        mobile = result[0]  # Extract email from tuple
        print("Mobile Number:", mobile)
    else:
        print(f"No Mobile Number found for ID: {user_id}")
    
    """
    Send an SMS alert to multiple numbers using Fast2SMS API.
    """
    message = "Fall Detected. Immediate assistance required."
    url = "https://www.fast2sms.com/dev/bulkV2"
    params = {
        "authorization": "8aNhrEMk0Tzn3ScP9lt1si4pmXJRG7AyVHq2DBUgWjZveFLuOYZtDBEQRsveoAbVwNq9H1Cc28npYhrP",  # Replace with your actual API key
        "sender_id": "TXTIND",
        "message": message,
        "language": "english",
        "route": "q",
        "numbers": str(mobile) # Comma-separated list of numbers
    }

    try:
        # Send a GET request to Fast2SMS API
        response = requests.get(url, params=params)

        # Print detailed response
        print("Response Status Code:", response.status_code)
        print("Response Text:", response.text)

        # Check response status
        if response.status_code == 200:
            print("SMS sent successfully.")
        else:
            print("Failed to send SMS. Check the response for details.")
    except requests.exceptions.RequestException as e:
        print("Error sending SMS:", str(e))
#send_sms()




cap = cv2.VideoCapture(0)
# Initiate holistic model
with mp_holistic.Holistic(min_detection_confidence=0.5, min_tracking_confidence=0.5) as holistic:
    
    while cap.isOpened():
        ret, frame = cap.read()
        
        # Recolor Feed
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False        
        
        # Make Detections
        results = holistic.process(image)
        # print(results.face_landmarks)
        
        # face_landmarks, pose_landmarks, left_hand_landmarks, right_hand_landmarks
        
        # Recolor image back to BGR for rendering
        image.flags.writeable = True   
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        # 1. Draw face landmarks
        mp_drawing.draw_landmarks(image, results.face_landmarks, mp_holistic.FACEMESH_CONTOURS, 
                                 mp_drawing.DrawingSpec(color=(80,110,10), thickness=1, circle_radius=1),
                                 mp_drawing.DrawingSpec(color=(80,256,121), thickness=1, circle_radius=1)
                                 )
        
        # 2. Right hand
        mp_drawing.draw_landmarks(image, results.right_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(80,22,10), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(80,44,121), thickness=2, circle_radius=2)
                                 )
        # 3. Left Hand
        mp_drawing.draw_landmarks(image, results.left_hand_landmarks, mp_holistic.HAND_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(121,22,76), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(121,44,250), thickness=2, circle_radius=2)
                                 )

        # 4. Pose Detections
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_holistic.POSE_CONNECTIONS, 
                                 mp_drawing.DrawingSpec(color=(245,117,66), thickness=2, circle_radius=4),
                                 mp_drawing.DrawingSpec(color=(245,66,230), thickness=2, circle_radius=2)
                                 )
        # Export coordinates
        try:
            # Extract Pose landmarks
            pose = results.pose_landmarks.landmark
            pose_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in pose]).flatten())
            
            # Extract Face landmarks
            face = results.face_landmarks.landmark
            face_row = list(np.array([[landmark.x, landmark.y, landmark.z, landmark.visibility] for landmark in face]).flatten())
            
            # Concate rows
            row = pose_row+face_row
            
#             # Append class name 
#             row.insert(0, class_name)
            
#             # Export to CSV
#             with open('coords.csv', mode='a', newline='') as f:
#                 csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
#                 csv_writer.writerow(row) 

            # Make Detections
            X = pd.DataFrame([row])
            body_language_class = model.predict(X)[0]
            body_language_prob = model.predict_proba(X)[0]
            print(body_language_class, body_language_prob)
            # Grab ear coords
            coords = tuple(np.multiply(
                            np.array(
                                (results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].x, 
                                 results.pose_landmarks.landmark[mp_holistic.PoseLandmark.LEFT_EAR].y))
                        , [640,480]).astype(int))
            
            cv2.rectangle(image, 
                          (coords[0], coords[1]+5), 
                          (coords[0]+len(body_language_class)*20, coords[1]-30), 
                          (245, 117, 16), -1)
            cv2.putText(image, body_language_class, coords, 
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            # Get status box
            cv2.rectangle(image, (0,0), (250, 60), (245, 117, 16), -1)
            
            # Display Class
            cv2.putText(image, 'CLASS'
                        , (95,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
            cv2.putText(image, body_language_class.split(' ')[0]
                        , (90,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            # data=body_language_class
            # TTS=gTTS(body_language_class)
            # TTS.save("voice.mp3")
  
        
  
            if(body_language_class =="fall"):
                #color = red
                cv2.imwrite('abc.png',frame)
                mail()
                print("mail send")
                # time.sleep(10)
                # # Call the function
                # send_sms()
                
                
            # Display Probability
                cv2.putText(image, 'PROB'
                            , (15,12), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(round(body_language_prob[np.argmax(body_language_prob)],2))
                            , (10,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
               
                # from subprocess import call
                # call(["python","sendmail.py"])
            
        except:
            pass
                        
        cv2.imshow('Raw Webcam Feed', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
cap.release()
cv2.destroyAllWindows()