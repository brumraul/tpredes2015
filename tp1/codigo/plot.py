#! /usr/bin/python
import argparse
import os
import sys
import matplotlib.pyplot as plt
import numpy as np

def valid_file(parser, arg):
    if not os.path.isfile(arg):
        parser.error("The file %s does not exist!" % arg)
    else:
        return arg

parser = argparse.ArgumentParser(description="Generates a plot from input file")
parser.add_argument('-i', '--input', required=True, type=lambda x: valid_file(parser,x), help='input filename', metavar='FILE')
parser.add_argument('-p', '--pie', help='Generates a pie chart from input', action="store_true")
parser.add_argument('-b', '--bar', help='Generates a histogram from input', action="store_true")
args = parser.parse_args()
output,ext = os.path.splitext(args.input)


with open(args.input) as file:
    label = []
    info = []
    freq = []
    for line in file:
        words = line.split()
        if words[0] == "entropy":
            entropy = float(words[1])
            barXLabel = words[2]
        else:        
            label.append(words[0])
            info.append(words[1])
            freq.append(words[2])

if args.pie:
    plt.clf()
#    plt.pie(freq, labels=label)
    plt.pie(freq)
    plt.legend(loc=(0,0),labels=label)
    plt.savefig(output+"-pie"+"."+"png")

if args.bar:
    r = 0
    b = 0.1
    if barXLabel == "Ip":
        r=45
        b=0.25
    plt.clf()
    info = [float(i) for i in info]
    width = 0.5
    x = np.arange(len(label))
    plt.bar(x, info, width, align='center', color='royalblue', label=label)
    plt.xticks(x, label, rotation=r)
    plt.xlabel(barXLabel)
    plt.ylabel('Informacion')
    plt.plot([0 - width / 2.0, x[-1] + width / 2.0], [entropy, entropy], color='lime', lw=2)
    plt.gcf().subplots_adjust(bottom=b)
    plt.savefig(output+"-bar"+"."+"png")            
