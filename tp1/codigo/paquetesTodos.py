#! /usr/bin/python
from scapy.all import *
from scapy.utils import rdpcap
from scapy.utils import wrpcap
from math import log
import sys
import os
import operator
import argparse

htypes = {}
offline = False

def entropia(fuente):
    N = sum(fuente.values())
    Ps = [ k/N for k in fuente.values() ]
    H = -sum([ p*log(p,2) for p in Ps ])
    return H

def info_simbolo(diccionario, key):
    N = sum(diccionario.values())
    Ps = diccionario.get(key)/N
    I = -(log(Ps,2))
    return I

def prob_simbolo(diccionario, key):
    N = sum(diccionario.values())
    Ps = diccionario.get(key)/N
    return Ps

def monitor_callback_all(pkt):
    if Ether in pkt:
#        htype = hex(pkt.type)
        if pkt.type == 34525:
            htype = 'IPv6'
        else:
            htype = pkt.payload.name
        # Modelo fuente de informacion hw type
	htypes[htype] = htypes.get(htype, 0.0) + 1.0  

def informacion(diccionario):
    for simbolo in diccionario.keys():
	    print "simbolo : %4s, Informacion : %f" % (simbolo, info_simbolo(diccionario, simbolo))

def probabilidad(diccionario):
    for simbolo in diccionario.keys():
        print "simbolo : %4s, Probabilidad : %f" % (simbolo, prob_simbolo(diccionario, simbolo))

def sniff_offline(archivo):
    pkts=rdpcap(archivo);
    for pkt in pkts:
        monitor_callback_all(pkt);

def valid_file(parser, arg):
    global offline
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        offline = True
        return arg

parser = argparse.ArgumentParser(description='''Network traffic capture tool.''')
parser.add_argument('-t', '--time', required=False, type=int, help='max running time in seconds', default=60)
parser.add_argument('-i', '--input', required=False, type=lambda x: valid_file(parser,x), help='input filename for offline sniff', metavar='FILE')
parser.add_argument('-d', '--dump', required=False, type=str, help='capture packets and dump them to output file', metavar='FILE')
args = parser.parse_args()

print '\n' + "Running %s with parameters: time=%s, input=%s"%(os.path.basename(sys.argv[0]) ,args.time, args.input) + '\n'

if offline:
    #realizamos un sniff offline
    sniff_offline(args.input)
elif not args.dump == None:
    #dump to file
    pkts = sniff(timeout=args.time)
    wrpcap(args.dump,pkts)
    print 'output saved in file {}'.format(args.dump)
    exit(0)
else:
    #ejecutamos el sniff online
    sniff(prn=monitor_callback_all, store=0, timeout=args.time)

print "Entropia Fuente HW Type: %f" % entropia(htypes) + '\n'
print probabilidad(htypes)
print informacion(htypes)



