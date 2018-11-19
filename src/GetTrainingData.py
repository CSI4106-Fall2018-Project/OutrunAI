from Display import Display  # For extracting curvature
from MemoryScanner import MemoryScanner  # For extracting car speed

import win32api  # To read key presses
import time  # To delay key press recognition
import pandas as pd  # To export data into a csv format


# Holds the steering training data, where the Class column is either {Left, Right, Straight}
steering = {'Curvature': [],
			'Speed': [],
			'CarPosition': [],
			'Class': []}

# Holds the throttle training data, where the Class column is either {Accelerate, Brake, Coast}
throttle = {'Curvature': [],
			'Speed': [],
			'CarPosition': [],
			'Class': []}


def annotate():
	"""
	Records the road curvature, speed, and car position while the player is playing the game.
	Extracts the player's key presses and then annotates the training data.
	To stop data extraction, enter CTRL + C in the command prompt where this program is running. Or,
	wait until the two minute logging window has passed.
	On completion, this function outputs the annotated data into training/Steering.csv and training/Throttle.csv
	"""
	display = Display("Cannonball", 30)

	print("1. Start the Outrun game")
	print("2. Select a stage")
	print("3. Once the race begins, press enter in this command prompt to start logging")
	print("4. Logging will stop after 2 minutes or when you press CTRL + C in this command prompt")
	start = input("Press Enter to Start Logging: ")
	print("Logging...")

	timeout = time.time() + 60*2 # Logging will stop after two minutes

	while True:
		try:
			time.sleep(0.3)
			startTime = time.time()
			rawFrame = display.capturer.getFrame()
			roadFrame = display.filterLines(rawFrame)
			curvature, car_position, _ = display.calculateCurvature(roadFrame)
			speed = display.calculateSpeed(rawFrame)

			throttle['Curvature'].append(curvature)
			throttle['Speed'].append(speed)
			throttle['CarPosition'].append(car_position)

			steering['Curvature'].append(curvature)
			steering['Speed'].append(speed)
			steering['CarPosition'].append(car_position)

			getThrottle()  # Records if the player accelerated, braked, or coasted
			getSteering()  # Records if the player went left, right, or straight

			if time.time() > timeout:
				exportData()
				break

			display.syncClock(startTime, time.time())
		except KeyboardInterrupt:
			exportData()
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


def exportData():
	pd.DataFrame(throttle).to_csv('training/Throttle.csv')
	pd.DataFrame(steering).to_csv('training/Steering.csv')
	print("Throttle Data Extracted in training/Throttle.csv")
	print("Steering Data Extracted in training/Steering.csv")


