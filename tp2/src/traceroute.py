#! /usr/bin/python
import argparse
import os
import sys
import scapy.all as scp
import socket
from collections import Counter
import numpy
import curses

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
            return (best, self.times[pos][best])
        else:
            return ('*', [0])

    def trace(self):
#        print('Traceroute to {}({})'.format(self.dst, self.ip))
        screen.addstr(1,1,'Traceroute to {}({})'.format(self.dst, self.ip))
        screen.addstr(3,1,'TTL',curses.A_BOLD)
        screen.addstr(3,5,'HOST',curses.A_BOLD)
        screen.addstr(3,52,'IP',curses.A_BOLD)
        screen.addstr(3,68,'RTT',curses.A_BOLD)
        
        for t in xrange(self.tries):
            distance = -1
            nodes = []
            for ttl in range(1, self.hops + 1):
                ip, rtt_list = self.distance(ttl)
                host = '*'
    
                if ip != '*':
                    try:
                        host = socket.gethostbyaddr(ip)[0]
                    except socket.herror:
                        host = ip

                rtt = median(rtt_list)
                nodes += [{'ip': ip, 'host': host, 'rtt': rtt}]
#                print('{} {} ({}) {:.3f} ms'.format(ttl, host, ip, rtt))
                screen.addstr(ttl+3,1,'{}'.format(ttl))
                screen.addstr(ttl+3,5,host)
                screen.addstr(ttl+3,52,ip)
                screen.addstr(ttl+3,68,'{:.3f} ms'.format(rtt))
                screen.refresh()

                if ip == self.ip:
                    distance = ttl
                    break

        if distance != -1:
            screen.addstr(distance+5,1,'Host reached in {} hops'.format(distance))
        else:
            screen.addstr(distance+5,1,'Host not reached in {} hops'.format(self.hops))
        screen.refresh
        return (distance, nodes)

    def trace_stat(self):
        screen.addstr(1,1,'Traceroute to {}({})'.format(self.dst, self.ip))
        screen.addstr(3,1,'TTL',curses.A_BOLD)
        screen.addstr(3,6,'IP',curses.A_BOLD)
        screen.addstr(3,23,'RTT',curses.A_BOLD)
        screen.addstr(3,35,'E(RTT)',curses.A_BOLD)
        screen.addstr(3,47,'S(RTT)',curses.A_BOLD)
        screen.addstr(3,59,'D(RTT)',curses.A_BOLD)

        for t in xrange(self.tries):
            distance = -1
            nodes = []
            rtt_ant = 0
            for ttl in range(1, self.hops + 1):
                ip, rtt_list = self.distance(ttl)
                host = '*'
    
                if ip != '*':
                    try:
                        host = socket.gethostbyaddr(ip)[0]
                    except socket.herror:
                        host = ip

                rtt = median(rtt_list)
                mean = numpy.mean(rtt_list)
                std = numpy.std(rtt_list)
                delta = mean - rtt_ant
                rtt_ant = mean
                
                nodes += [{'ip': ip, 'rtt': rtt, 'mean': mean, 'std':std}]
                screen.addstr(ttl+3,1,'{}'.format(ttl))
                screen.addstr(ttl+3,6,ip)
                screen.addstr(ttl+3,23,'{:.3f} ms'.format(rtt))
                screen.addstr(ttl+3,35,'{:.3f} ms'.format(mean))
                screen.addstr(ttl+3,47,'{:.3f} ms'.format(std))
                screen.addstr(ttl+3,59,'{:.3f} ms'.format(delta))
                screen.refresh()

                if ip == self.ip:
                    distance = ttl
                    break


parser = argparse.ArgumentParser(description="Traceroute to given domain name")
group = parser.add_mutually_exclusive_group(required=True)
group.add_argument('-t', '--trace', action="store_true", help="run normal traceroute")
group.add_argument('-s', '--stat', action="store_true", help="run traceroute with statistics")
parser.add_argument('-d', '--dom', required=True, type=str, help='domain name')
parser.add_argument('-r', '--runs', required=False, type=int, help='number of runs, omit for continuos output')
args = parser.parse_args()

if args.runs:
    t=args.runs
else:
    t=9999

try:
    screen = curses.initscr()
    screen.border(0)
    route = TraceRoute(args.dom,t)
    
    if args.trace:
        route.trace()

    if args.stat:
        route.trace_stat()

    screen.getch()  

finally:
    curses.endwin()
