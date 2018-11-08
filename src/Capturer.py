import numpy as np #Image storage used by OpenCV
import mss #Screen capturer
import win32gui as win32 #Windows

class Capturer:
	#Constructor TODO: Add some error handling
	def __init__(self, windowTitle):
		self.windowTitle = windowTitle #Title of window to capture
		self.windowHandle = win32.FindWindow(None, self.windowTitle) #Handle representing the window to capture
		self.clientRect = win32.GetClientRect(self.windowHandle) #Rectangle representing the window's size
		self.windowRect = win32.GetWindowRect(self.windowHandle) #Rectangle representing the windon's top left and bottom right position

		#Calculate the window border offset
		self.edgeBorder = int(((self.windowRect[2] - self.windowRect[0]) - self.clientRect[2]) / 2)
		self.topBorder = (self.windowRect[3] - self.windowRect[1]) - self.clientRect[3] - self.edgeBorder

		#Calculate the window's position and size
		self.x = self.windowRect[0] + self.edgeBorder
		self.y = self.windowRect[1] + self.topBorder
		self.width = self.clientRect[2]
		self.height = self.clientRect[3]

		self.captureArea = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}

	#Returns the current frame of the window associated with the capturer
	def getFrame(self):
		with mss.mss() as sct:
			frame = np.array(sct.grab(self.captureArea))

		return frame