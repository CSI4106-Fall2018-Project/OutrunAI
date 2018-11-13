import numpy as np #Image storage used by OpenCV
import win32gui as win32 #Windows

import time #For timing analysis and framerate synchronization
import cv2 as cv #OpenCV for image processing

from Capturer import Capturer #Capturer to grab frames

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

			#horizon = self.findHorizon(rawFrame)

			roadFrame = self.filterLines(rawFrame)

			cv.imshow("Road Frame", roadFrame)

			#Should ALWAYS be called last (to ensure accurate synchronization and avoid undetectable delays)
			self.syncClock(startTime, time.time(), False)

	#Check the current fps and synchronize it to what was specified
	def syncClock(self, startTime, endTime, verbose = False):
		maxFps = 1/(endTime - startTime) #Fastest possible framerate based on executed code

		#Ensure there is always at least 1ms of waiting time
		sleepTime = max(int((1/self.fps - 1/maxFps) * 1000), 1)

		if cv.waitKey(sleepTime) & 0xFF == ord("q"):
			cv.destroyAllWindows()
			sys.exit()

		displayFps = 1/(time.time() - startTime)

		if (verbose == True):
			print("FPS: ", displayFps, " Slept: ", sleepTime, "ms")
	
		return displayFps

	#Takes the raw image capture and finds the position of the horizion
	def findHorizon(self, inputFrame):
		if (inputFrame.all() != None):
			#Do stuff
			horizon = cv.cvtColor(inputFrame, cv.COLOR_RGB2GRAY)
			horizon = cv.GaussianBlur(horizon, (5, 5), 0) #Remove sharp edges

			height, width = inputFrame.shape[:2]

			for i in range(0, height - height / 12, height - 12):
				lines = cv.HoughLinesP(horizon[height//2:height, 0:width], 1, 3.14 / 180, 20, 100, 400)

				for line in lines:
					position = line[0]
					cv.line(horizon, (position[0], position[1]), (position[2], position[3]), (0, 0, 0), 1)

			cv.imshow("Horizon image", horizon)
			return -1
		else:
			print("No frame supplied!")
			return None

	#Takes the raw image capture and isolates the road lines TODO: Create ROI below horizon
	def filterLines(self, inputFrame):
		if (inputFrame.all() != None):
			height, width = inputFrame.shape[:2]

			outputFrame = cv.cvtColor(inputFrame, cv.COLOR_RGB2GRAY) #Convert to grayscale

			outputFrame = cv.GaussianBlur(outputFrame, (3, 3), 0) #Remove sharp edges

			ret, outputFrame = cv.threshold(outputFrame, 245, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			outputFrame, contours, hierarchy = cv.findContours(outputFrame, 1, 2)

			outputFrame = np.zeros((height, width, 1), np.uint8)

			for cnt in contours:
				#moments = cv.moments(cnt)

				area = cv.contourArea(cnt)
				if (area > 0 and area < 300):
					rect = cv.minAreaRect(cnt)
					box = cv.boxPoints(rect)
					box = np.int0(cnt)
					cv.drawContours(outputFrame, [box], 0, (255, 255, 255), -1)

			#Average out the road lines TODO: Use rate of change to smooth values
			roadCurvature = 0
			for k in range(height//3 * 2, height - height//8, 10):
				whiteSum = 0
				whitePixels = 0

				for y in range(k, k + 10):
					for x in range(0, width):
						if (outputFrame.item(y, x, 0) > 0):
							whiteSum += x
							whitePixels += 1

				if (whitePixels > 0):
					whiteAverage = whiteSum// whitePixels
					tmpCurve = (width//2 - whiteAverage) * ( k - (height//3 * 2))

					if (abs(tmpCurve) > abs(roadCurvature)//20 or abs(tmpCurve) < abs(roadCurvature)//20):
						roadCurvature += tmpCurve
						cv.circle(outputFrame, (whiteAverage, y), 2, (255, 255, 255), -1, 8, 0)

			print("Road curvature: ", roadCurvature)
			return outputFrame
		else:
			print("No frame supplied!")
			return None