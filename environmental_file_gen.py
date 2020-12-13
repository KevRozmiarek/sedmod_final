# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 12:54:26 2020

@author: Kevin Rozmiarek

"""

"""
This code generates a file of the format used in Ku model runs. It accepts the following parameters

-filename
    The name of the generated file. Needs to match the file used in the Ku model
-years
    The number of years to generate values for
-mean
    The average value of the parameter being generator
-method
    The particular method to use to generate data
        -norm: Add noise to each value sampled from a normal distribustion
        -slope: Adds a linear change to the parameter over years. Then runs norm
-option
    If needed, an option added to each method
        -norm: Adds a linear scalar on the noise
        -slope: The slope in change per year

"""


#from random import random
import math
import scipy.stats as stats
import os

def file_gen(filename, years, mean, method, noise, option):
    try:
        os.remove(filename)
    except OSError:
        pass
    
    temp = open(filename,"x")
    for i in range(years): #Main build loop
        
        if method == "norm":
            temp_num = norm_noise(mean, noise)
            
        if method == "slope":
            temp_num = increase(mean, option, i)
            temp_num = norm_noise(temp_num, noise) #Adding norm noise anyways
            
        order_mag = orderOfMagnitude(temp_num) #Get the order of magnitude
        
        if order_mag != 0: #Check for 0 order of magnitude
            file_write_value = temp_num/(10*order_mag) #Without order of magnitude
        if order_mag == 0:
            file_write_value = temp_num
            
        temp.write(str(file_write_value) + "e+0" + str(order_mag) + "\n")
    temp.close()
    
def orderOfMagnitude(number): #Function that returns the order of magnitude of a value
    mag_value = math.floor(math.log(abs(number), 10))
    if mag_value < 0:
        mag_value = 0
    return (mag_value)

def norm_noise(number, scale): #Function that adds normal noise
    norm_value = stats.norm()
    value_report = float(number + norm_value.rvs(1)*scale)
    return(value_report)
    
def increase(number, slope, year): #Function the addes to a value an amount determined by the number of years that have gone by
    value_report = number + slope * year
    return (value_report)

#file_gen("./data/T_air.txt", 1000, -6, "slope", 1, 0.01)