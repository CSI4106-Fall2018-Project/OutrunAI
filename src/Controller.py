import win32api
import win32con

class Controller:

    @staticmethod
    def left():
        win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x25, 0, 0, 0)

    @staticmethod
    def right():
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x27, 0, 0, 0)

    @staticmethod
    def up():
        win32api.keybd_event(0x26, 0, 0, 0)
        win32api.keybd_event(0x26, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def down():
        win32api.keybd_event(0x28, 0, 0, 0)
        win32api.keybd_event(0x28, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def straight():
        win32api.keybd_event(0x25, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x27, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def accelerate():
        win32api.keybd_event(0x58, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x5A, 0, 0, 0)

    @staticmethod
    def brake():
        win32api.keybd_event(0x5A, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x58, 0, 0, 0)

    @staticmethod
    def coast():
        win32api.keybd_event(0x58, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(0x5A, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def start():
        win32api.keybd_event(0x31, 0, 0, 0)
        win32api.keybd_event(0x31, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def insertCoin():
        win32api.keybd_event(0x35, 0, 0, 0)
        win32api.keybd_event(0x35, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def pause():
        win32api.keybd_event(0x70, 0, 0, 0)
        win32api.keybd_event(0x70, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def nextFrame():
        win32api.keybd_event(0x71, 0, 0, 0)
        win32api.keybd_event(0x71, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def startGame():
        insertCoin()
        start()

    @staticmethod
    def changeView():
        win32api.keybd_event(0x10, 0, 0, 0)
        win32api.keybd_event(0x10, 0, win32con.KEYEVENTF_KEYUP, 0)