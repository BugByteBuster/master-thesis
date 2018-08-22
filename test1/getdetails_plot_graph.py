import xlsxwriter
import re
import collections

total_count = []
string5 = ""
count_array15_25 = []
count_array15_65 = []
workbook = xlsxwriter.Workbook('file_xac.xlsx')
worksheet = workbook.add_worksheet()

with open('/home/vidyadhar/xac') as f:
	lines=f.readlines()
	for line in lines:
		if "length of mtus" in line:
			total_count.append(int(line[14:27]))
		#if re.search(r'\bfrequency\b', line):
		if "range15-65"	in line:
			string1 = line[12:-2].split(".")
			string1 = string1[0:-1]
			string1 = map(int, string1)
			#print string1
		if "frequency15-65" in line:
                        string2 = filter(None, line[16:-2].split(" "))
			string2 = string2[0:-1]
			string2 = map(int, string2)
			#print string2
			count_array15_65.append(string2)
		if "range15-25" in line:
                        string3 = line[12:-2].split(".")
                        string3 = string3[0:-1]
			string3 = map(int, string3)
			#print string3
		if "frequency15-25" in line:
			string4 = filter(None, line[16:-2].split(" "))
                        string4 = string4[0:-1]
                        string4 = map(int, string4)
			#print string4
                        count_array15_25.append(string4)
		if re.search(r'\bmain_array\b', line):
			string5 += ', {}'.format(line[12:-2])


string6 = string5.split(",")
string6=string6[1:]
string6 = map(int, string6)
keys_values = collections.Counter(string6)


count_array15_65=[sum(x) for x in zip(*count_array15_65)]
count_array15_25=[sum(x) for x in zip(*count_array15_25)]


print "sum {}".format(sum(count_array15_65))
print "sum {}".format(sum(count_array15_25))
print "sum {}".format(sum(total_count))


row1 = 0
for i in count_array15_65:
	worksheet.write(row1,1, i)
	row1 += 1


row2 = 12
for i in count_array15_25:
	worksheet.write(row2, 1, i)
	row2 += 1



row3 = 25
col5 = 0
col6 = 1
for k,v in keys_values.items():
        worksheet.write(row3, col5, k)
        worksheet.write(row3, col6, v)
        row3 +=1


#worksheet.write('B1', sum1)
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
chart3.set_x_axis({'name': 'absolute packet length'})
chart3.set_y_axis({'name': 'count'})
chart3.set_title({'name': 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart3.add_series({
    'values': '=Sheet1!$B$26:$B$60',
    'categories': '=Sheet1!$A$26:$A$60',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})




worksheet.insert_chart('C1', chart)
worksheet.insert_chart('C13', chart2)
worksheet.insert_chart('C26', chart3)

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


workbook.close()
