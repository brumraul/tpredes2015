#!/usr/bin/python
import urllib2
import argparse

def get_ip_info(ip):
	f = urllib2.urlopen("http://api.hostip.info/get_json.php?ip="+ip+"&position=true")
	data = f.read()
	f.close();
	return data;

def tester():
	print get_ip_info('64.233.160.0');

parser = argparse.ArgumentParser(description="Get ip information")
parser.add_argument('-i', '--ip', required=True, type=str, help='ip address')
args = parser.parse_args()

print get_ip_info(args.ip)

