import numpy as np
import os
import dpkt
import matplotlib.pyplot as plt
import datetime
import collections

def read_pcap_files(directory):
    timestamps = []
    mtu = []

    for filename in os.listdir(directory):
        if filename.startswith('packet'):
            with open(os.path.join(directory, filename)) as f:
                pcap = dpkt.pcap.Reader(f)
            for timestamp, buf in pcap:
                ip = dpkt.ethernet.Ethernet(buf).data
                timestamps.append(datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H'))
                mtu.append(len(dpkt.ethernet.Ethernet(buf)))
    return timestamps, mtu

def plot_timestamp_counts(timestamps):
    counter = collections.Counter(timestamps)
    labels, values = zip(*counter.items())
    indexes = np.arange(len(labels))

    plt.bar(indexes, values)
    plt.xticks(indexes, labels)
    plt.xlabel('Time')
    plt.ylabel('Count')
    plt.show()

def plot_packet_frequency(mtu):
    counts, bins = np.histogram(mtu, bins=10, range=(1500, 6500))

    plt.bar(bins[:-1], counts)
    plt.xlabel('Packet Length')
    plt.ylabel('Frequency')
    plt.show()

def main():
    timestamps, mtu = read_pcap_files('/home/vidyadhar/packets')
    
    print("Length of timestamps: {}".format(len(timestamps)))
    print("Length of mtus: {}".format(len(mtu)))
    
    counter = collections.Counter(timestamps)
    print("Counter: {}".format(counter))
    
    plot_timestamp_counts(timestamps)
    plot_packet_frequency(mtu)

if __name__ == "__main__":
    main()
