from Display import Display
import sys


# Program entry point
def main(run_mode):
	"""
	Starts the main AI loop.
	:param run_mode: DecisionTree or NeuralNet
	"""
	if run_mode not in {'DecisionTree', 'NeuralNet'}:
		print("Incorrect run mode. Please chose either DecisionTree or NeuralNet")
	else:
		display = Display("Cannonball", 30)
		display.run(run_mode)

# Called upon runtime
if (__name__ == "__main__"):
	main(sys.argv[1:][0])