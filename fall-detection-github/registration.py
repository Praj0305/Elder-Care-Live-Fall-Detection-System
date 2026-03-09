import tkinter as tk
from tkinter import messagebox as ms
import sqlite3
from PIL import Image, ImageTk
import re
import random
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

window = tk.Tk()
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
window.geometry("%dx%d+0+0" % (w, h))
window.title("REGISTRATION FORM")
window.configure(background="#220a32")

Fullname = tk.StringVar()
address = tk.StringVar()
username = tk.StringVar()
Phoneno = tk.IntVar()
var = tk.IntVar()
age = tk.IntVar()
password = tk.StringVar()
password1 = tk.StringVar()

emails = []  # List to store multiple emails

# Database Setup
db = sqlite3.connect('evaluation.db')
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS admin_registration"
               "(Fullname TEXT, address TEXT, username TEXT, Email TEXT, Phoneno TEXT, Gender TEXT, age TEXT, password TEXT)")
db.commit()

def add_email():
    email = email_entry.get()
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if re.match(regex, email):
        if email not in emails:
            emails.append(email)
            email_listbox.insert(tk.END, email)
            email_entry.delete(0, tk.END)
        else:
            ms.showinfo("Duplicate Email", "This email is already added.")
    else:
        ms.showerror("Invalid Email", "Please enter a valid email.")

# def send_email(to_emails):
#     sender_email = "pragati.code@gmail.com"  # Change to your email
#     sender_password = "grqheqzoutabdfzd"  # Change to your password

#     subject = "Registration Successful"
#     body = "Thank you for registering! Your account has been successfully created."

#     for recipient in to_emails:
#         try:
#             msg = MIMEMultipart()
#             msg['From'] = sender_email
#             msg['To'] = recipient
#             msg['Subject'] = subject
#             msg.attach(MIMEText(body, 'plain'))

#             server = smtplib.SMTP("smtp.gmail.com", 587)
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, recipient, msg.as_string())
#             server.quit()
#         except Exception as e:
#             print(f"Failed to send email to {recipient}: {e}")

def insert():
    fname = Fullname.get()
    addr = address.get()
    un = username.get()
    mobile = Phoneno.get()
    gender = var.get()
    time = age.get()
    pwd = password.get()
    cnpwd = password1.get()
    email_str = ", ".join(emails)  # Store multiple emails as a string

    if not fname or fname.isdigit():
        ms.showerror("Error", "Please enter a valid name.")
    elif not addr:
        ms.showerror("Error", "Please enter an address.")
    elif not emails:
        ms.showerror("Error", "Please add at least one email.")
    elif len(str(mobile)) != 10:
        ms.showerror("Error", "Please enter a 10-digit phone number.")
    elif time > 100 or time == 0:
        ms.showerror("Error", "Please enter a valid age.")
    elif not pwd or pwd != cnpwd:
        ms.showerror("Error", "Passwords do not match.")
    else:
        conn = sqlite3.connect('evaluation.db')
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO admin_registration (Fullname, address, username, Email, Phoneno, Gender, age, password) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                (fname, addr, un, email_str, mobile, gender, time, pwd))

            conn.commit()
            conn.close()
            ms.showinfo('Success!', 'Account Created Successfully!')

            # Send confirmation email
            # send_email(emails)

            window.destroy()


fg_image = Image.open('img23.jpg')  # Replace with your second image
fg_image = fg_image.resize((500, 600), Image.LANCZOS)  # Adjust size as needed
foreground_image = ImageTk.PhotoImage(fg_image)

# Foreground label (position it over the background image)
foreground_label = tk.Label(window, image=foreground_image, borderwidth=0)
foreground_label.place(x=250, y=130) 
# UI Components
# image2 = Image.open('R2.jpg')
# image2 = image2.resize((700, 700), Image.ANTIALIAS)
# background_image = ImageTk.PhotoImage(image2)
# background_label = tk.Label(window, image=background_image)
# background_label.place(x=0, y=0)
canvas=tk.Canvas(window,background="#4c206a")
canvas.place(x=750,y=130,width=500,height=600)

l1 = tk.Label(canvas, text="Registration Form", font=("Times New Roman", 20, "bold"), bg="#4c206a", fg="white")
l1.place(x=130, y=10)

tk.Label(canvas, text="Full Name:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=60)
tk.Entry(canvas, textvar=Fullname, width=20, font=('', 15)).place(x=200, y=60)

tk.Label(canvas, text="Address:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=110)
tk.Entry(canvas, textvar=address, width=20, font=('', 15)).place(x=200, y=110)

tk.Label(canvas, text="E-mail:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=160)
email_entry = tk.Entry(canvas, width=20, font=('', 15))
email_entry.place(x=200, y=160)
tk.Button(canvas, text="Add", command=add_email, font=("Times New Roman", 12, "bold"), bg="#660033", fg="white").place(x=420, y=160)

email_listbox = tk.Listbox(canvas, width=40, height=3)
email_listbox.place(x=200, y=190)

tk.Label(canvas, text="Phone number:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=260)
tk.Entry(canvas, textvar=Phoneno, width=20, font=('', 15)).place(x=200, y=260)

tk.Label(canvas, text="Gender:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=310)
tk.Radiobutton(canvas, text="Male", variable=var, value=1, font=("bold", 15), bg="snow").place(x=200, y=310)
tk.Radiobutton(canvas, text="Female", variable=var, value=2, font=("bold", 15), bg="snow").place(x=330, y=310)

tk.Label(canvas, text="Age:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=360)
tk.Entry(canvas, textvar=age, width=20, font=('', 15)).place(x=200, y=360)

tk.Label(canvas, text="User Name:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=410)
tk.Entry(canvas, textvar=username, width=20, font=('', 15)).place(x=200, y=410)

tk.Label(canvas, text="Password:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=460)
tk.Entry(canvas, textvar=password, width=20, font=('', 15), show="*").place(x=200, y=460)

tk.Label(canvas, text="Confirm Password:", font=("Times New Roman", 15, "bold"), bg="#4c206a",fg="white").place(x=30, y=510)
tk.Entry(canvas, textvar=password1, width=20, font=('', 15), show="*").place(x=200, y=510)

tk.Button(canvas, text="Register", bg="#4c206a",fg="white", font=("", 20), width=7, command=insert).place(x=200, y=540)

window.mainloop()
