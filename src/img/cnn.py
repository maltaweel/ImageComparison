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
import ray

#start ray
ray.init()

@ray.remote    
def preVariables():
    (X_train, y_train), (X_test, y_test) = mnist.load_data()

    plt.imshow(X_train[0])
    X_train[0].shape 
    
    return X_train,y_train,X_test,y_test        
           
@ray.remote         
def data_preprocessing (X_train,X_test):
    #reshape data to fit model
    X_train = X_train.reshape(60000,28,28,1)
    X_test = X_test.reshape(10000,28,28,1)
    
    return X_train,X_test

@ray.remote       
def one_hot_encode(y_train,y_test):
    #one-hot encode target column
    y_train = to_categorical(y_train)
    y_test = to_categorical(y_test)
    print(y_train[0])
    
    return y_train,y_test

@ray.remote   
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

@ray.remote      
def train_model(X_train,y_train,X_test,y_test,model):
    #train the model
    model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=3)

@ray.remote    
def model_predict(model,X_test,y_test):
    #predict first 4 images in the test set
    model.predict(X_test[:4])
    
    return y_test[:4]


def run():
    
    X_train,y_train,X_test,y_test=ray.get(preVariables.remote())
    plt.imshow(X_train[0])
    
    X_train,X_test=ray.get(data_preprocessing.remote(X_train,X_test))
    y_train,y_test=ray.get(one_hot_encode.remote(y_train,y_test))
    model=build_model.remote()
    ray.get(train_model.remote(X_train,y_train,X_test,y_test,model))
    test=ray.get(model_predict.remote(model,X_test,y_test))
    
    print(test[:4])
    plt.imshow(test[:4])
   
    
#launch the main
if __name__ == "__main__":
    run()
  
