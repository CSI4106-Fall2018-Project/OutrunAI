import sys
import win32gui as win32 #Windows
import time #For timing analysis and framerate synchronization

import numpy as np #Image storage used by OpenCV
import cv2 as cv #OpenCV for image processing

from Capturer import Capturer #Capturer to grab frames
from Controller import Controller

class Display:
	#Constructor
	def __init__(self, windowTitle = "", fps = -1):
		self.capturer = Capturer(windowTitle)
		self.fps = fps

	#Main program
	def run(self):
		#Start the capture loop
		while(True):
			startTime = time.time()

			rawFrame = self.capturer.getFrame()

			roadFrame = self.filterLines(rawFrame)

			roadCurvature, carPosition, outputFrame = self.calculateCurvature(roadFrame)

			#print("Road curvature: ", roadCurvature, " Car position: ", carPosition)

			speed = self.calculateSpeed(rawFrame)

			print(speed, "km/h")

			#Extremely simple decision tree for controlling the car's steering
			# if (roadCurvature < -0.05):
			# 	print("Left")
			# 	Controller.left()
			# elif (roadCurvature > 0.05):
			# 	print("Right")
			# 	Controller.right()
			# else:
			# 	print("Straight")
			# 	Controller.straight()

			cv.imshow("Road Frame", outputFrame)

			#Should ALWAYS be called last (to ensure accurate synchronization and avoid undetectable delays)
			self.syncClock(startTime, time.time(), False)

	#Check the current fps and synchronize it to what was specified
	def syncClock(self, startTime, endTime, verbose = False):
		maxFps = 1/(endTime - startTime) #Fastest possible framerate based on executed code

		#Ensure there is always at least 1ms of waiting time
		sleepTime = max(int((1/self.fps - 1/maxFps) * 1000), 1)

		if cv.waitKey(sleepTime) & 0xFF == ord("q"):
			cv.destroyAllWindows()
			sys.exit(0)

		displayFps = 1/(time.time() - startTime)

		if (verbose == True):
			print("FPS: ", displayFps, " Slept: ", sleepTime, "ms")

		return displayFps

	#Takes the raw image capture and isolates the road lines
	def filterLines(self, inputFrame):
		if (inputFrame.all() != None):
			outputFrame = cv.cvtColor(inputFrame, cv.COLOR_RGB2GRAY) #Convert to grayscale

			ret, outputFrame = cv.threshold(outputFrame, 245, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			return outputFrame
		else:
			print("No frame supplied!")
			return None

	#Calculates road curvature and car position
	def calculateCurvature(self, inputFrame):
		height, width = inputFrame.shape[:2]

		outputFrame, contours, hierarchy = cv.findContours(inputFrame, 0, 2)

		vxAvg = 0
		vyAvg = 0
		xAvg = 0
		yAvg = 0
		numberPoints = 0

		for cnt in contours:
			#Check that the contour actually represents a line
			if (cv.contourArea(cnt) > 30):

				moment = cv.moments(cnt) #Calculate the moment of each blob

				[vx,vy,x,y] = cv.fitLine(cnt, cv.DIST_L2, 0, 0.01, 0.01) #Fit a straight line to each moment

				if (x > int(width/2)):
					vx *= -1;
					vy *= -1;

				if (y > height//3 and abs(vx) > 0.05 and abs(vx) < 0.99):
					cv.arrowedLine(outputFrame, (x, y), (x + (20 * vx), y + (20 * vy)), (255, 255, 255), 2, tipLength=0.5) #Display the direction of each moment
					#cv.line(outputFrame, (x, y), (x + (20 * vx), y + (20 * vy)), (255, 255, 255), 3)
					cv.putText(outputFrame, str(vx[0])[:5], (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))

					vxAvg += vx
					vyAvg += vy
					xAvg += x
					yAvg += y
					numberPoints += 1

		if (numberPoints > 0):
			vxAvg /= -numberPoints
			vyAvg /= numberPoints
			xAvg /= numberPoints
			yAvg /= numberPoints

			return vxAvg[0], xAvg[0], outputFrame

		return -99, -99, outputFrame #Default return (no lines found)

	#Gets the speed displayed on the screen, using a modular method that works with different screen resolutions
	def calculateSpeed(self, inputFrame):
		if (inputFrame.all() != None):
			height, width = inputFrame.shape[:2]
			numberSize = (int(round(0.0969 * width)) - int(round(0.0781 * width))) * (int(round(0.9598 * height)) - int(round(0.9107 * height)))

			#Digit one
			digitOne = inputFrame[int(round(0.9107 * height)):int(round(0.9598 * height)), int(round(0.0781 * width)):int(round(0.0969 * width))][:,:,2]
			ret, digitOne = cv.threshold(digitOne, 254, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			digitOneLeft = inputFrame[int(round(0.9107 * height)):int(round(0.9598 * height)), int(round(0.0781 * width)):int(round(0.0875 * width))][:,:,2]
			ret, digitOneLeft = cv.threshold(digitOneLeft, 254, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			hundreds = cv.countNonZero(digitOne) + cv.countNonZero(digitOneLeft)
			hundreds = self.convertSpeed(hundreds, numberSize)

			#Digit two
			digitTwo = inputFrame[int(round(0.9107 * height)):int(round(0.9598 * height)), int(round(0.1031 * width)):int(round(0.1219 * width))][:,:,2]
			ret, digitTwo = cv.threshold(digitTwo, 254, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			digitTwoLeft = inputFrame[int(round(0.9107 * height)):int(round(0.9598 * height)), int(round(0.1031 * width)):int(round(0.1125 * width))][:,:,2]
			ret, digitTwoLeft = cv.threshold(digitTwoLeft, 254, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			tens = cv.countNonZero(digitTwo) + cv.countNonZero(digitTwoLeft)
			tens = self.convertSpeed(tens, numberSize)

			#Digit three
			digitThree = inputFrame[int(round(0.9107 * height)):int(round(0.9598 * height)), int(round(0.1281 * width)):int(round(0.1469 * width))][:,:,2]
			ret, digitThree = cv.threshold(digitThree, 254, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			digitThreeLeft = inputFrame[int(round(0.9107 * height)):int(round(0.9598 * height)), int(round(0.1281 * width)):int(round(0.1375 * width))][:,:,2]
			ret, digitThreeLeft = cv.threshold(digitThreeLeft, 254, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			ones = cv.countNonZero(digitThree) + cv.countNonZero(digitThreeLeft)
			ones = self.convertSpeed(ones, numberSize)

			return str(hundreds) + str(tens) + str(ones)
		else:
			print("No frame supplied!")
			return -1

	#Helper method to decode the digits into their real values based on the below table (640x448), numberSize = 264:
	# 0: 96 + 48 = 144
	# 1: 40 + 0 = 40
	# 2: 88 + 44 = 132
	# 3: 92 + 36 = 128
	# 4: 76 + 28 = 104
	# 5: 80 + 40 = 120
	# 6: 96 + 56 = 152
	# 7: 68 + 24 = 92
	# 8: 112 + 56 = 168
	# 9: 96 + 40 = 136
	def convertSpeed(self, num, numberSize):
		pixelRatio = num / numberSize

		if (pixelRatio == 0 or pixelRatio == 144 / 264):
			return 0
		elif (pixelRatio == 40 / 264):
			return 1
		elif (pixelRatio == 132 / 264):
			return 2
		elif (pixelRatio == 128 / 264):
			return 3
		elif (pixelRatio == 104 / 264):
			return 4
		elif (pixelRatio == 120 / 264):
			return 5
		elif (pixelRatio == 152 / 264):
			return 6
		elif (pixelRatio == 92 / 264):
			return 7
		elif (pixelRatio == 168 / 264):
			return 8
		elif (pixelRatio == 136 / 264):
			return 9
