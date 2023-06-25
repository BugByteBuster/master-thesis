import os
import datetime
import sys
import xlsxwriter
import numpy
sys.path.append("/home/ezpedvi/myimports/")
import dpkt
import collections

def process_packet(filename, directory):
    timestamps = []
    mtu = []
    count_tcp = 0
    count_udp = 0
    count_icmp = 0
    
    with open(os.path.join(directory, filename), 'rb') as f:
        print(filename)
        pcap = dpkt.pcap.Reader(f)
        for timestamp, buf in pcap:
            eth = dpkt.sll.SLL(buf)  # since the packets are linux cooked encapsulated
            ip = eth.data
            time = datetime.datetime.fromtimestamp(int(timestamp)).strftime('%H')
            timestamps.append(int(time))
            mtu.append(len(eth))
            if ip.p == 17:
                count_udp += 1
            elif ip.p == 6:
                count_tcp += 1
            elif ip.p == 1:
                count_icmp += 1
    
    return timestamps, mtu, count_tcp, count_udp, count_icmp

def write_data_to_worksheet(worksheet, row, col, data):
    for item in data:
        worksheet.write(row, col, item)
        row += 1

def create_histogram(mtu, bins, range):
    counts, bins = numpy.histogram(mtu, bins=bins, range=range)
    return counts, bins

def create_chart(workbook, sheet, title, data_range):
    chart = workbook.add_chart({'type': 'column'})
    chart.set_x_axis({'name': 'range of packets'})
    chart.set_y_axis({'name': 'count'})
    chart.set_title({
        'name': title,
        'name_font': {'size': 10, 'bold': True, 'italic': True}
    })
    chart.add_series({
        'values': f'={sheet}!$B${data_range[0]}:$B${data_range[1]}',
        'categories': f'={sheet}!$A${data_range[0]}:$A${data_range[1]}',
        'name': 'packet count',
        'data_labels': {'value': True, 'position': 'outside_end'}
    })
    return chart

def process_packets(directory, output_file):
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet()

    row = 0

    for filename in os.listdir(directory):
        if filename.startswith('mtas_sig_35_2_'):
            try:
                timestamps, mtu, count_tcp, count_udp, count_icmp = process_packet(filename, directory)

                row_end = row + len(timestamps)

                write_data_to_worksheet(worksheet, row, 0, timestamps)
                write_data_to_worksheet(worksheet, row, 1, mtu)

                row = row_end

                count_tcp = count_tcp + count_udp + count_icmp

            except ValueError:
                print("Exception")

    counts, bins = create_histogram(mtu, 6, (0, 3000))
    write_data_to_worksheet(worksheet, 12, 1, counts)

    counts2, bins2 = create_histogram(mtu, 10, (1500, 2500))
    write_data_to_worksheet(worksheet, 25, 1, counts2)

    c = collections.Counter(mtu)
    write_data_to_worksheet(worksheet, 36, 0, [item for item, count in c.most_common(10)])
    write_data_to_worksheet(worksheet, 36, 1, [count for item, count in c.most_common(10)])

    counts3, bins3 = create_histogram(mtu, 10, (2100, 2200))
    write_data_to_worksheet(worksheet, 48, 1, counts3)

    counts4, bins4 = create_histogram(mtu, 10, (2100, 2110))
    write_data_to_worksheet(worksheet, 61, 1, counts4)

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
    worksheet.write('A62', 'UDP')
    worksheet.write('A63', 'ICMP')

    worksheet.write('B61', count_tcp)
    worksheet.write('B62', count_udp)
    worksheet.write('B63', count_icmp)

    chart1 = create_chart(workbook, 'Sheet1', 'Analysis of packets with mtu > 1500 (on 35-2 PL-3) for one hour', (1, 6))
    chart2 = create_chart(workbook, 'Sheet1', 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour', (13, 22))
    chart3 = create_chart(workbook, 'Sheet1', 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour', (26, 35))
    chart4 = create_chart(workbook, 'Sheet1', 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour', (37, 46))
    chart5 = create_chart(workbook, 'Sheet1', 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour', (49, 58))
    chart6 = create_chart(workbook, 'Sheet1', 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour', (61, 63))

    worksheet.insert_chart('E1', chart1)
    worksheet.insert_chart('E13', chart2)
    worksheet.insert_chart('E26', chart3)
    worksheet.insert_chart('E37', chart4)
    worksheet.insert_chart('E49', chart5)
    worksheet.insert_chart('E61', chart6)

    workbook.close()
