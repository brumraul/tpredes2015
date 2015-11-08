#! /usr/bin/python
import argparse
import os
import sys
import matplotlib.pyplot as plt
from matplotlib import cm
import numpy as np

def valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

parser = argparse.ArgumentParser(description="Generates a plot from input file")
parser.add_argument('-i', '--input', required=True, type=lambda x: valid_file(parser,x), help='input filename', metavar='FILE')
parser.add_argument('-l', '--line', help='Generates a line graph from input', action="store_true")
parser.add_argument('-b', '--bar', help='Generates a histogram from input', action="store_true")
args = parser.parse_args()
output,ext = os.path.splitext(args.input)

with open(args.input) as file:
    label = []
    rtt = []
    delta = []
    for line in file:
        words = line.split()
        label.append(words[0])
        rtt.append(words[1])
        delta.append(words[2])

if args.bar:
    plt.figure(figsize=(12,6))
    y = [float(i) for i in delta]
    x = [int(i) for i in label]
    plt.bar(x, y, align='center', color='royalblue', label="RTT")
    plt.xticks(x, label)
    plt.xlabel("Hop")
    plt.ylabel('ms')
    plt.savefig(output+"-bar"+"."+"png")

if args.line:
    plt.figure(figsize=(15,5))
    rtt = [float(i) for i in rtt]
    delta = [float(i) for i in delta]
    x = [int(i) for i in label]
    sub1 = plt.subplot(2,1,1)
    sub2 = plt.subplot(2,1,2)
    sub1.set_xticks(x)
    sub2.set_xticks(x)
    sub1.plot(x,rtt,color='red',linewidth=2.5,label="RTT")
    sub2.plot(x,delta,color='green',linewidth=2.5,label="Delta RTT")
    sub1.legend(loc='upper left', frameon=False)
    sub2.legend(loc='upper left', frameon=False)
    sub1.grid()
    sub2.grid()
    plt.savefig(output+"-lines"+"."+"png")

