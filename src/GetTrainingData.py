from Display import Display  # For extracting curvature
from MemoryScanner import MemoryScanner  # For extracting car speed

import win32api  # To read key presses
import time  # To delay key press recognition
import pandas as pd  # To export data into a csv format


# Holds the steering training data, where the Class column is either {Left, Right, Straight}
steering = {'Curvature': [],
			'Speed': [],
			'Class': []}

# Holds the throttle training data, where the Class column is either {Accelerate, Brake, Coast}
throttle = {'Curvature': [],
			'Speed': [],
			'Class': []}


def annotate():
	"""
	Records the road curvature and current speed while the player is playing the game.
	Extracts the player's key presses and then annotates the training data.
	To stop data extraction, enter CTRL + C in the command prompt where this program is running.
	On interruption, outputs this annotated data into training/Steering.csv and training/Throttle.csv
	"""
	display = Display("Cannonball", 30)

	print("1. Start the Outrun game")
	print("2. Select a stage")
	print("3. Once the race begins, enter any key in this command prompt to start data extraction")
	print("To stop logging, enter CTRL + C in this command prompt")
	start = input("Enter any key and then press enter: ")
	print("Logging...")
	timeout = time.time() + 60 # Two minutes
	while True:
		try:
			time.sleep(0.5)
			curvature = display.getCurvature()
			# speed = MemoryScanner.readSpeed() # TODO: Implement MemoryScanner.readSpeed
			speed = 0

			throttle['Curvature'].append(curvature)
			throttle['Speed'].append(speed)
			getThrottle()
			getSteering()
			if time.time() > timeout:
				pd.DataFrame(throttle).to_csv('training/Throttle.csv')
				pd.DataFrame(steering).to_csv('training/Steering.csv')
				print("Throttle Data Extracted in training/Throttle.csv")
				print("Steering Data Extracted in training/Steering.csv")
				break
		except KeyboardInterrupt:
			pd.DataFrame(throttle).to_csv('training/Throttle.csv')
			pd.DataFrame(steering).to_csv('training/Steering.csv')
			print("Throttle Data Extracted in training/Throttle.csv")
			print("Steering Data Extracted in training/Steering.csv")
			break


def getThrottle():
	# Get the keypress
	if win32api.GetAsyncKeyState(0x5A) < 0: # Accelerate
		throttle['Class'].append('Accelerate')
	elif win32api.GetAsyncKeyState(0x58) < 0: # Brake
		throttle['Class'].append('Brake')
	else:  # Coast
		throttle['Class'].append('Coast')


def getSteering():
	# Get the KeyPress
	if win32api.GetAsyncKeyState(0x25) < 0:  # Left Arrow
		steering['Class'].append('Left')
	elif win32api.GetAsyncKeyState(0x27) < 0:  # Right Arrow
		steering['Class'].append('Right')
	else:  # Going Straight
		steering['Class'].append('Straight')

