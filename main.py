import tkinter as tk
from tkinter import filedialog
import os

import scriptGenerator as sg
import errorChecking as ec

datFilePath = ""

window = tk.Tk(screenName="Airfoil Generator", baseName="Airfoil Generator")
window.geometry("700x600")
window.title("Airfoil Generator")
window.resizable(False, False)

def selectFileCallback():
  dialogPath = filedialog.askopenfile(parent=window, mode='rb', title='Choose a file')

  if(dialogPath == None):
    return
  
  global datFilePath # set variable out side function scope 

  datFilePath = dialogPath.name
  dataDisplay = datFilePath
  if len(dataDisplay) > 50:
    dataDisplay = "..." + dataDisplay[50:] 

  fileLabel.configure(text="File: " + dataDisplay, fg="white")

def generateCallback():
  global datFilePath

  if datFilePath == "" or datFilePath == None:
    errorLabel.configure(text="Error: No file selected", fg="red")
    return
  
  # error checking
  if not splineCount.get().isnumeric():
    print(splineCount.get())
    errorLabel.configure(text="Error: Invalid input", fg="red")
    print("error not int")
    return
  if not ec.isNumeric(totalRotation.get(), totalHeight.get(), convergenceX.get(), convergenceY.get(), wingScaleX.get(), wingScaleY.get()):
    errorLabel.configure(text="Error: Invalid input", fg="red")
    print("error not floats")
    return

  sg.totalRotation = float(totalRotation.get())
  sg.totalHeight = float(totalHeight.get())
  sg.wingScaleX = float(wingScaleX.get())
  sg.wingScaleY = float(wingScaleY.get())
  sg.convergenceX = float(convergenceX.get())
  sg.convergenceY = float(convergenceY.get())
  sg.splineCount = int(splineCount.get())

  errorLabel.configure(text="")

  if os.path.exists("results.scr"):
    os.remove("results.scr")

  f = open("results.scr", "x")
  f.write(sg.generateSplines(datFilePath))
  f.close()

  errorLabel.configure(text="Success: results.scr generated", fg="green")

tk.Label(text="Airfoil Generator", font=("Arial",30)).grid(row=0, columnspan=4, pady=10, padx=10)

# if the widget is smaller than the grid sticky will position it according 
# to a cardinal direction, in this case West (left) and in the vetically centered 
tk.Button(text="Select File", command= selectFileCallback).grid(row=1,sticky="W",column=0, padx=(10,0))

fileLabel = tk.Label(text="File: None selected", fg="red")
fileLabel.grid(row=2, sticky="W", columnspan=4, pady=(0,10), padx=(10,0))

tk.Label(text="Total Rotation:").grid(row=3, sticky="W", padx=(10,0))
totalRotation = tk.Entry()
totalRotation.grid(row=3, column=1)

tk.Label(text="Total Height:").grid(row=3, column=2, sticky="W", padx=(10,0))
totalHeight = tk.Entry()
totalHeight.grid(row=3, column=3)

tk.Label(text="Convergence X:").grid(row=4, sticky="W", padx=(10,0))
convergenceX = tk.Entry()
convergenceX.grid(row=4, column=1)

tk.Label(text="Convergence Y:").grid(row=4, column=2, sticky="W",)
convergenceY = tk.Entry()
convergenceY.grid(row=4, column=3)

tk.Label(text="Wing Scale X:").grid(row=5, sticky="W", padx=(10,0))
wingScaleX = tk.Entry()
wingScaleX.grid(row=5, column=1)

tk.Label(text="Wing Scale Y:").grid(row=5, column=2, sticky="W")
wingScaleY = tk.Entry()
wingScaleY.grid(row=5, column=3)

tk.Label(text="Spline Count:").grid(row=6, column=0, sticky="W", padx=(10,0))
splineCount = tk.Entry()
splineCount.grid(row=6, column=1)

errorLabel = tk.Label(text="")
errorLabel.grid(row=7, column=1, columnspan=3, sticky="W")

# if you put parameters on the command function it won't have context ig 
generateButton = tk.Button(text="Generate Script", command= generateCallback)
generateButton.grid(row=7, column=0,padx=10, pady=20)

window.mainloop()
