# OutrunAI
A supervised machine learning model designed to play the classic 1986 arcade game Outrun, implemented in Python 3.

## Design
The majority of the code is used for interacting with the game, and pre-trained learning models are provided. The normal execution of the game-playing loop follows a three step process:

Extract features --> Predict using learning model --> Simulate controller input

## Learning Algorithms
Two supervised learning models have been implemented: a Decision Tree and a Multilayer Perceptron.

## Repository Breakdown
src/ - Python 3 source files.  
training/ - Sample training data and pre-fit learning models.

## Dependencies
TBD

## Running Instructions

### Record Training Data
GetTrainingData.py

ex. GetTrainingData.py

### Train New Model
TrainModel.py runMode[DecisionTree, NeuralNet] throttleData steeringData warmStart

ex. TrainModel.py NeuralNet ../training/case1/Throttle.csv ../training/case1/Steering.csv False

### Test AI models
main.py runMode[DecisionTree, NeuralNet] trainedModelThrottle trainedModelSteering

ex. main.py NeuralNet "../training/case1/trained mlp/throttle.joblib" "../training/case1/trained mlp/steering.joblib"
