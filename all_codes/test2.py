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

count_tcp = 0
count_udp = 0
count_icmp = 0
workbook = xlsxwriter.Workbook('mtas_sig_35_2.xlsx')
worksheet = workbook.add_worksheet()

for filename in os.listdir('/home/ezpedvi/packets_oneHour_mtas-35-2_INM_Ipv6_mtu_2140_case2_External_VIP_mtasSig_20180828'):
	if filename.startswith('mtas_sig_35_2_'):
        	try:
			with open(os.path.join('/home/ezpedvi/packets_oneHour_mtas-35-2_INM_Ipv6_mtu_2140_case2_External_VIP_mtasSig_20180828', filename), 'rb') as f:
				print filename
				pcap = dpkt.pcap.Reader(f)
        			for timestamp, buf in pcap:
            				eth = dpkt.sll.SLL(buf) # since the packets are linux cooked encapsulated
           				ip = eth.data
					time=datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H')
             				timestamps.append(int(time))
        				mtu.append(len(eth))
					#print eth.type	
					if ip.p == 17:
						count_udp += 1
                                        elif ip.p == 6:
                                             	count_tcp += 1	
					elif ip.p == 1:
						count_icmp += 1
		except ValueError:
			print "exception"

print 'total packets received %s'%(count_tcp + count_udp + count_icmp)
print 'number of tcp packets %s'%(count_tcp)
print 'number of udp packets %s'%(count_udp)
print 'number of icmp packets %s'%(count_icmp)
print 'length of mtus %s' %(len(mtu)) #count of total packets received

#these many packets received in this hour
c = collections.Counter(mtu)
print c.most_common(100)

counts, bins = numpy.histogram(mtu, bins=6, range=(0, 3000))
print "range0-3000 {}".format(bins)
print "frequency0-3000 {}".format(counts)

counts2, bins2 = numpy.histogram(mtu, bins = 10, range=(1500,2500))
print "range1500-2500 {}".format(bins2)
print "frequency1500-2500 {}".format(counts2)

counts3, bins3 = numpy.histogram(mtu, bins = 10, range=(2100,2200))
print "range2100-2200 {}".format(bins3)
print "frequency2100-2200 {}".format(counts3)


counts4, bins4 = numpy.histogram(mtu, bins = 10, range=(2100,2110))
print "range2100-2110 {}".format(bins4)
print "frequency2100-2110 {}".format(counts4)


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


row4 = 36
for i in counts3:
	worksheet.write(row4, 1, i)
	row4 += 1

row5 = 48
for i in counts4:
        worksheet.write(row5, 1, i)
        row5 += 1

worksheet.write('A1', '0-500')
worksheet.write('A2', '500-1000')
worksheet.write('A3', '1000-1500')
worksheet.write('A4', '1500-2000')
worksheet.write('A5', '2000-2500')
worksheet.write('A6', '2500-3000')

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

worksheet.write('A37', '2100-2110')
worksheet.write('A38', '2110-2120')
worksheet.write('A39', '2120-2130')
worksheet.write('A40', '2130-2140')
worksheet.write('A41', '2140-2150')
worksheet.write('A42', '2150-2160')
worksheet.write('A43', '2160-2170')
worksheet.write('A44', '2170-2180')
worksheet.write('A45', '2180-2190')
worksheet.write('A46', '2190-2200')



worksheet.write('A49', '2100')
worksheet.write('A50', '2101')
worksheet.write('A51', '2102')
worksheet.write('A52', '2103')
worksheet.write('A53', '2104')
worksheet.write('A54', '2105')
worksheet.write('A55', '2106')
worksheet.write('A56', '2107')
worksheet.write('A57', '2108')
worksheet.write('A58', '2109')


worksheet.write('A61', 'TCP')
worksheet.write('A62','UDP')
worksheet.write('A63', 'ICMP')


worksheet.write('B61', count_tcp)
worksheet.write('B62', count_udp)
worksheet.write('B63', count_icmp)


chart = workbook.add_chart({'type': 'column'})
chart.set_x_axis({'name': 'range of packets'})
chart.set_y_axis({'name': 'count'})
chart.set_title({'name': 'Analysis of packets with mtu > 1500 (on 35-2 PL-3) for one hour',
		'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart.add_series({
    'values': '=Sheet1!$B$1:$B$6',
    'categories': '=Sheet1!$A$1:$A$6',
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
    'values': '=Sheet1!$B$37:$B$46',
    'categories': '=Sheet1!$A$37:$A$46',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})


chart5 = workbook.add_chart({'type': 'column'})
chart5.set_x_axis({'name': 'type of packets'})
chart5.set_y_axis({'name': 'count'})
chart5.set_title({'name': 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart5.add_series({
    'values': '=Sheet1!$B$49:$B$58',
    'categories': '=Sheet1!$A$49:$A$58',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})



chart6 = workbook.add_chart({'type': 'column'})
chart6.set_x_axis({'name': 'type of packets'})
chart6.set_y_axis({'name': 'count'})
chart6.set_title({'name': 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart6.add_series({
    'values': '=Sheet1!$B$61:$B$63',
    'categories': '=Sheet1!$A$61:$A$63',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})



worksheet.insert_chart('E1', chart)
worksheet.insert_chart('E13', chart2)
worksheet.insert_chart('E25', chart3)
worksheet.insert_chart('E37', chart4)
worksheet.insert_chart('E49', chart5)
worksheet.insert_chart('E61', chart6)



workbook.close()
