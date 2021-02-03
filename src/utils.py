from math import radians, cos, sin, asin, sqrt 
import math
from random import Random

rand = Random(12)

def distance(lat1, lat2, lon1, lon2): 
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
       
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
  
    c = 2 * asin(sqrt(a))  
     
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 3956
       
    # calculate the result 
    return (c * r) 

def ang_dis_to_coo(ang, dis, x_center, y_center):
    new_x = x_center - math.cos(math.radians(ang)) * dis
    new_y = y_center - math.sin(math.radians(ang)) * dis
    return new_x, new_y
