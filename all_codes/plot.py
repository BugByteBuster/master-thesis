import numpy as np
import os
import dpkt
import matplotlib.pyplot as plt
import datetime
import collections

def read_packets(directory):
    timestamps = []
    mtu = []

    for filename in os.listdir(directory):
        if filename.startswith('packet'):
            print(filename)
            with open(os.path.join(directory, filename)) as f:
                pcap = dpkt.pcap.Reader(f)
                for timestamp, buf in pcap:
                    ip = dpkt.ethernet.Ethernet(buf).data
                    time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H')
                    timestamps.append(time)
                    mtu.append(len(dpkt.ethernet.Ethernet(buf)))
    
    return timestamps, mtu

def plot_histogram(data, bins, range):
    counts, bins = np.histogram(data, bins=bins, range=range)
    print("range {}".format(bins))
    print("frequency {}".format(counts))
    
    labels, values = zip(*collections.Counter(data).items())
    indexes = np.arange(len(labels))

    plt.bar(indexes, values)
    plt.xticks(indexes, labels)
    plt.show()

def plot_bar(timestamps, mtu):
    plt.bar(timestamps, mtu)
    plt.xlabel('time')
    plt.ylabel('count')
    plt.show()

# Read packets
timestamps, mtu = read_packets('/home/ezpedvi/packets')

# Print lengths
print("length of timestamps {}".format(len(timestamps)))
print("length of mtus {}".format(len(mtu)))

# Count packets per hour
print(collections.Counter(timestamps))

# Plot histogram
plot_histogram(mtu, bins=10, range=(1500, 6500))

# Plot bar chart
plot_bar(timestamps, mtu)
