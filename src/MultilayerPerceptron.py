from sklearn.neural_network import MLPClassifier #Scikit-learn Multiplayer Perceptron classifier
from sklearn.externals import joblib #Replacement for Python's built-in persistence model "pickle", designed for large Numpy arrays
import pandas as pd #For loading data from csv file

class MultilayerPerception:

	#Constructor
	def __init__(self, warmStart):
		#Creates a new Multilayer Perceptron classifier using default parameters
		self.classifier = MLPClassifier(warm_start = warmStart)

	#Train the model based on recorded training data
	def fit(self, trainingData):
		data = pd.read_csv(trainingData)
		features = data.loc[:, 'Curvature':'CarPosition']
		observation = data.loc[:, 'Class']

		self.classifier = self.classifier.fit(features, observation)

	#Dumps the trained model to a file
	def dumpModel(self, fileName):
		joblib.dump(self.classifier, fileName)

	#Loads a trained model from a file
	def loadModel(self, fileName):
		self.classifier = joblib.load(fileName)

	#Predicts the output of the trained MLP based on input data
	def predict(self, inputData):
		return self.classifier.predict(inputData) #Causing issues!