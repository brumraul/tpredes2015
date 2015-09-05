#! /usr/bin/python
from scapy.all import *
from scapy.utils import rdpcap
from math import log
import sys
import os
import operator

ipssrc = {}
ipsdst = {}

def entropia(ips):
    N = sum(ips.values())
    Ps = [ k/N for k in ips.values() ]
    H = -sum([ p*log(p,2) for p in Ps ])
    return H

def info_simbolo(diccionario, key):
    N = sum(diccionario.values())
    Ps = diccionario.get(key)/N
    H = -(log(Ps,2))
    return H

def prob_simbolo(diccionario, key):
    N = sum(diccionario.values())
    Ps = diccionario.get(key)/N
    return Ps

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        src = pkt[ARP].psrc
        dst = pkt[ARP].pdst

        # If no src is defined return cero add one and set
        ipssrc[src] = ipssrc.get(src, 0.0) + 1.0
        ipsdst[dst] = ipsdst.get(dst, 0.0) + 1.0
	

def informacion(diccionario):
    for simbolo   in diccionario.keys():
	     print "simbolo : %s, Informacion : %f" % (simbolo, info_simbolo(diccionario, simbolo))

def probabilidad(diccionario):
    for simbolo   in diccionario.keys():
	     print "simbolo : %s, Probabilidad : %f" % (simbolo, prob_simbolo(diccionario, simbolo))

def sniff_offline(archivo):
    pkts=rdpcap(archivo);
    for pkt    in pkts:
             arp_monitor_callback(pkt);

if len(sys.argv) < 2:
    #Si no se especifico archivo ejecutamos el sniff online
    sniff(prn=arp_monitor_callback, filter="arp", store=0)
elif not os.path.exists(sys.argv[1]):
    sys.stderr.write('ERROR: no existe el archivo pasado como parametro\n')
else:
    #Si existe el archivo realizamos un sniff offline
    #Tiene que estar filtrado por ARP   
    sniff_offline(sys.argv[1]);
    print "IPs Dst - Informacion: ";
    print informacion(ipsdst)
    print "IPs Src - Informacion: ";
    print informacion(ipssrc)
    print "Entropia Fuente IPs Destino: ";
    print entropia(ipsdst)
    print "Entropia Fuente IPs Origen: ";
    print entropia(ipssrc)
    print "IPs Dst - Probabilidad: ";
    print probabilidad(ipsdst)
    print "IPs Src - Probabilidad: ";
    print probabilidad(ipssrc)

