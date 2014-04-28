#!/usr/bin/env python

import sys
import re
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'

def find_http_requests(pkts):

	get_requests = []
	http_get = 'GET /'

	for p in pkts:
		if p.haslayer(TCP) and p.haslayer(Raw):
			raw = p.getlayer(Raw).load
			if http_get in raw:
				dstip = p.getlayer(IP).dst
				dport = p.getlayer(TCP).dport
				srcip = p.getlayer(IP).src
				new_raw = p.getlayer(Raw).load
				request = ''
				host = '' 
				for t in re.finditer('(GET) (\S*)', new_raw):
					request = t.group(2)
				for s in re.finditer('(Host:) (\S*)', new_raw):
					host = s.group(2)
				talker = request, srcip, dstip, dport, host
				if talker not in get_requests:
					get_requests.append(talker)

	for url, src, dst, port, host in get_requests:
		print GREEN + '[+] Web traffic from: ' + str(src) + ' to ' + str(dst) + ' on port ' + str(port) + ' to ' + host + ' for ' + url + END

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage is ./parse.py <input pcap file>'
		print 'Example - ./parse.py sample.pcap'
		sys.exit(1)
	pkts = rdpcap(sys.argv[1])
	find_http_requests(pkts)