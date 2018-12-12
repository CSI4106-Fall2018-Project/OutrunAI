from Display import Display  # For extracting curvature
from Controller import Controller #For changing camera view

import win32api  # To read key presses
import time  # To delay key press recognition
import sys
import pandas as pd  # To export data into a csv format

class DataRecorder:
	def __init__(self):
		# Holds the steering training data, where the Class column is either {Left, Right, Straight}
		self.steering = {'Curvature': [],
			'Speed': [],
			'CarPosition': [],
			'Class': []}

		# Holds the throttle training data, where the Class column is either {Accelerate, Brake, Coast}
		self.throttle = {'Curvature': [],
			'Speed': [],
			'CarPosition': [],
			'Class': []}

		self.pause = False

	def annotate(self):
		"""
		Records the road curvature, speed, and car position while the player is playing the game.
		Extracts the player's key presses and then annotates the training data.
		To stop data extraction, enter CTRL + C in the command prompt where this program is running. Or,
		wait until the two minute logging window has passed.
		On completion, this function outputs the annotated data into training/Steering.csv and training/Throttle.csv
		"""
		display = Display(windowTitle="Cannonball", fps=30)

		print("1. Start the Outrun game")
		print("2. Select a stage")
		print("3. Once the race begins, press enter in this command prompt to start logging")
		print("4. Logging will pause when you press 'p', and stop when you press 'q'")
		start = input("Press Enter to Start Logging: ")

		#To allow the user to swap windows and start playing
		for i in range(3, 0, -1):
			print(i)
			time.sleep(1)

		Controller.changeView()
		print("Logging...")

		while (self.pause == False):
			try:
				startTime = time.time()

				rawFrame = display.capturer.getFrame()
				roadFrame = display.filterLines(rawFrame)
				curvature, car_position, _ = display.calculateCurvature(roadFrame)
				speed = display.calculateSpeed(rawFrame)

				self.throttle['Curvature'].append(curvature)
				self.throttle['Speed'].append(speed)
				self.throttle['CarPosition'].append(car_position)

				self.steering['Curvature'].append(curvature)
				self.steering['Speed'].append(speed)
				self.steering['CarPosition'].append(car_position)

				self.getThrottle() #Records if the player accelerated, braked, or coasted
				self.getSteering() #Records if the player went left, right, or straight
				
				if (win32api.GetAsyncKeyState(0x51) < 0): #Stop recording when the user presses "q"
					self.exportData()
					break
				elif (win32api.GetAsyncKeyState(0x50) < 0): #Pause recording when the user presses "p"
					self.pause != self.pause

				display.syncClock(startTime, time.time(), False)
			except KeyboardInterrupt:
				self.exportData() #In the event the user uses Ctrl + C to exit, save the data
				break

	def getThrottle(self):
		# Get the keypress
		if win32api.GetAsyncKeyState(0x5A) < 0: # Accelerate
			self.throttle['Class'].append('Accelerate')
		elif win32api.GetAsyncKeyState(0x58) < 0: # Brake
			self.throttle['Class'].append('Brake')
		else:  # Coast
			self.throttle['Class'].append('Coast')

	def getSteering(self):
		# Get the KeyPress
		if win32api.GetAsyncKeyState(0x25) < 0:  # Left Arrow
			self.steering['Class'].append('Left')
		elif win32api.GetAsyncKeyState(0x27) < 0:  # Right Arrow
			self.steering['Class'].append('Right')
		else:  # Going Straight
			self.steering['Class'].append('Straight')

	def exportData(self):
		pd.DataFrame(self.throttle).to_csv('../training/Throttle.csv', mode = 'w', header = True)
		pd.DataFrame(self.steering).to_csv('../training/Steering.csv', mode = 'w', header = True)
		print("Throttle Data Extracted in training/Throttle.csv")
		print("Steering Data Extracted in training/Steering.csv")

def main():
	recorder = DataRecorder()
	recorder.annotate()

#Called upon runtime
if (__name__ == "__main__"):
	main()