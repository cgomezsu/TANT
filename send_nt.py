"""
v.e.s.

Traffic-Aware Network Telemetry


MIT License

Copyright (c) 2021 Cesar A. Gomez

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

"""                           


import sys
import time
from scapy.all import *

t = 5                                                   # Emulation time for each flow
traff_type = int(sys.argv[1])                           # Traffic type parsed from the classifier

levels = [0.1e-3, 0.5e-3, 1e-3, 10e-3, 100e-3]

granularity = levels[traff_type]

start = time.time()

while (time.time() - start) <= t:
    send(IP(dst='10.10.0.10')/"TelemetryDat")
    time.sleep(granularity)