#! /usr/bin/python
from scapy.all import *
from scapy.utils import rdpcap
from math import log
import sys
import os
import operator

htypes = {}

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
        htype = hex(pkt.type)
            
        # Modelo fuente de informacion hw type
	htypes[htype] = htypes.get(htype, 0.0) + 1.0  

def informacion(diccionario):
    for simbolo   in diccionario.keys():
	     print "simbolo : %s, Informacion : %f" % (simbolo, info_simbolo(diccionario, simbolo))

def probabilidad(diccionario):
    for simbolo   in diccionario.keys():
	     print "simbolo : %s, Probabilidad : %f" % (simbolo, prob_simbolo(diccionario, simbolo))

def sniff_offline(archivo):
    pkts=rdpcap(archivo);
    for pkt   in pkts:
             monitor_callback_all(pkt);

if len(sys.argv) < 2:
    #Si no se especifico archivo ejecutamos el sniff online
    sniff(prn=arp_monitor_callback, store=0)
elif not os.path.exists(sys.argv[1]):
    sys.stderr.write('ERROR: no existe el archivo pasado como parametro\n')
else:
    #Si existe el archivo realizamos un sniff offline
    sniff_offline(sys.argv[1]);
    print "Entropia Fuente HW Type: %f" % entropia(htypes)
    print probabilidad(htypes)
    print informacion(htypes)



