import numpy
import os
import dpkt
import matplotlib.pyplot as plt
import datetime
import collections

timestamps=[]
mtu=[]

for filename in os.listdir('/home/vidyadhar/packets'):
   if filename.startswith('packet'):
    print filename
        with open(os.path.join('/home/vidyadhar/packets', filename)) as f:
            pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            ip = dpkt.ethernet.Ethernet(buf).data
        #tcp = ip.data
           time=datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H')
             timestamps.append(time)
        mtu.append(len(dpkt.ethernet.Ethernet(buf)))
print "length of timestamps {}".format(len(timestamps))
print "lenght of mtus{}".format(len(mtu)) #count of total packets received

#print mtu (print length of all the received packets)
#these many packets received in this hour
print collections.Counter(timestamps)
#print counter

#frequency of packets with length greater than 1500 and range between 1500 - 6500
counts, bins = numpy.histogram(mtu, bins=10, range=(1500, 6500))
print "range {}".format(bins)
print "frequency {}".format(counts)

labels, values = zip(*collections.Counter(timestamps).items())
indexes = numpy.arange(len(labels))
width=1

#plt.bar(indexes, values, width)
plt.bar(indexes, values)
#plt.xticks(indexes+width*0.5, labels)
plt.xticks(indexes, labels)
plt.show()



'''
#print timestamps
plt.bar(timestamps,len(mtu))
plt.xlabel('time')
plt.ylabel('count')
plt.show()
plt.savefig('plot.png')
'''
