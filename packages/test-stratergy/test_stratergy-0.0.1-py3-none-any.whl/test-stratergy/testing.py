#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 25 19:15:44 2020

@author: harshit
"""

import numpy as np
import pandas as pd

import statistics 

import tensorflow as tf
import keras

from keras.models import model_from_json

global profit
profit = 0

def read_value(file):
        
    with open('{}.txt'.format(file), 'r') as f:
        value = f.read()
        value  = (np.float_(value))
        
    return value
    
    
def write_value(file,string):
    text_file = open("{}.txt".format(file), "w")
    text_file.write(string)
    text_file.close()  
    
    
def selling_avg_price(sd, stop_loss, investment, inventory, df,y):
    
    flag = 0
    avg_price =  statistics.mean(inventory[:y])
    print("Avg Price: ", avg_price)
    
    if (stop_loss==0):
        stop_loss = avg_price - (2 * sd)

    if ((avg_price + sd) <= df[0]):
        stop_loss = avg_price + sd
    
    print("Stop Loss: ",stop_loss)
    
    if( df[0] <= stop_loss ):
         
        global profit
        array = (np.subtract(df[0], inventory[:y]))
        profit += np.sum(array)
        print(inventory[:y])
        print(df[0])
        print(array)
        print("Profit: ", profit)

        investment = 0
        inventory  = np.zeros(1000)
        stop_loss = 0
        y = 0
                     
        print("\n************Selling Stock avg price************\n") 
        flag = 1
        
    return stop_loss, flag, investment, inventory, y
    

def selling_investment_value(investment, inventory, data,y):
   
    flag = 0
    
    value = 0   
    value = investment - (0.05 * investment)
    print("Value:",value)
    print("Investment:", investment)
    print("Current Value: ", (y*data[0]))
    if(value > (y*data[0])):    
         
        global profit

        array = (np.subtract(data[0], inventory[:y]))
        profit += np.sum(array) 
        print(inventory[:y])
        print(data[0])
        print(array)
        print("Profit: ", profit)
        investment = 0
        inventory  = np.zeros(1000)
        y = 0
        
                     
        print("\n************Selling Stock investment************\n") 
        flag  =1
        
    return flag,investment, inventory, y

def selling_max_price(sd, max_price, investment, inventory, data,y):
     
    if max_price < data[0]:
        max_price = data[0]
    
    print("Max Price: ", max_price)
    
    trend1 = read_value("trend1c1")
    trend5 = read_value("trend5c1")
    flag = 0 
    
    
    if ( (data[0] >= (max_price - sd)) and  (trend5 > 0 and trend1 > 0) ):
         
        global profit

        array = (np.subtract(data[0],  inventory[:y]))
        profit += np.sum(array)
        print(inventory[:y])
        print(data[0])
        print(array)
        print("Profit: ", profit)
  
        investment = 0
        inventory  = np.zeros(1000)
                    
        max_price = 0
        y = 0
        flag  =1

    
        print("\n************Selling Stock max price************\n")  
                   
    return flag, max_price, investment, inventory, y
class Testing:
    def __init__(self, name):
        self.filename = name

    def test(self):


        max_price = 0 
        stop_loss = 0
        trend5 = 0 
        inventory  = np.zeros(1000)
        investment = 0 
        k = 0

        dataset_train1 = pd.read_csv('{}_1min.csv'.format(self.filename))
        dataset_train1 = dataset_train1.dropna()
        training_set1 = dataset_train1.iloc[:,1:].values
        # Feature Scaling
        from sklearn.preprocessing import MinMaxScaler
        sc1 = MinMaxScaler(feature_range = (0, 1))
        training_set1_scaled1 = sc1.fit_transform(training_set1)


        # Creating a data structure with 60 DAYsteps and 1 output
        X_train1 = []
        for i in range(120, (training_set1_scaled1.shape[0])):
            X_train1.append(training_set1_scaled1[i-120:i])
        X_train1 = np.array(X_train1)

        # Reshaping
        X_train1 = np.reshape(X_train1, (X_train1.shape[0], X_train1.shape[1], 5))

        config = tf.ConfigProto(
            device_count={'cpu': 0},
            intra_op_parallelism_threads=1,
            allow_soft_placement=True
        )

        session = tf.Session(config=config)

        keras.backend.set_session(session)

        init = tf.global_variables_initializer()
        session.run(init)

        # Part 2 - Building the RNN

        # load json and create model
        json_file = open('regressor1.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        regressor1 = model_from_json(loaded_model_json)
        # load weights into new model
        regressor1.load_weights("bi{}1.h5".format(self.filename))
         

        # Compiling the RNN
        regressor1.compile(optimizer = 'adam', loss = 'mean_squared_error')





        # Importing the training set
        dataset_train5 = pd.read_csv('{}_5min.csv'.format(self.filename))
        dataset_train5 = dataset_train5.dropna()
        training_set5 = dataset_train5.iloc[:,1:].values
        # Feature Scaling
        from sklearn.preprocessing import MinMaxScaler
        sc5 = MinMaxScaler(feature_range = (0, 1))
        training_set_scaled5 = sc5.fit_transform(training_set5)


        # Creating a data structure with 60 DAYsteps and 1 output
        X_train5 = []
        for i in range(120, (training_set_scaled5.shape[0])):
            X_train5.append(training_set_scaled5[i-120:i])
        X_train5 = np.array(X_train5)

        # Reshaping
        X_train5 = np.reshape(X_train5, (X_train5.shape[0], X_train5.shape[1], 5))


        config5 = tf.ConfigProto(
            device_count={'cpu': 0},
            intra_op_parallelism_threads=1,
        )
        session5 = tf.Session(config=config5)

        keras.backend.set_session(session5)

        init5 = tf.global_variables_initializer()
        session5.run(init5)
        # Part 2 - Building the RNN


        json_file = open('regressor5.json', 'r')
        loaded_model_json = json_file.read()
        json_file.close()
        regressor5 = model_from_json(loaded_model_json)
        # load weights into new model
        regressor5.load_weights("{}5.h5".format(self.filename))
        regressor5.compile(optimizer = 'adam', loss = 'mean_squared_error')


        y = 0
        j = 0

        trend1 = 0 
        for i in range(0, X_train1.shape[0]-120):
            
            if j == 5 :
                trend1 = 0
                j = 0        
            X_test1 = X_train1[i:i+120,:]
            with session.as_default():
                with session.graph.as_default():
                    predicted_stock_price1 = regressor1.predict(X_test1)
                    
            predicted_stock_price1 = sc1.inverse_transform(predicted_stock_price1)
            
            pd.DataFrame(predicted_stock_price1).to_csv("prediction_1min_{}1.csv".format(self.filename), index=False)
            
            trend1 = trend1 +  predicted_stock_price1[-2,0] - predicted_stock_price1[-1,0] 
            
            write_value("trend1c1",str(trend1))
            
            j+=1

            
            if i%5==0 and i!=0:


                    X_test = X_train5[y:y+120,:]
                    with session5.as_default():
                        with session5.graph.as_default():
                            predicted_stock_price = regressor5.predict(X_test)
                    predicted_stock_price = sc5.inverse_transform(predicted_stock_price)
                
                    
                    trend5 = predicted_stock_price[-2,0] - predicted_stock_price[-1,0]
                
            
                    trend1 = read_value("trend1c1")
                    
                    if (trend5 <= 0 and trend1 <=0):
            
                        
                        inventory[k] = training_set1[i,1]
                        investment+= training_set1[i,1]
                        k+= 1
                        print("\nBuying Stock")

            
                    """if (trend5 > 0 and trend1 > 0) and (k>0):
                    
                        print(inventory[:k])
                        print(training_set1[i,1])
                        array = (np.subtract(training_set1[i,1],  inventory[:k]))
                        print(array )
                        profit += np.sum(array)      
                        print("Profit: ", profit)
                  
                        investment = 0
                        inventory  = np.zeros(1000)
                            
                        k = 0
                        print("Selling Stock")
                     """   
            
                    if((trend5 < 0 and trend1 > 0 ) or (trend5 > 0 and trend1 < 0) ):
                        print("\nHolding Stock")
                        
                    
                    write_value("trend5c1",str(trend5))
                        
                    pd.DataFrame(predicted_stock_price).to_csv("prediction_5min_{}1.csv".format(self.filename), index=False)
                    trend1 = 0
                    trend5 = 0
                    if (y == X_train5.shape[0]):

                        print(inventory[:k])
                        print(training_set1[i,1])
                        array = (np.subtract(training_set1[i,1],  inventory[:k]))
                        print(array )
                        profit += np.sum(array)      
                        print("Profit: ", profit)                        
                        break
                    y+=1
                                
            if  k > 0:

                flag = 0
                print("Current Stock price: ",  training_set1[i,0])
                sd = statistics.stdev(training_set1[i:120+i,1])
            
                stop_loss, flag, investment, inventory, k = selling_avg_price(sd, stop_loss, investment, inventory, training_set1[i,:],k)
                
                if flag!= 1:
                    flag,investment, inventory, k = selling_investment_value(investment, inventory, training_set1[i,:],k)
                    
                if flag!= 1:
                    flag, max_price, investment, inventory, k = selling_max_price(sd, max_price, investment, inventory, training_set1[i,:],k)
                    
                if flag == 1 :
                    max_price = 0
                    stop_loss  = 0 
            
            print(i)

        print(inventory[:k])
        print(training_set1[i,1])
        array = (np.subtract(training_set1[i,1],  inventory[:k]))
        print(array )

        profit += np.sum(array)      
        print("Profit: ", profit)  

     