import numpy as np #Image storage used by OpenCV
import win32gui as win32 #Windows

import time #For timing analysis and framerate synchronization
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
	def findHorizon(self, inputFrame): #TODO: Update horizon detection based on new limited scope
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

			ret, outputFrame = cv.threshold(outputFrame, 245, 255, cv.THRESH_BINARY) #Threshold the image to find the lines

			outputFrame, contours, hierarchy = cv.findContours(outputFrame, 0, 2)

			#outputFrame = np.zeros((height, width, 1), np.uint8)

			vxAvg = 0
			vyAvg = 0
			xAvg = 0
			yAvg = 0
			numberPoints = 0
			for cnt in contours:
				#check blob size
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

				cv.line(outputFrame, (xAvg, yAvg), (xAvg + (20 * vxAvg), yAvg + (20 * vyAvg)), (255, 255, 255), 1)

				#print("Road curvature: ", width//2 - xAvg / numberPoints)
				print("Road curvature: ", vxAvg)

			#TODO: Work on the following experimental curve detection
			# rvxAvg = 0
			# rvyAvg = 0
			# rxAvg = 0
			# ryAvg = 0
			# rNumberPoints = 0

			# lvxAvg = 0
			# lvyAvg = 0
			# lxAvg = 0
			# lyAvg = 0
			# lNumberPoints = 0
			# for cnt in contours:
			# 	#check blob size
			# 	if (cv.contourArea(cnt) > 20):

			# 		moment = cv.moments(cnt) #Calculate the moment of each blob

			# 		[vx,vy,x,y] = cv.fitLine(cnt, cv.DIST_L2, 0, 0.01, 0.01) #Fit a straight line to each moment

			# 		if (y > height//3 and abs(vx) > 0.05 and abs(vx) < 0.99):
			# 			if (x > width//2):
			# 				vx *= -1;
			# 				vy *= -1;

			# 				rvxAvg += vx
			# 				rvyAvg += vy
			# 				rxAvg += x
			# 				ryAvg += y
			# 				rNumberPoints += 1
			# 			else:
			# 				lvxAvg += vx
			# 				lvyAvg += vy
			# 				lxAvg += x
			# 				lyAvg += y
			# 				lNumberPoints += 1


			# 			cv.arrowedLine(outputFrame, (x, y), (x + (20 * vx), y + (20 * vy)), (255, 255, 255), 2, tipLength=0.5) #Display the direction of each moment
			# 			#cv.line(outputFrame, (x, y), (x + (20 * vx), y + (20 * vy)), (255, 255, 255), 3)
			# 			cv.putText(outputFrame, str(vx[0])[:5], (x, y), cv.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255))
			
			# if (rNumberPoints > 0):
			# 	rvxAvg /= -rNumberPoints
			# 	rvyAvg /= rNumberPoints
			# 	rxAvg /= rNumberPoints
			# 	ryAvg /= rNumberPoints

			# if (lNumberPoints > 0):
			# 	lvxAvg /= -lNumberPoints
			# 	lvyAvg /= lNumberPoints
			# 	lxAvg /= lNumberPoints
			# 	lyAvg /= lNumberPoints

			# if (rNumberPoints + lNumberPoints > 0):
			# 	vxAvg = (rvxAvg + lvxAvg)/2
			# 	vyAvg = (rvyAvg + lvyAvg)/2
			# 	xAvg = (rxAvg + lxAvg)/2
			# 	yAvg = (ryAvg + lyAvg)/2

			# 	cv.line(outputFrame, (xAvg, yAvg), (xAvg + (20 * vxAvg), yAvg + (20 * vyAvg)), (255, 255, 255), 1)

			# 	#print("Road curvature: ", width//2 - xAvg / numberPoints)
			# 	print("Road curvature: ", vxAvg)

			return outputFrame
		else:
			print("No frame supplied!")
			return None