import cv2
import numpy as np
import tkinter as tk
from PIL import Image, ImageTk

# Global variables for overlay images
glasses_img = cv2.imread('beginner cv programs\glasses3.png', cv2.IMREAD_UNCHANGED)
moustache_img = cv2.imread('gui in python\Moustache.png', cv2.IMREAD_UNCHANGED)

# Create a VideoCapture object
cap = cv2.VideoCapture(0)

# Flags to toggle overlays
show_glasses = False
show_moustache = False

# Offset values for overlays
glasses_offset = (0, 0)  # Unique offset for glasses
moustache_offset = (0, -0.4)  # Unique offset for moustache

# Size values for overlay images
glasses_size = (1, 1)  # Size of glasses overlay (as a ratio of face width and height)
moustache_size = (1, 0.8)  # Size of moustache overlay (as a ratio of face width and height)

def apply_filter():
    ret, frame = cap.read()
    if not ret:
        return

    if show_glasses:
        overlay_img = glasses_img
        apply_overlay(frame, overlay_img, glasses_offset, glasses_size)

    if show_moustache:
        overlay_img = moustache_img
        apply_overlay(frame, overlay_img, moustache_offset, moustache_size)

    # Display the resulting frame
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    panel.imgtk = imgtk
    panel.config(image=imgtk)

    # Schedule the next iteration
    root.after(10, apply_filter)

def apply_overlay(frame, overlay_img, offset, size):
    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Load the face cascade file
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

    for (x, y, w, h) in faces:
        # Calculate the position to overlay the image
        x_offset = x-int(offset[0] * w)
        y_offset = y-int(offset[1] * h)

        # Resize the overlay image to fit the face
        overlay_width = int(size[0] * w)
        overlay_height = int(size[1] * h)
        overlay_resized = cv2.resize(overlay_img, (overlay_width, overlay_height))

        # Overlay the image on the face
        for c in range(0, 3):
            frame[y_offset:y_offset+overlay_height, x_offset:x_offset+overlay_width, c] = \
                overlay_resized[:, :, c] * (overlay_resized[:, :, 3] / 255.0) + \
                frame[y_offset:y_offset+overlay_height, x_offset:x_offset+overlay_width, c] * \
                (1.0 - overlay_resized[:, :, 3] / 255.0)

def toggle_glasses():
    global show_glasses, show_moustache
    show_glasses = not show_glasses
    if show_glasses:
        show_moustache = False

def toggle_moustache():
    global show_glasses, show_moustache
    show_moustache = not show_moustache
    if show_moustache:
        show_glasses = False

def turn_off_all():
    global show_glasses, show_moustache
    show_glasses = False
    show_moustache = False

# Create Tkinter application window
root = tk.Tk()
root.title("CV Filter Demo")

# Create a panel to display the image
panel = tk.Label(root)
panel.pack()

# Create buttons to toggle overlays
button_toggle_glasses = tk.Button(root, text="Toggle Glasses", command=toggle_glasses)
button_toggle_glasses.pack()

button_toggle_moustache = tk.Button(root, text="Toggle Moustache", command=toggle_moustache)
button_toggle_moustache.pack()

button_turn_off_all = tk.Button(root, text="Turn Off All", command=turn_off_all)
button_turn_off_all.pack()

# Start applying the filter
apply_filter()

# Start the application
root.mainloop()

# Release the capture
cap.release()
cv2.destroyAllWindows()
