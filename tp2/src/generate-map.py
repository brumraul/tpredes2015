#!/usr/bin/python
import urllib2
import argparse
import json
import pygmaps
import os

def get_ip_info(ip):
    data = json.loads(urllib2.urlopen(" http://www.telize.com/geoip/"+ip).read())
    lat = data.get('latitude','')
    lon = data.get('longitude','')
    country = data.get('country','')
    city = data.get('city','')
    return lat,lon,country,city


parser = argparse.ArgumentParser(description="plot traceroute on map from ip list")
parser.add_argument('-l', '--list', required=True, nargs='+', type=str, help='ip address separated by blank space')
parser.add_argument('-o', '--out', type=str, help='output filename', metavar='FILE')
args = parser.parse_args()

output = "./mymap.html"
if not args.out == None:
    output = args.out

traceList = []

for ip in args.list:
    latitude,longitude,country,city = get_ip_info(ip)
    info = {'ip':ip, 'latitude':latitude, 'longitude':longitude, 'country':country, 'city':city}
    traceList.append(info)


mymap = pygmaps.maps(0, 0, 2)
path= []
for l in traceList:
    mymap.addpoint(l['latitude'],l['longitude'], "#FF0000", l['ip'])
    path.append((l['latitude'], l['longitude']))
mymap.addpath(path,"#0000FF")
mymap.draw(output)

    

