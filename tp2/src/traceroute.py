#! /usr/bin/python
import argparse
import os
import sys
import scapy.all as scp
import socket
from collections import Counter
import numpy

ICMP_ECHO_REPLY = 0
ICMP_TIME_EXCEEDED = 11

def median(l):
    return numpy.median(numpy.array(l))

class TraceRoute:
    def __init__(self, dst, tries, hops=30): #dst is a domanin name
        self.dst    = dst
        self.tries  = tries
        self.hops   = hops
        pkt = scp.IP(dst=dst) / scp.ICMP()
        ans, unans = scp.sr(pkt, verbose=0)
        self.ip = ans[0][0].dst
        self.hosts = [Counter() for _ in xrange(hops)]
        self.times = [{} for _ in xrange(hops)]

    def distance(self, ttl):
        dst = self.ip
        pkt = scp.IP(dst=dst, ttl=ttl) / scp.ICMP()  
        ans, unans = scp.sr(pkt, verbose=0, timeout=1)
        pos = ttl -1

        if ans:
            rx = ans[0][1]
            tx = ans[0][0]

            if rx.type == ICMP_TIME_EXCEEDED or rx.type == ICMP_ECHO_REPLY:
                self.hosts[pos][rx.src] += 1
                if rx.src not in self.times[pos]:
                    self.times[pos][rx.src] = []
                self.times[pos][rx.src] += [(rx.time - tx.sent_time) * 1000]
                    
        if self.hosts[pos]:
            best = self.hosts[pos].most_common(1)[0][0]
            return (best, median(self.times[pos][best]))
        else:
            return ('*', 0)

    def trace(self):
        print('Traceroute to {}({})'.format(self.dst, self.ip))
        for t in xrange(self.tries):
            print "\n"
            distance = -1
            nodes = []
            for ttl in range(1, self.hops + 1):
                ip, rtt = self.distance(ttl)
                host = '*'
    
                if ip != '*':
                    try:
                        host = socket.gethostbyaddr(ip)[0]
                    except socket.herror:
                        host = ip

                nodes += [{'ip': ip, 'host': host, 'rtt': rtt}]
                print('{} {} ({}) {:.3f} ms'.format(ttl, host, ip, rtt))

                if ip == self.ip:
                    distance = ttl
                    break
        print "\n"
        if distance != -1:
            print('Host reached in {} hops'.format(distance))
        else:
            print('Host not reached in {} hops'.format(self.hops))

        return (distance, nodes)


parser = argparse.ArgumentParser(description="Traceroute to given domain name")
parser.add_argument('-n', '--name', required=True, type=str, help='domain name')
parser.add_argument('-t', '--tries', required=False, type=int, help='number of runs, omit for continuos output')
args = parser.parse_args()

if args.tries:
    t=args.tries
else:
    t=9999

TraceRoute(args.name,t).trace()
