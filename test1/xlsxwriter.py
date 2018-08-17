import xlsxwriter

total_count = []
array_15_16 = []
array_16_17 = []
array_17_18 = []
array_18_19 = []
array_19_20 = []
array_20_21 = []
array_21_22 = []
array_22_23 = []
array_23_24 = []
array_24_25 = []

workbook = xlsxwriter.Workbook('file.xlsx')
worksheet = workbook.add_worksheet()

worksheet.write('A1', '1500-1600')
worksheet.write('A2', '1600-1700')
worksheet.write('A3', '1700-1800')
worksheet.write('A4', '1800-1900')
worksheet.write('A5', '1900-2000')
worksheet.write('A6', '2000-2100')
worksheet.write('A7', '2100-2200')
worksheet.write('A8', '2200-2300')
worksheet.write('A9', '2300-2400')
worksheet.write('A10', '2400-2500')
worksheet.write('A11', '< 2500')

with open('/home/vidyadhar/output.txt') as f:
	lines=f.readlines()
	for line in lines:
		if "length of timestamps" in line:
#			print line
#			print line[21:27]
			total_count.append(int(line[21:27]))
		if "frequency" in line:
#			print line
			array_15_16.append(int(line[13:17]))
			array_16_17.append(int(line[18:24]))
			array_17_18.append(int(line[27:31]))
			array_18_19.append(int(line[35:38]))
			array_19_20.append(int(line[42:45]))
			array_20_21.append(int(line[48:52]))
			array_21_22.append(int(line[53:62]))
			array_22_23.append(int(line[65]))
			array_23_24.append(int(line[72]))
			array_24_25.append(int(line[79]))
#			print "length : {}".format(int(line[13:17]))
#			print "length : {}".format(int(line[18:24]))
#			print "length : {}".format(int(line[27:31]))
#			print "length : {}".format(int(line[35:38]))
#			print "length : {}".format(int(line[42:45]))
#			print "length : {}".format(int(line[48:52]))
#			print "length : {}".format(int(line[53:62]))
#			print "length : {}".format(int(line[65]))
#			print "length : {}".format(int(line[72]))
#			print "length : {}".format(int(line[79]))
#int(line) if line.is_integer() else int(float(line))
sum1 = sum(array_15_16)
sum2 = sum(array_16_17)
sum3 = sum(array_17_18)
sum4 = sum(array_18_19)
sum5 = sum(array_19_20)
sum6 = sum(array_20_21)
sum7 = sum(array_21_22)
sum8 = sum(array_22_23)
sum9 = sum(array_23_24)
sum10 = sum(array_24_25)

print "array with total packets in each file : {}".format(total_count)
print "length {}".format(len(total_count))
print "total packets received with mtu > 1500 : {}".format(sum(total_count))

worksheet.write('B1', sum1)
worksheet.write('B2', sum2)
worksheet.write('B3', sum3)
worksheet.write('B4', sum4)
worksheet.write('B5', sum5)
worksheet.write('B6', sum6)
worksheet.write('B7', sum7)
worksheet.write('B8', sum8)
worksheet.write('B9', sum9)
worksheet.write('B10', sum10)
worksheet.write('B11', 90)
chart = workbook.add_chart({'type': 'column'})
chart.set_x_axis({'name': 'range of packets'})
chart.set_y_axis({'name': 'count'})
chart.set_title({'name': 'Analysis of packets with mtu > 1500',
		'name_font': {'size': 10, 'bold': True, 'italic':True}})
chart.add_series({
    'values': '=Sheet1!$B$1:$B$11',
    'categories': '=Sheet1!$A$1:$A$11',
    'name': 'packet count',
    'data_labels': {'value': True, 'position': 'outside_end'}
})

worksheet.insert_chart('C1', chart)


workbook.close()
