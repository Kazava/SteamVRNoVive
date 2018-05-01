'''
Created on 3 Oct 2017

@author: murra
'''
import math

def multiply_quarternion(data):
    
    w2 = 0.5
    x2 = -0.5
    y2 = 0.5
    z2 = -0.5
    
    
    x = data[0]
    y = data[1]
    z = data[2]
    
    w1 = data[3]
    x1 = data[4]
    y1 = data[5]
    z1 = data[6] 
    
    #normalise
    normalised_quaterion_data = normalise_quaternion(w1,x1,y1,z1)

    w1 = normalised_quaterion_data[0]
    x1 = normalised_quaterion_data[1]
    y1 = normalised_quaterion_data[2]
    z1 = normalised_quaterion_data[3]

    xo = (x1 *w2) + (y1 * z2) - (z1 * y2) + (w1 * x2)
    yo = (-x1 * z2) + (y1 * w2) + (z1 * x2) + (w1 * y2)
    zo = (x1 * y2) - (y1 * x2) + (z1 * w2) + (w1 * z2)
    wo = (-x1 * x2) - (y1 * y2) - (z1 * z2) + (w1 * w2)

    return [x,y,z,wo,xo,yo,zo]

def normalise_quaternion(w,x,y,z):

    n = math.sqrt(x*x + y*y + z*z + w*w)
    wo = w / n 
    xo = x / n
    yo = y / n
    zo = z / n
    
    #wo = w
    #xo = x
    #yo = y
    #zo = z
    
    return[wo,xo,yo,zo]