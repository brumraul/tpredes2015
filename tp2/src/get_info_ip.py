#!/usr/bin/python
import urllib2

def get_ip_info(ip):
	f = urllib2.urlopen("http://api.hostip.info/get_json.php?ip="+ip+"&position=true")
	data = f.read()
	f.close();
	return data;

def tester():
	print get_ip_info('64.233.160.0');

if __name__ == '__main__':
	tester()
