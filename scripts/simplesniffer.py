#!/usr/bin/env python

import sys
from scapy.all import *

iface = sys.argv[1]

pkts = sniff(iface=iface, filter=sys.argv[2], prn=lambda x: x.summary())