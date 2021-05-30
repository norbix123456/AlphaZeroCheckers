import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
import keras.models
import ResNetCheckers
import main
import Training
import pickle
from keras import backend as k

# !!!!!  When loading a model instead of making a new one, uncomment the loadfile command

# from scratch
#myNetwork = ResNetCheckers.Network()
#model = myNetwork.getModel()
#model.save('AlphaZeroCheckersModel')  ###path of file here
victory_threshold = 0.51

# from file
model = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
k.set_value(model.optimizer.learning_rate, 0.0001)
additionalData = []
trainingData = []
# [print(i.shape, i.dtype) for i in model.inputs]
# [print(o.shape, o.dtype) for o in model.outputs]
#with open("TrainingData.txt", "rb") as fp:   # Unpickling
#    additionalData = pickle.load(fp)
print("Choose 1 to training\n")
print("Choose 2 to selfplay\n")
choopaczups = int(input("Choose mode:\n"))
if choopaczups == 1:
    for i in range(1000):
        print("iteration: ", i)

        trainingData = main.selfplay(1, model)  # generate self play data

        #with open("TrainingDataADDITIONAL.txt", "wb") as fp:
        #   pickle.dump(trainingData, fp)

        trainingData = trainingData + additionalData
        newModel = keras.models.load_model('AlphaZeroCheckersModel')  ###path of file here
        k.set_value(newModel.optimizer.learning_rate, 0.0001)
        Training.trainNetwork(newModel, trainingData)  # training loop

        # ##the next 6 lines can be commented to omit evaluation
        isNewNetworkBetter = main.evaluate(model, newModel, 1)  # evaluate model #CHANGE TO 50 GIER
        # print(main.evaluate(model, model, 10))

        if isNewNetworkBetter > victory_threshold:
            print(str(isNewNetworkBetter))
            model = newModel
            print("test passed!")
            additionalData = []
            model.save('AlphaZeroCheckersModel')  ###path of file here
            print("model saved!")
        else:
            print("test failed!")
            print(str(isNewNetworkBetter))
            additionalData = trainingData
            #with open("TrainingData.txt", "wb") as fp:
            #    pickle.dump(trainingData, fp)
        # Training.trainNetwork(model, trainingData)
        # if i % 10 == 0:
        # model.save('AlphaZeroCheckersModel')  ###path of file here
        # print("model saved!")
else:
    print("Players:\n")
    print("0 -> human player\n")
    print("1 -> random player\n")
    print("2 -> alphazero player\n")
    player1 = int(input("Choose first player:\n"))
    player2 = int(input("Choose second player:\n"))
    print(main.evaluateplayer(model, 10, player1, player2))

