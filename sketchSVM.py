from tkinter import *
from PIL import Image, ImageDraw
import numpy as np
import os
import sys
import pickle

# Load our model
with open("model/svm_model.pkl", 'rb') as file:
    loaded_model = pickle.load(file)

# The classes of images in our dataset
classes = ['The Eiffel Tower', 'The Great Wall of China', 'The Mona Lisa', 'aircraft carrier', 'airplane', 'alarm clock', 'ambulance', 'angel', 'animal migration', 'ant']

canvas_width = 500
canvas_height = 500

# https://www.semicolonworld.com/question/55284/how-can-i-convert-canvas-content-to-an-image
# These are used to draw the image to memory at the same time it is also drawn on the canvas
image = Image.new("L", (canvas_width, canvas_height), (255))
draw = ImageDraw.Draw(image)


# Do prediction on empty image once so that model is loaded and doesn't lag on first prediction
image_resized = image.resize(size=(28,28))
arr = np.array(image_resized)
arr2 = np.reshape(arr, (1,784))
arr2 = arr2 / 255
arr2 = np.ones((1,784)) - arr2

# Prediction
pred = loaded_model.predict(arr2)


def paint( event ):
    # Resize image in memory and save image to file (save to file only for debugging purposes)
    filename = "my_drawing.jpg"
    image_resized = image.resize(size=(28,28))
    image_resized.save(filename)

    # Create numpy array from image in memory
    arr = np.array(image_resized)
    arr2 = np.reshape(arr, (1, 784))
    arr2 = arr2 / 255
    arr2 = np.ones((1,784)) - arr2

    # Setup dot and dot location
    dot_size = 15
    x1, y1 = ( event.x - dot_size ), ( event.y - dot_size )
    x2, y2 = ( event.x + dot_size ), ( event.y + dot_size )
    # Draw to canvas
    canvas.create_oval( x1, y1, x2, y2, fill = '#000000' )
    # Draw to memory
    draw.ellipse( [x1, y1, x2, y2], fill = '#000000' )

    # Predict with loaded model and numpy array
    pred = loaded_model.predict_proba(arr2)

    # Display prediction result
    result = classes[np.argmax(pred)] + " (" + str(pred[0][np.argmax(pred)] * 100) + "%)"
    message.configure(text=result)

# Setup Canvas
master = Tk()
master.title( "CPSC599 Quickdraw" )
canvas = Canvas(master, 
           width=canvas_width, 
           height=canvas_height,
           background='#FFFFFF')
canvas.pack(expand = YES, fill = BOTH)
canvas.bind( "<B1-Motion>", paint )

message = Label( master, text = "Press and Drag the mouse to draw" )
message.pack( side = BOTTOM )


mainloop()