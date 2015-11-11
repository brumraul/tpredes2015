#!/usr/bin/python

import os
import warnings
import scipy.stats as stats
import numpy

critical_values_table = {	3:1.1531, 4:1.4625, 5:1.6714, 6:1.8221, 7:1.9381, 8:2.0317,  9:2.1096, 10:2.1761, 11:2.2339, 12:2.2850, 13:2.3305, 
							14:2.3717, 15:2.4090, 16:2.4433, 17:2.4748, 18:2.5040, 19:2.5312, 20:2.5566,
							21:2.58, 22:2.60, 23:2.62, 24:2.64, 25:2.66, 26:2.681, 27:2.698, 28:2.714, 29:2.730, 30:2.745, 31:2.759}


#test cases
points1 = [199.31, 199.53, 200.19, 200.82, 201.92, 201.95, 202.18, 245.57]
points2 = stats.norm.rvs(size = 31) # deberia dar false la mayoria de las veces por ser una muestra normal
points3 = stats.norm.rvs(size = 20) # deberia dar false la mayoria de las veces por ser una muestra normal
points4 = [199.31, 199.53, 200.19, 200.82, 201.92, 201.95, 202.18, 245.57, 
			245.57, 245.57,245.57,245.57,245.57,245.57,245.57,245.,
			245.57,245.57,245.57,10000] # deberia dar true
			
			
points5 = [stats.norm.rvs(size = 100), 1000, 1001, 1003]



def is_normal(points):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return stats.normaltest(points) >= 0.05

def hay_outliers(points):
	mean = numpy.mean(points)
	std = numpy.std(points)
	critical_value = critical_values_table[len(points)-1]
	G = (max(points) - mean) / std
	return G > critical_value 	 # rechazo la hipotesis nula si G > critical_value
									 # la hipotesis nula es: el valor maximo no es un oulier	
										

# nodes: {ip,rtt,mean,std,delta}			 
def get_outliers(nodes):
    f = open('out', 'w')
    outliers = []
    i = 0
    while hay_outliers([n['delta'] for n in nodes]) and i < 4:
        max_delta = max([n['delta'] for n in nodes])
        outliers += [n['ip'] for n in nodes if n['delta'] == max_delta]
        nodes = [n for n in nodes if n['delta'] != max_delta]
        f.write(str(i))
        i += 1
    f.close()
    return outliers
        
        
									 
def tester():
	print hay_outliers(points1) # deberia dar true
	print hay_outliers(points2)
	print hay_outliers(points3)
	print hay_outliers(points4)

	print 'Outliers points4:'
	get_outliers(points4)
	
	
	print 'Outliers points5:'
	get_outliers(points5)

if __name__ == '__main__':
	tester()

