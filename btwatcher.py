import sys
import threading
import subprocess

class BtWatcher:

	__active = False
	__callback = None

	def __init__(self):
		self.__callback = None
		self.__clientCount = 0

	def start(self):
		if BtWatcher.__active:
			raise Exception('Watcher is active.')
		if BtWatcher.__callback is None:
			raise Exception('Callback not set.')

		print ("Starting watcher thread.")
		thread = threading.Thread(target=self.__watcherThread)
		thread.start()

	def stop(self):
		print ("Stopping watcher thread.")
		BtWatcher.__active = False

	def setActiveCallback(self, callback):
		BtWatcher.__callback = callback

	def __watcherThread(self):
		BtWatcher.__active = True

		proc = subprocess.Popen('bluetoothctl', stdout=subprocess.PIPE, stdin=subprocess.PIPE)
		print("Watching bluetoothctl.")
	
		try:
			while BtWatcher.__active:
				output = proc.stdout.readline()
				if not output:
					continue
				output = output.decode("utf-8")
				if "Connected: " in output or "Paired: " in output:
					self.__handConnection(output)
		except:
			print ("Unexpected error:", sys.exc_info())

		print ("Update loop spinning down.")

		BtWatcher.__active = False
		proc.terminate()
		print("Cleaned up bluetoothctl.")

	def __handConnection(self, connectStr):
		prev = self.__clientCount
		if "yes" in connectStr:
			self.__clientCount += 1
		elif "no" in connectStr:
			self.__clientCount = max(0, self.__clientCount - 1)
		else:
			print("Unknown connection state: ", connectStr)
			return

		if prev == 0 and self.__clientCount > 0:
			BtWatcher.__callback(self, True)
		elif self.__clientCount == 0 and prev > 0:
			BtWatcher.__callback(self, False)