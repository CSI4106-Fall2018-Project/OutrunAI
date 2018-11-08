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

		#Old way of doing things (less efficient, more delays)
		# if (maxFps > self.fps):
		# 	#Ensure there is always at least 1ms of waiting time
		# 	sleepTime = max(int((1/self.fps - 1/maxFps) * 1000), 1)

		# 	if cv.waitKey(sleepTime) & 0xFF == ord("q"):
		# 		cv.destroyAllWindows()
		# 		sys.exit()

		# 	displayFps = 1/(time.time() - startTime)

		# 	if (verbose == True):
		# 		print("FPS: ", displayFps, " Slept: ", sleepTime, "ms")
		# else:
		# 	#Wait for the minimum amount of time
		# 	if cv.waitKey(1) & 0xFF == ord("q"):
		# 		cv.destroyAllWindows()
		# 		sys.exit()

		# 	displayFps = 1/(time.time() - startTime)

		# 	if (verbose == True):
		# 		print("Unable to meet desired FPS (", self.fps, "). Currently running at: ", displayFps)

	#Takes the raw image capture and isolates the road lines TODO: Create ROI below horizon
	def filterLines(self, inputFrame):
		if (inputFrame.all() != None):
			outputFrame = cv.cvtColor(inputFrame, cv.COLOR_RGB2GRAY) #Convert to grayscale

			ret, outputFrame = cv.threshold(outputFrame, 245, 255, cv.THRESH_BINARY) #Threshold the image to find the lines
			outputFrame = cv.GaussianBlur(outputFrame, (5, 5), 0) #Remove sharp edges

			#Remove noise
			kernel = np.ones((3, 3), np.uint8)
			outputFrame = cv.morphologyEx(outputFrame, cv.MORPH_OPEN, kernel)

			return outputFrame
		else:
			print("No frame supplied!")
			return None