#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  2 01:45:54 2020

@author: larjuang
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def backtest(daily_fluc, allocation, commission):
    """the decision to for investment allocation was already made on 0th, (i-1)th day"""
    """the gain/loss occurs on 1st, ith day"""
    assert len(daily_fluc) == len(allocation) # daily_fluc is 
    weights = np.array([-1, -0.75, 0.5, 0.25, 0, 0.25, 0.5, 0.75, 1])    # only 100%, 50%, and 0 positions available
    total_return = 1
    max_return = 1
    drawdown = []
    return_series = []
    for i in range(len(daily_fluc)):
        pos = allocation[i]
        assert(np.sum(pos) == 1)
        transaction = 0
        if i > 0:
            if np.array_equal(pos, allocation[i-1]) == False:
                transaction = 1
            
        total_return = total_return*(1+np.sum(weights*pos)*daily_fluc[i]) -  transaction*commission
        max_return = max(max_return, total_return)
        drawdown.append(total_return/max_return)
        return_series.append(total_return)
        total_return = max(0, total_return)


    return total_return, np.array(drawdown), np.array(return_series)


data = pd.read_csv("Data/SPY.csv") # to be manually replaced by files in Data folder
data["Date"] = pd.to_datetime(data["Date"])
data["Open"] = data["Open"]*data["Adj Close"]/data["Close"] 
data["High"] = data["High"]*data["Adj Close"]/data["Close"] 
data["Low"] = data["Low"]*data["Adj Close"]/data["Close"] 

data["Adj Close Yesterday"] = data["Adj Close"].shift(1)
data["High 5"] = data["Adj Close"].rolling(5).max()
data["High 10"] = data["Adj Close"].rolling(10).max()
data["High 20"] = data["Adj Close"].rolling(20).max()
data["High 50"] = data["Adj Close"].rolling(50).max()
data["High 75"] = data["Adj Close"].rolling(75).max()
data["High 100"] = data["Adj Close"].rolling(100).max()
data["High 125"] = data["Adj Close"].rolling(125).max()
data["Low 20"] = data["Adj Close"].rolling(20).min()
data["Low 30"] = data["Adj Close"].rolling(30).min()
data["Low 40"] = data["Adj Close"].rolling(40).min()
data["Low 50"] = data["Adj Close"].rolling(50).min()
data["Low 75"] = data["Adj Close"].rolling(75).min()
data["Low 100"] = data["Adj Close"].rolling(100).min()
data["Low 125"] = data["Adj Close"].rolling(125).min()

data["Daily Fluctuation"] = (data["Adj Close"].values-data["Adj Close Yesterday"].values)/data["Adj Close Yesterday"].values


data = data.dropna()
data = data.reset_index(drop = True)

action = [0]

for n in range(1, len(data)):
    if (data["Adj Close"][n] >= data["High 50"][n]) and (action[n-1] == 0):
        position = 1
        action.append(position)
        continue
    if (data["Adj Close"][n] >= data["High 75"][n]) and (action[n-1] == 1):
        position = 2
        action.append(position)
        continue
    if (data["Adj Close"][n] >= data["High 100"][n]) and (action[n-1] == 2):
        position = 3
        action.append(position)
        continue
    if (data["Adj Close"][n] >= data["High 125"][n]) and (action[n-1] == 3):
        position = 4
        action.append(position)
        continue    
    if (data["Adj Close"][n] <= data["Low 20"][n]) and (action[n-1] > 0):
        position = action[n-1] - 1
        action.append(position)
        continue
    if (data["Adj Close"][n] <= data["Low 30"][n]) and (action[n-1] == 0):
        position = -1
        action.append(position)
        continue
    if (data["Adj Close"][n] <= data["Low 40"][n]) and (action[n-1] == -1):
        position = -2
        action.append(position)
        continue
    if (data["Adj Close"][n] <= data["Low 50"][n]) and (action[n-1] == -2):
        position = -3
        action.append(position)
        continue
    if (data["Adj Close"][n] <= data["Low 75"][n]) and (action[n-1] == -3):
        position = -4
        action.append(position)
        continue    
    if (data["Adj Close"][n] >= data["High 5"][n]) and (action[n-1] < 0):
        position = action[n-1] + 1
        action.append(position)
        continue 
    
    
    
    
    
    
    position = action[n-1]
    action.append(position)
 
allocation = []
for n in range(len(action)):
    if action[n] == 0:
        allocation.append(np.array([0, 0, 0, 0, 1, 0, 0, 0, 0]))
        continue
    if action[n] == 1:
        allocation.append(np.array([0, 0, 0, 0, 0, 1, 0, 0, 0]))
        continue
    if action[n] == 2:
        allocation.append(np.array([0, 0, 0, 0, 0, 0, 1, 0, 0]))
        continue
    if action[n] == 3:
        allocation.append(np.array([0, 0, 0, 0, 0, 0, 0, 1, 0]))
        continue
    if action[n] == 4:
        allocation.append(np.array([0, 0, 0, 0, 0, 0, 0, 0, 1]))
        continue
    if action[n] == -1:
        allocation.append(np.array([0, 0, 0, 1, 0, 0, 0, 0, 0]))
        continue
    if action[n] == -2:
        allocation.append(np.array([0, 0, 1, 0, 0, 0, 0, 0, 0]))
        continue
    if action[n] == -3:
        allocation.append(np.array([0, 1, 0, 0, 0, 0, 0, 0, 0]))
        continue
    if action[n] == -4:
        allocation.append(np.array([1, 0, 0, 0, 0, 0, 0, 0, 0]))
        continue
        
    
    
#data["action"] = action
total_return, drawdown, return_series = backtest(data["Daily Fluctuation"], allocation, 0.0003)
    
plt.figure(1)
plt.plot(data["Date"], data["Adj Close"])
plt.plot(data["Date"], data["High 50"])
plt.plot(data["Date"], data["Low 50"])

plt.figure(2)
plt.plot(data["Date"], return_series)
plt.figure(3)
plt.plot(data["Date"], drawdown)
plt.figure(4)
plt.plot(data["Date"], action)

 

    

