import os
import datetime
import sys
import xlsxwriter
import numpy
sys.path.append("/home/ezpedvi/myimports/")
import dpkt
import collections
timestamps=[]
mtu=[]

count_tipc = 0
count_ipv6 = 0
count_ip = 0
count_tcp = 0
count_udp = 0
#count_tcp_ipv6 = 0

workbook = xlsxwriter.Workbook('packets_oneHour_mtas-35-2_INM_Ipv6_mtu_2140_case2_20180823.xlsx')
worksheet = workbook.add_worksheet()

for filename in os.listdir('.'):
	if filename.startswith('packet'):
    		print filename
        	try:
			if filename != 'packetinfo0178':
				with open(os.path.join('.', filename)) as f:
        	    			pcap = dpkt.pcap.Reader(f)
        				for timestamp, buf in pcap:
            					eth = dpkt.ethernet.Ethernet(str(buf))
           					time=datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H')
             					timestamps.append(int(time))
        					mtu.append(len(eth))
						ip = eth.data
						if eth.type == 35018: #tipc packets
							count_tipc += 1 
						if eth.type == 34525:	
							count_ipv6 += 1
						if eth.type == dpkt.ethernet.ETH_TYPE_IP:
                                                	count_ip += 1
                                                	if ip.p == 17:
                                                        	count_udp += 1
                                                	elif ip.p == 6:
                                                        	count_tcp += 1	
															
		except ValueError:
			print "exception"

print 'total packets received %s'%(count_tipc + count_ipv6 + count_ip)
print 'number of tipc packets %s'%(count_tipc)
print 'number of ipv6 or ipv6 tcp packets %s'%(count_ipv6)
print 'number of ip packets %s'%(count_ip)
print 'number of tcp_ipv4 packets %s'%(count_tcp)
print 'number of upd_ipv4 packets %s'%(count_udp)
print 'length of mtus %s' %(len(mtu)) #count of total packets received

#these many packets received in this hour
c= collections.Counter(mtu)
print c.most_common(10)

counts, bins = numpy.histogram(mtu, bins=10, range=(1500, 6500))
print "range15-65 {}".format(bins)
print "frequency15-65 {}".format(counts)

counts2, bins2 = numpy.histogram(mtu, bins = 10, range=(1500, 2500))
print "range15-25 {}".format(bins2)
print "frequency15-25 {}".format(counts2)


row1 = 0
for i in counts:
	worksheet.write(row1,1, i)
	row1 += 1

row2 = 12
for i in counts2:
        worksheet.write(row2,1, i)
        row2 += 1


row3 = 25
col = 1
for item, count in c.most_common(10):
        worksheet.write(row3, 0, item)
       	worksheet.write(row3, 1, count)
	row3 += 1





worksheet.write('A1', '1500-2000')
worksheet.write('A2', '2000-2500')
worksheet.write('A3', '2500-3000')
worksheet.write('A4', '3000-3500')
worksheet.write('A5', '3500-4000')
worksheet.write('A6', '4000-4500')
worksheet.write('A7', '4500-5000')
worksheet.write('A8', '5000-5500')
worksheet.write('A9', '5500-6000')
worksheet.write('A10', '6000-6500')

worksheet.write('A13', '1500-1600')
worksheet.write('A14', '1600-1700')
worksheet.write('A15', '1700-1800')
worksheet.write('A16', '1800-1900')
worksheet.write('A17', '1900-2000')
worksheet.write('A18', '2000-2100')
worksheet.write('A19', '2100-2200')
worksheet.write('A20', '2200-2300')
worksheet.write('A21', '2300-2400')
worksheet.write('A22', '2400-2500')

worksheet.write('A37', 'TIPC')
worksheet.write('A38', 'TCP_IPV6')
worksheet.write('A39', 'TCP_IP')
worksheet.write('A40', 'UDP')



worksheet.write('B37', count_tipc)
worksheet.write('B38', count_ipv6)
worksheet.write('B39', count_tcp)
worksheet.write('B40', count_udp)


chart = workbook.add_chart({'type': 'column'})
chart.set_x_axis({'name': 'range of packets'})
chart.set_y_axis({'name': 'count'})
chart.set_title({'name': 'Analysis of packets with mtu > 1500 (on 35-2 PL-3) for one hour',
		'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart.add_series({
    'values': '=Sheet1!$B$1:$B$10',
    'categories': '=Sheet1!$A$1:$A$10',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})

chart2 = workbook.add_chart({'type': 'column'})
chart2.set_x_axis({'name': 'range of packets'})
chart2.set_y_axis({'name': 'count'})
chart2.set_title({'name': 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart2.add_series({
    'values': '=Sheet1!$B$13:$B$22',
    'categories': '=Sheet1!$A$13:$A$22',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})


chart3 = workbook.add_chart({'type': 'column'})
chart3.set_x_axis({'name': 'absolute packet lengths'})
chart3.set_y_axis({'name': 'count'})
chart3.set_title({'name': 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart3.add_series({
    'values': '=Sheet1!$B$26:$B$35',
    'categories': '=Sheet1!$A$26:$A$35',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})





chart4 = workbook.add_chart({'type': 'column'})
chart4.set_x_axis({'name': 'type of packets'})
chart4.set_y_axis({'name': 'count'})
chart4.set_title({'name': 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart4.add_series({
    'values': '=Sheet1!$B$37:$B$40',
    'categories': '=Sheet1!$A$37:$A$40',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})


worksheet.insert_chart('E1', chart)
worksheet.insert_chart('E13', chart2)
worksheet.insert_chart('E25', chart3)
worksheet.insert_chart('E37', chart4)
workbook.close()
