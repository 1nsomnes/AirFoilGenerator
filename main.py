import tkinter as tk
from tkinter import filedialog

import scriptGenerator as sg

datFilePath = "Files/dat_files/naca4424-80.txt"

window = tk.Tk(screenName="Airfoil Generator", baseName="Airfoil Generator")
window.geometry("700x600")
window.title("Airfoil Generator")
window.resizable(False, False)

greeting = tk.Label(text="Hello, Tkinter")
greeting.pack()

def selectFileCallback():
  datFilePath = filedialog.askopenfile(parent=window, mode='rb', title='Choose a file')
  greeting.configure(text=datFilePath)

def generateCallback():

  f = open("results.scr", "x")
  f.write(sg.generateSplines(datFilePath))
  f.close()

selectFile = tk.Button(text="Select File", command= selectFileCallback)
selectFile.pack()

generate = tk.Button(text="Generate Script", command= generateCallback)
generate.pack()

window.mainloop()
