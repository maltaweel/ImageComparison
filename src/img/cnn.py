'''
Module applying CNN deep learning.

Created on May 24, 2020

@author: mark
'''
from keras.datasets import mnist
import matplotlib.pyplot as plt
from keras.utils import to_categorical
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Flatten

def preVariables():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    plt.imshow(X_train[0])
    X_train[0].shape 
    
    return X_train,y_train,X_test,y_test        
           
           
def data_preprocessing (X_train,X_test):
    #reshape data to fit model
    X_train = X_train.reshape(60000,28,28,1)
    X_test = X_test.reshape(10000,28,28,1)
    
def one_hot_encode(y_train,y_test):
    #one-hot encode target column
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    y_train[0]
    
def build_model():
    #create model
    model = Sequential()
    #add model layers
    model.add(Conv2D(64, kernel_size=3, activation='relu', input_shape=(28,28,1)))
    model.add(Conv2D(32, kernel_size=3, activation='relu'))
    model.add(Flatten())
    model.add(Dense(10, activation='softmax'))
    
    #compile model using accuracy to measure model performance
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    
    return model
    
def train_model(X_train,y_train,X_test,y_test,model):
    #train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)
    
def model_predict(model,X_test,y_test):
    #predict first 4 images in the test set
    model.predict(X_test[:4])
    
    return y_test[:4]

def run():
    X_train,y_train,X_test,y_test=preVariables()
    data_preprocessing (X_train,X_test)
    model=build_model()
    train_model(X_train,y_train,X_test,y_test,model)
    test=model_predict(model,X_test,y_test)
    print(test)
    
#launch the main
if __name__ == "__main__":
    run()
  
