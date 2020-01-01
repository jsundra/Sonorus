from btwatcher import BtWatcher
from lighting import Lighting

lighting = None

def main():
	global lighting
	lighting = Lighting()
	lighting.setActive(False)

	watcher = BtWatcher()

	watcher.setActiveCallback(onBtActive)
	watcher.start()

	
	try:
		while True:
			lighting.update()
	except KeyboardInterrupt:
		print("Shutting down.")

	lighting.clear()
	watcher.stop()

def onBtActive(btwatcher, active):
	print("Bluetooth active: ", active)
	lighting.setActive(active)

main()