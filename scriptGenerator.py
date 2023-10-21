import math
import re 

epsilon = 0.000001

# in degrees
totalRotation = 30
totalHeight = 10

wingScale = 1.5
convergenceX = 0
convergenceY = 0
splineCount = 5

def closeToZero(value: float) -> bool:
  return abs(value) < epsilon

def degToRad(degree: float) -> float:
  return degree * (math.pi / 180)


def calculateXY(x: float, y: float, inversePercent: float, percent: float) -> tuple:
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

def makeCoordString(x: float, y: float, z:float) -> str:
  return str(x) + "," + str(y) + "," + str(z) + "\n"


def generateSplines(datFilePath: str) -> str:
    script = ""

    f = open(datFilePath, "r")
    results = re.findall("-?\d\.\d{6}", f.read())
    f.close()

    for i in range(0, splineCount):
        percent = i / splineCount
        inversePercent = 1 - percent

        z = percent * totalHeight

        adjustedX = float(results[i]) - convergenceX
        adjustedY = float(results[i]) - convergenceY

        script += "SPLINE\n"

        # make sure splines are closed otherwise they won't loft into 3D objects properly
        (xInitial, yInitial) = calculateXY(float(results[0]), float(results[1]), inversePercent, percent)
        script += makeCoordString(xInitial, yInitial, z)

        for j in range(2, len(results), 2):
            (x, y) = calculateXY(float(results[j]), float(results[j + 1]), inversePercent, percent)

            script += makeCoordString(x, y, z)

        # make sure splines are closed otherwise they won't loft into 3D objects properly
        script += makeCoordString(xInitial, yInitial, z)

        #don't specify an end or start tangent using the enter keys
        script += "\n\n\n"
    return script