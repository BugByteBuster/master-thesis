import os
import sys
sys.path.append("/home/ezpedvi/myimports/")
import dpkt
import datetime

timestamps = []
mtu = []

count_ipv6 = 0
count_ipv4 = 0
count_tipc = 0
count_sctp = 0
count_tcp = 0
count_udp = 0
count_attribute_errors = 0

for filename in os.listdir('/home/ezpedvi/packets_sctp'):
        if filename.startswith('sctp') and filename != "packetinfo0078":
                print filename
                with open(os.path.join('/home/ezpedvi/packets_sctp', filename)) as f:
                        pcap = dpkt.pcap.Reader(f)
                        for timestamp, buf in pcap:
                                link_eth = dpkt.ethernet.Ethernet(str(buf))
                                if link_eth.type != 35018 and link_eth.type != 34525 and link_eth.type != 2048:
                                        print link_eth.type
                                if link_eth.type == 35018:
                                        count_tipc += 1
                                if link_eth.type == 34525:
                                        count_ipv6 += 1
                                if link_eth.type == 2048:
                                        count_ipv4 += 1
                                        #net_layer = link_eth.data
                                        #print net_layer.p, len(link_eth)
                                network_layer = link_eth.data
                                try:
                                        transport_layer = network_layer.data
                                        if transport_layer.p == 132:
                                                if len(transport_layer) >= 1500:
                                                        print len(transport_layer)
                                                count_sctp += 1
                                        if transport_layer.p == 6:
                                                count_tcp += 1
                                        if transport_layer.p == 17:
                                                count_udp += 1
                                        if transport_layer.p != 132 and transport_layer.p != 6 and transport_layer.p != 17:
                                                print transport_layer.p
                                                print "********************************", len(transport_layer)
                                except AttributeError:
                                        count_attribute_errors += 1
                                        pass
                        print "attribute_errors __   _ _ _ ", count_attribute_errors
                        print "count_tipc: %s, count_sctp= %s, count_tcp=%s, count_udp=%s"%(count_tipc, count_sctp, count_tcp, count_udp)
                        print "total packets: %s"%(count_tipc+count_sctp+count_tcp+count_udp)
                        print "total packets count: %s"%(count_ipv6 + count_ipv4 + count_tipc)
                        print "count_ipv4:%s, count_ipv6:%s, count_tipc:%s"%(count_ipv4, count_ipv6, count_tipc)
print "total packets count: %s"%(count_ipv6 + count_ipv4 + count_tipc)
print "count_ipv4:%s, count_ipv6:%s, count_tipc:%s"%(count_ipv4, count_ipv6, count_tipc)
print count_tipc, count_sctp, count_tcp, count_udp
