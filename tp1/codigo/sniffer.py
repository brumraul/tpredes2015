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
ipssrc = {}
ipsdst = {}
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
	htypes[htype] = htypes.get(htype, 0.0) + 1.0

def monitor_callback_arp(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        src = pkt[ARP].psrc
        dst = pkt[ARP].pdst
        ipssrc[src] = ipssrc.get(src, 0.0) + 1.0
        ipsdst[dst] = ipsdst.get(dst, 0.0) + 1.0

def informacion(diccionario):
    for simbolo in diccionario.keys():
	    return "simbolo : %4s, Informacion : %f" % (simbolo, info_simbolo(diccionario, simbolo))

def probabilidad(diccionario):
    for simbolo in diccionario.keys():
        return "simbolo : %4s, Probabilidad : %f" % (simbolo, prob_simbolo(diccionario, simbolo))

def valid_file(parser, arg):
    global offline
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        offline = True
        return arg

def check_root():
    if os.getuid() != 0:
        raise RuntimeError("You need to run this script with root privileges!")


parser = argparse.ArgumentParser(description='''Network traffic capture tool.''')
parser.add_argument('-t', '--time', required=False, type=int, help='max running time in seconds', default=60)
parser.add_argument('-i', '--input', required=False, type=lambda x: valid_file(parser,x), help='input filename for offline sniff', metavar='FILE')
parser.add_argument('-d', '--dump', required=False, type=str, help='capture packets and dump them to output file', metavar='FILE')
parser.add_argument('-n', '--nodes', help='filter ARP packets by node', action="store_true")
args = parser.parse_args()

#check we are running as root for online capture
if not offline or not args.dump == None:
    check_root()

print '\n' + "Running %s with parameters: time=%s, input=%s, nodes=%s"%(os.path.basename(sys.argv[0]) ,args.time, args.input, args.nodes) + '\n'

if not args.dump == None:
    #dump to file & exit
    pkts = sniff(timeout=args.time)
    wrpcap(args.dump,pkts)
    print 'output saved in file {}'.format(args.dump)
    exit(0)

if args.nodes:
    if offline:
        #realizamos un sniff offline filtrando por nodos
        pkts=rdpcap(args.input)
        for pkt in pkts:
            monitor_callback_arp(pkt)
    else:
        #realizamos un sniff online filtrando por nodes
        sniff(prn=monitor_callback_arp, store=0, timeout=args.time, filter='arp')

    print "Entropia Fuente IPs Dst: %f" % entropia(ipsdst)
    print "Entropia Fuente IPs Src: %f" % entropia(ipssrc) + '\n'    
    print "IPs Dst - Informacion:"
    print informacion(ipsdst)
    print "IPs Src - Informacion:"
    print informacion(ipssrc) + '\n'
    print "IPs Dst - Probabilidad:" 
    print probabilidad(ipsdst)
    print "IPs Src - Probabilidad:"
    print probabilidad(ipssrc)
    exit(0)

if offline:
    #realizamos un sniff offline
        pkts=rdpcap(args.input)
        for pkt in pkts:
            monitor_callback_all(pkt)
else:
    #ejecutamos el sniff online
    sniff(prn=monitor_callback_all, store=0, timeout=args.time)

print "Entropia Fuente HW Type: %f" % entropia(htypes) + '\n'
print probabilidad(htypes)
print informacion(htypes)



