import re
import os
import math

epsilon = 0.000001

# in degrees
totalRotation = 30
totalHeight = 10

wingScale = 1.5
convergenceX = 0
convergenceY = 0
splineCount = 5

datFilePath = "dat_files/naca4424-80.txt"


def closeToZero(value: float) -> bool:
  return abs(value) < epsilon


def degToRad(degree: float) -> float:
  return degree * (math.pi / 180)


def calculateXY(x: float, y: float) -> tuple:
  x = x * inversePercent + convergenceX
  y = y * inversePercent + convergenceY

  #rotate
  initialAngle = 0
  hyp = math.sqrt(x * x + y * y)

  if closeToZero(x):
    initialAngle = math.atan(0)
  else:
    initialAngle = math.atan(y / x)

  newAngle = initialAngle + degToRad(totalRotation) * percent

  x = math.cos(newAngle) * hyp
  y = math.sin(newAngle) * hyp

  x = x * wingScale
  y = y * wingScale
  return (x, y)


def makeCoordString(x: float, y: float) -> str:
  return str(x) + "," + str(y) + "," + str(z) + "\n"


f = open(datFilePath, "r")
results = re.findall("-?\d\.\d{6}", f.read())

f.close()

if os.path.exists("result.scr"):
  os.remove("result.scr")

f = open("result.scr", "x")

#TODO: Make upper bound inclusive
for i in range(0, splineCount):
  percent = i / splineCount
  inversePercent = 1 - percent

  z = percent * totalHeight

  adjustedX = float(results[i]) - convergenceX
  adjustedY = float(results[i]) - convergenceY

  f.write("SPLINE\n")

  # make sure splines are closed otherwise they won't loft into 3D objects properly
  (xInitial, yInitial) = calculateXY(float(results[0]), float(results[1]))
  f.write(makeCoordString(xInitial, yInitial))

  for j in range(2, len(results), 2):
    (x, y) = calculateXY(float(results[j]), float(results[j + 1]))

    f.write(makeCoordString(x, y))

  # make sure splines are closed otherwise they won't loft into 3D objects properly
  f.write(makeCoordString(xInitial, yInitial))

  #don't specify an end or start tangent using the enter keys
  f.write("\n\n\n")

f.close()
