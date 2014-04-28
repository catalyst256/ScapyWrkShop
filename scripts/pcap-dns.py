#!/usr/bin/env python

# by @catalyst256
import sys
import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
from scapy.all import *

# Add some colouring for printing packets later
YELLOW = '\033[93m'
GREEN = '\033[92m'
END = '\033[0m'
RED = '\033[91m'

def find_dns(pkts):
	for p in pkts:
		if p.haslayer(DNSQR) and p.haslayer(DNSRR):
			rrname = p.getlayer(DNSRR).rrname
			ancount = p.getlayer(DNS).ancount
			rttl = p.getlayer(DNSRR).ttl
			rdata = p.getlayer(DNSRR).rdata
			data = rrname, ancount, rttl, rdata
			if ancount > 4:
				print RED + '[-] DNS Query for: ' + rrname + ' / TTL: ' + str(rttl) + ' / Returned IP: ' + rdata + ' / Number of records: ' + str(ancount) + END
			else:
				print YELLOW + '[-] DNS Query for: ' + rrname + ' / TTL: ' + str(rttl) + ' / Returned IP: ' + rdata + ' / Number of records: ' + str(ancount) + END

if __name__ == '__main__':
	if len(sys.argv) != 2:
		print 'Usage is ./pcap-dns.py <input pcap file>'
		print 'Example - ./pcap-dns.py sample.pcap'
		sys.exit(1)

	pkts = rdpcap(sys.argv[1])
	dns_records = []
	print GREEN + '[+] Initial DNS Dump....' + END
	find_dns(pkts)
