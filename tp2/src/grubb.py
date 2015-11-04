#!/usr/bin/python

import scipy.stats as stats
import numpy

critical_values_table = {	3:1.1531, 4:1.4625, 5:1.6714, 6:1.8221, 7:1.9381, 8:2.0317,  9:2.1096, 10:2.1761, 11:2.2339, 12:2.2850, 13:2.3305, 
							14:2.3717, 15:2.4090, 16:2.4433, 17:2.4748, 18:2.5040, 19:2.5312, 20:2.5566,
							21:2.58, 22:2.60, 23:2.62, 24:2.64, 25:2.66, 26:2.681, 27:2.698, 28:2.714, 29:2.730, 30:2.745, 31:2.759}

# si el normal test tiene un p-valor mayor a 0.05 rechazo la hipotesis, si no considero que la distribucion es normal
def is_normal(points):
	return stats.normaltest(points) >= 0.05

def hay_outliers(points):
	mean = numpy.mean(points)
	std = numpy.std(points)
	if is_normal(points):
		critical_value = critical_values_table[len(points)-1]
		G = (max(points) - mean) / std
		return G > critical_value 	 # rechazo la hipotesis nula si G > 2.032
									 # la hipotesis nula es: el valor maximo no es un oulier	
									 
									 
									 
def tester():
	error = False
	
	points = [199.31, 199.53, 200.19, 200.82, 201.92, 201.95, 202.18, 245.57]
	print hay_outliers(points) # deberia dar true

	points = stats.norm.rvs(size = 31) # deberia dar false la mayoria de las veces por ser una muestra normal
	print hay_outliers(points)

	points = stats.norm.rvs(size = 20) # deberia dar false la mayoria de las veces por ser una muestra normal
	print hay_outliers(points)

	points = [199.31, 199.53, 200.19, 200.82, 201.92, 201.95, 202.18, 245.57, 
				245.57, 245.57,245.57,245.57,245.57,245.57,245.57,245.,
				245.57,245.57,245.57,10000] # deberia dar true
	print hay_outliers(points)

if __name__ == '__main__':
	tester()


