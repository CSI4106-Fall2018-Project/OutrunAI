from sklearn import tree
import pandas as pd


class DecisionTree:

	# Constructor
	def __init__(self, trainingData):
		self.data = pd.read_csv(trainingData)
		self.features = self.data.loc[:, 'Curvature':'CarPosition']
		self.observation = self.data.loc[:, 'Class']

		self.classifier = tree.DecisionTreeClassifier()
		self.classifier = self.classifier.fit(self.features, self.observation)