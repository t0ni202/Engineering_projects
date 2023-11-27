"""
This module provides functionality for calculating the great circle distance between two points on the surface of a sphere, 
typically Earth. It includes a function that implements the Vincenty formula to compute the distance, given the latitude and 
longitude of the two points. The module is particularly useful for geographical applications where the distance between two 
locations needs to be determined considering the curvature of the Earth.
"""

from math import pi, sqrt, sin, cos, atan2, radians
import csv

def great_circle_distance(loc1,loc2,r=6371.0,units='degrees'):
    ''' 
        computes the great_circle_distance using the Vincenty formula
        loc1[0] is latitude of point 1 and loc1[1] is longitude of point 1
        loc2[0] is latitude of point 2 and loc2[1] is longitude of point 2
        r is the radius of the sphere (default is Earth's radius in km)
        units is 'degrees' by default; radians assumed if this is any other value
    '''

    d = 0.0
    
    if units == 'degrees':
        lat1 = radians(loc1[0])
        long1=radians(loc1[1])
        lat2 = radians(loc2[0])
        long2 = radians(loc2[1])
    loc1 = (lat1,long1)
    loc2 = (lat2,long2)
    dlat=lat2-lat1    
    
    nume = sqrt(((cos(loc2[1])*sin(dlat))**2)+((cos(loc1[1])*sin(loc2[1]))- (sin(loc1[1])*cos(loc2[1])*cos(dlat)))**2)
    denom = (sin(loc1[1])*sin(loc2[1]))+(cos(loc1[1])*cos(loc2[1])*cos(dlat))
    d = r* atan2(nume,denom)
    return d

def main():

    csvinput = input('Enter name of CSV file containing name and coordinates of selected cities:\n')
    ''' Read the reference location name and coordinates from input; convert coordinates to floats and store in a tuple '''
    my_city, my_lat_string, my_long_string = input('Enter a city name, its latitude (deg), and longitude (deg), separated by commas:\n').split(',')
    my_loc = (float(my_lat_string),float(my_long_string))

    ''' Read the CSV file into a dictionary '''
    input_cities_dict = {}
    with open(csvinput) as csvfile:
        citiesreader = csv.reader(csvfile)
        for row in citiesreader:
            input_cities_dict[row[0]]=(float(row[1]),float(row[2]))

    for key,value in input_cities_dict.items():
        print ('{}->{}: {:.2f} km'.format(my_city,key,great_circle_distance(my_loc,value)))


if __name__ == '__main__':
    main()






