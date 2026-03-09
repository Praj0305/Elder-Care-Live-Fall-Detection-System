from tkinter import *
import tkinter as tk
from tkinter import ttk, LEFT, END, messagebox as ms
import time
import numpy as np
import cv2
import os
from PIL import Image, ImageTk
import sqlite3
import pandas as pd
from subprocess import call

##############################################
root = tk.Tk()
root.configure(background="seashell2")
root.title("Face Auth")

# Set full screen
w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

# Database connection
my_conn = sqlite3.connect('evaluation.db')

# ++++++++++++++++++++++++++++++++++++++++++++
# Background Image
image2 = Image.open('6.jpg')
image2 = image2.resize((w, h), Image.LANCZOS)
background_image = ImageTk.PhotoImage(image2)
background_label = tk.Label(root, image=background_image)
background_label.place(x=0, y=0)

# Title
lbl = tk.Label(root, text="Face Authentication Recognition",
               font=('times', 40, 'bold'), height=1, width=30,
               bg="black", fg="yellow")
lbl.place(x=330, y=5)

# Frame
frame_alpr = tk.LabelFrame(root, text=" --Process-- ",
                           width=280, height=400, bd=5,
                           font=('times', 15, 'bold'), bg="seashell4")
frame_alpr.place(x=70, y=130)


##############################################
def Create_database():
    face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)
    user_id = entry2.get()
    sampleN = 0

    if not os.path.exists("facesData"):
        os.makedirs("facesData")

    while True:
        ret, img = cap.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in faces:
            sampleN += 1
            cv2.imwrite(f"facesData/User.{str(user_id)}.{str(sampleN)}.jpg", gray[y:y+h, x:x+w])
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
            cv2.waitKey(100)

        cv2.imshow('Capturing Face Data', img)
        cv2.waitKey(1)
        if sampleN > 40:
            break

    cap.release()
    cv2.destroyAllWindows()
    entry2.delete(0, 'end')
    ms.showinfo("Success", "Face data created successfully!")


def update_label(msg):
    result_label = tk.Label(root, text=msg, width=40, font=("bold", 25),
                            bg='bisque2', fg='black')
    result_label.place(x=450, y=400)


def Train_database():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = "facesData"

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []

        for imagePath in imagePaths:
            filename = os.path.split(imagePath)[-1]
            parts = filename.split(".")

            # Only process if file name looks like User.ID.sample.jpg
            if len(parts) >= 3 and parts[1].isdigit():
                ID = int(parts[1])
                facesImg = Image.open(imagePath).convert('L')
                faceNP = np.array(facesImg, 'uint8')
                faces.append(faceNP)
                IDs.append(ID)
                cv2.imshow("Training Face", faceNP)
                cv2.waitKey(10)
            else:
                print(f"[WARNING] Skipped invalid file: {filename}")

        return np.array(IDs), faces

    # Get images and their IDs
    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    recognizer.save("trainingData.yml")
    cv2.destroyAllWindows()
    print("[INFO] Training completed successfully.")



def Test_database():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('trainingdata.yml')

    cascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)

    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.3, 8, minSize=(int(minW), int(minH)))

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])

            if confidence < 50:
                confidence_txt = f"  {round(100 - confidence)}%"
                cv2.putText(img, f"ID: {id}", (x+5, y-5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, confidence_txt, (x+5, y+h-5), font, 1, (255, 255, 0), 1)
                update_label('Authenticated User Detected')

                with sqlite3.connect('evaluation.db') as db:
                    c = db.cursor()
                    c.execute('SELECT * FROM admin_registration WHERE id=?', (id,))
                    result = c.fetchall()
                    if result:
                        for row in result:
                            print(f"Authenticated: Name={row[1]}, LastName={row[2]}")
                cam.release()
                cv2.destroyAllWindows()
                return
            else:
                id_txt = "Unknown Person"
                confidence_txt = f"  {round(100 - confidence)}%"
                cv2.putText(img, id_txt, (x+5, y-5), font, 1, (255, 255, 255), 2)
                cv2.putText(img, confidence_txt, (x+5, y+h-5), font, 1, (255, 255, 0), 1)
                update_label(' Unauthenticated User Detected!')

                # Save unauthenticated image
                cv2.imwrite("unauth_user.jpg", img[y:y+h, x:x+w])
                print("[INFO] Saved unauthenticated image as unauth_user.jpg")

                # Send mail alert
                try:
                    call(["python", "mail.py"])
                    print("[INFO] Email sent successfully.")
                    
                except Exception as e:
                    print(f"[ERROR] Email failed: {e}")

                cam.release()
                cv2.destroyAllWindows()
                ms.showwarning("Alert", "Unauthenticated person detected! Email sent.")
                return

        cv2.imshow('Camera', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cam.release()
    cv2.destroyAllWindows()


def registration():
    call(["python", "registration.py"])


def display():
    call(["python", "display.py"])


def ID():
    framed = tk.LabelFrame(root, text=" --WELCOME-- ", width=600,
                           height=50, bd=5, font=('times', 14, 'bold'),
                           bg="pink")
    framed.place(x=500, y=100)
    r_set = my_conn.execute("SELECT * FROM admin_registration")
    i = 0
    for student in r_set:
        for j in range(len(student)):
            e = tk.Entry(framed, width=15, fg='blue')
            e.grid(row=i, column=j)
            e.insert(END, student[j])
        i += 1


def window():
    root.destroy()


##############################################
# Buttons

button1 = tk.Button(frame_alpr, text="Registration Of User", bd=5,
                    command=registration, width=20, height=1,
                    font=('times', 15, 'bold'),
                    bg="purple", fg="white")
button1.place(x=10, y=20)

button3 = tk.Button(frame_alpr, text="Display", bd=5,
                    command=ID, width=20, height=1,
                    font=('times', 15, 'bold'),
                    bg="purple", fg="white")
button3.place(x=10, y=80)

button1 = tk.Button(frame_alpr, text="Create Face Data", bd=5,
                    command=Create_database, width=15, height=1,
                    font=('times', 15, 'bold'),
                    bg="purple", fg="white")
button1.place(x=10, y=140)

button2 = tk.Button(frame_alpr, text="Train Face Data", bd=5,
                    command=Train_database, width=20, height=1,
                    font=('times', 15, 'bold'),
                    bg="purple", fg="white")
button2.place(x=10, y=200)

button3 = tk.Button(frame_alpr, text="Face Authentication", bd=5,
                    command=Test_database, width=20, height=1,
                    font=('times', 15, 'bold'),
                    bg="purple", fg="white")
button3.place(x=10, y=260)

entry2 = tk.Entry(frame_alpr, bd=5, width=7)
entry2.place(x=210, y=150)

exit_btn = tk.Button(frame_alpr, text="Exit", bd=5,
                     command=window, width=20, height=1,
                     font=('times', 15, 'bold'),
                     bg="red", fg="white")
exit_btn.place(x=10, y=320)

root.mainloop()
