from Display import Display
import sys


# Program entry point
def main(runMode, trainedModelThrottle, trainedModelSteering):
	"""
	Starts the main AI loop.
	:param run_mode: DecisionTree or NeuralNet
	:param trainedModelThrottle: Location of trained throttle model.
		e.g training/casex/trained decision tree/throttle.joblib
		e.g training/casex/trained mlp/throttle.joblib
	:param trainedModelSteering: Location of trained steering model.
		e.g training/casex/trained decision tree/steering.joblib
		e.g training/casex/trained mlp/steering.joblib
	"""
	if runMode not in {'DecisionTree', 'NeuralNet'}:
		print("Incorrect run mode. Please chose either DecisionTree or NeuralNet")
	else:
		display = Display(trainedModelThrottle, trainedModelSteering, runMode, "Cannonball", 30)
		display.run()

# Called upon runtime
if (__name__ == "__main__"):
	main(sys.argv[1:][0], sys.argv[1:][1], sys.argv[1:][2])