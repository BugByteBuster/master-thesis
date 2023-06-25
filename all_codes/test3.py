import os
import datetime
import sys
import xlsxwriter
import numpy as np
import dpkt
import collections


def read_pcap_files(directory):
    timestamps = []
    mtu = []

    count_tipc = 0
    count_ipv6 = 0
    count_ip = 0
    count_tcp = 0
    count_udp = 0

    for filename in os.listdir(directory):
        if filename.startswith("packet"):
            print(filename)
            try:
                if filename != "packetinfo0178":
                    with open(os.path.join(directory, filename)) as f:
                        pcap = dpkt.pcap.Reader(f)
                        for timestamp, buf in pcap:
                            eth = dpkt.ethernet.Ethernet(str(buf))
                            time = datetime.datetime.fromtimestamp(
                                int(timestamp)
                            ).strftime("%H")
                            timestamps.append(int(time))
                            ip = eth.data
                            mtu.append(len(ip))
                            if eth.type == 35018:  # tipc packets
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
                print("exception")

    return timestamps, mtu, count_tipc, count_ipv6, count_ip, count_tcp, count_udp


def write_data_to_worksheet(worksheet, row, col, data):
    for item in data:
        worksheet.write(row, col, item)
        row += 1


def create_histogram(data, bins, range):
    counts, bins = np.histogram(data, bins=bins, range=range)
    return counts, bins


def create_chart(workbook, sheet_name, title, data_range):
    chart = workbook.add_chart({"type": "column"})
    chart.set_x_axis({"name": "range of packets"})
    chart.set_y_axis({"name": "count"})
    chart.set_title(
        {"name": title, "name_font": {"size": 10, "bold": True, "italic": True}}
    )
    chart.add_series(
        {
            "values": f"={sheet_name}!$B${data_range[0]}:$B${data_range[1]}",
            "categories": f"={sheet_name}!$A${data_range[0]}:$A${data_range[1]}",
            "name": "packet count",
            "data_labels": {"value": True, "position": "outside_end"},
        }
    )
    return chart


directory = "/home/ezpedvi/packets_oneHour_mtas-35-2_INM_Ipv6_mtu_2140_case2_20180823"
(
    timestamps,
    mtu,
    count_tipc,
    count_ipv6,
    count_ip,
    count_tcp,
    count_udp,
) = read_pcap_files(directory)

workbook = xlsxwriter.Workbook(
    "packets_oneHour_mtas-35-2_INM_Ipv6_mtu_2140_case2_20180823.xlsx"
)
worksheet = workbook.add_worksheet()

counts, bins = create_histogram(mtu, 10, (1500, 6500))
write_data_to_worksheet(worksheet, 0, 1, counts)

counts2, bins2 = create_histogram(mtu, 10, (1500, 2500))
write_data_to_worksheet(worksheet, 12, 1, counts2)

c = collections.Counter(mtu)
write_data_to_worksheet(worksheet, 25, 0, [item for item, count in c.most_common(10)])
write_data_to_worksheet(worksheet, 25, 1, [count for item, count in c.most_common(10)])

worksheet.write("A1", "1500-2000")
worksheet.write("A2", "2000-2500")
worksheet.write("A3", "2500-3000")
worksheet.write("A4", "3000-3500")
worksheet.write("A5", "3500-4000")
worksheet.write("A6", "4000-4500")
worksheet.write("A7", "4500-5000")
worksheet.write("A8", "5000-5500")
worksheet.write("A9", "5500-6000")
worksheet.write("A10", "6000-6500")

worksheet.write("A13", "1500-1600")
worksheet.write("A14", "1600-1700")
worksheet.write("A15", "1700-1800")
worksheet.write("A16", "1800-1900")
worksheet.write("A17", "1900-2000")
worksheet.write("A18", "2000-2100")
worksheet.write("A19", "2100-2200")
worksheet.write("A20", "2200-2300")
worksheet.write("A21", "2300-2400")
worksheet.write("A22", "2400-2500")

worksheet.write("A37", "TIPC")
worksheet.write("A38", "TCP_IPV6")
worksheet.write("A39", "TCP_IP")
worksheet.write("A40", "UDP")

worksheet.write("B37", count_tipc)
worksheet.write("B38", count_ipv6)
worksheet.write("B39", count_tcp)
worksheet.write("B40", count_udp)

chart1 = create_chart(
    workbook,
    "Sheet1",
    "Analysis of packets with mtu > 1500 (on 35-2 PL-3) for one hour",
    (1, 10),
)
chart2 = create_chart(
    workbook,
    "Sheet1",
    "Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour",
    (13, 22),
)
chart3 = create_chart(
    workbook,
    "Sheet1",
    "Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour",
    (26, 35),
)
chart4 = create_chart(
    workbook,
    "Sheet1",
    "Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour",
    (37, 40),
)

worksheet.insert_chart("E1", chart1)
worksheet.insert_chart("E13", chart2)
worksheet.insert_chart("E25", chart3)
worksheet.insert_chart("E37", chart4)

workbook.close()
