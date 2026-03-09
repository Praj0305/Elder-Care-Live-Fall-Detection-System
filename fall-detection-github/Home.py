import tkinter as tk
from tkinter import ttk, LEFT, END
from PIL import Image, ImageTk
from tkinter.filedialog import askopenfilename
from tkinter import messagebox as ms
import cv2
import sqlite3
import os
import numpy as np
import time

global fn
fn = ""
##############################################+=============================================================
root = tk.Tk()
root.configure(background="brown")
# root.geometry("1300x700")


w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))
root.title("Human Action Recognition Using Machine Learning")

# 43

# ++++++++++++++++++++++++++++++++++++++++++++
#####For background Image
  # , relwidth=1, relheight=1)


image2 = Image.open('f3.jpg')
image2 = image2.resize((w,h), Image.LANCZOS)

background_image = ImageTk.PhotoImage(image2)

background_label = tk.Label(root, image=background_image)

background_label.image = background_image

background_label.place(x=0, y=0)  # , relwidth=1, relheight=1)






# img=ImageTk.PhotoImage(Image.open("a1.jpg"))

# img2=ImageTk.PhotoImage(Image.open("s2.jpg"))

# img3=ImageTk.PhotoImage(Image.open("s3.jpg"))


# logo_label=tk.Label()
# logo_label.place(x=0,y=100)

# x = 1

# # function to change to next image
# def move():
# 	global x
# 	if x == 4:
# 		x = 1
# 	if x == 1:
# 		logo_label.config(image=img)
# 	elif x == 2:
# 		logo_label.config(image=img2)
# 	elif x == 3:
# 		logo_label.config(image=img3)
# 	x = x+1
# 	root.after(2000, move)

# # calling the function
# move()
#
label_l1 = tk.Label(root, text="Fall Detection Using Machine Learning",font=("Times New Roman", 35, 'bold'),
                    background="#152238", fg="white", width=60, height=2)
label_l1.place(x=0, y=0)



################################$%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

def action():
   
    from subprocess import call
    call(["python","GUI_Master.py"])
    
def action():
   
    from subprocess import call
    call(["python","Face_Auth.py"])
#################################################################################################################
def window():
    root.destroy()



button3 = tk.Button(root, text="Fall Detection",command=action, width=20, height=1, bg="#152238", fg="white",font=('times', 20, ' bold '), bd=5, relief="ridge")
button3.place(x=100, y=150)


button3 = tk.Button(root, text="Face Auth",command=action, width=20, height=1, bg="#152238", fg="white",font=('times', 20, ' bold '), bd=5, relief="ridge")
button3.place(x=100, y=250)

exit = tk.Button(root, text="Exit", command=window, width=20, height=1, font=('times', 20, ' bold '), bg="red",fg="white", bd=5, relief="ridge")
exit.place(x=100, y=350)

root.mainloop()