import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# Create main window
root = tk.Tk()
root.title("Fake Video Detection")
root.geometry("1600x1600")
root.configure(bg="white")
# Create a frame for the graph
# frame = ttk.Frame(root)
# frame.pack(pady=20)

# Create Matplotlib figure with two subplots
image = Image.open("accuracy.png")  # Replace with the path to your image file
image = image.resize((500, 700), Image.LANCZOS)  # Resize the image to fit
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo, bg="white")
image_label.image = photo  # Keep a reference to the image
image_label.place(x=200, y=15)

image = Image.open("loss.png")  # Replace with the path to your image file
image = image.resize((500, 700), Image.LANCZOS)  # Resize the image to fit
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo, bg="white")
image_label.image = photo  # Keep a reference to the image
image_label.place(x=1000, y=15)

# Run the application
root.mainloop()
