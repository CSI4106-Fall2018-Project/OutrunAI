import sys

from DecisionTree import DecisionTree
from MultilayerPerceptron import MultilayerPerception

def main(runMode, throttleData, steeringData, warmStart):

	if (runMode == "DecisionTree"):
		modelThrottle = DecisionTree()
		modelSteering = DecisionTree()
	else:
		if (warmStart == "True"):
			warmStartBool = True
		else:
			warmStartBool = False
		
		modelThrottle = MultilayerPerception(warmStartBool)
		modelSteering = MultilayerPerception(warmStartBool)

		if (warmStartBool == True):
			print("Loading existing model...")
			modelThrottle.loadModel("throttle.joblib")
			modelSteering.loadModel("steering.joblib")

	print("Fitting model...")
	modelThrottle.fit(throttleData)
	modelSteering.fit(steeringData)

	print("\nDumping model...")
	modelThrottle.dumpModel("throttle.joblib")
	modelSteering.dumpModel("steering.joblib")

# Called upon runtime
if (__name__ == "__main__"):
	main(sys.argv[1:][0], sys.argv[1:][1], sys.argv[1:][2], sys.argv[1:][3])