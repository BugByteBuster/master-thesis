import xlsxwriter
import re
import collections

def read_file(filename):
    with open(filename) as f:
        lines = f.readlines()
    return lines

def extract_total_count(lines):
    total_count = []
    for line in lines:
        if "length of mtus" in line:
            total_count.append(int(line[14:27]))
    return total_count

def extract_data(lines, keyword1, keyword2):
    string = ""
    count_array = []
    for line in lines:
        if keyword1 in line:
            string1 = line[12:-2].split(".")
            string1 = string1[0:-1]
            string1 = list(map(int, string1))
        if keyword2 in line:
            string2 = filter(None, line[16:-2].split(" "))
            string2 = string2[0:-1]
            string2 = list(map(int, string2))
            count_array.append(string2)
        if re.search(r'\bmain_array\b', line):
            string += ', {}'.format(line[12:-2])
    return string1, count_array, string

def write_data_to_worksheet(worksheet, data, row):
    for i in data:
        worksheet.write(row, 1, i)
        row += 1

def create_chart(workbook, worksheet, chart_title, chart_values, chart_categories, chart_row):
    chart = workbook.add_chart({'type': 'column'})
    chart.set_x_axis({'name': 'range of packets'})
    chart.set_y_axis({'name': 'count'})
    chart.set_title({'name': chart_title, 'name_font': {'size': 10, 'bold': True, 'italic': True}})
    chart.add_series({'values': chart_values, 'categories': chart_categories, 'name': 'packet count', 'data_labels': {'value': True, 'position': 'outside_end'}})
    worksheet.insert_chart('C{}'.format(chart_row), chart)

def main():
    lines = read_file('/home/vidyadhar/xac')
    total_count = extract_total_count(lines)
    string15_65, count_array15_65, string5 = extract_data(lines, "range15-65", "frequency15-65")
    string15_25, count_array15_25, _ = extract_data(lines, "range15-25", "frequency15-25")
    keys_values = collections.Counter(list(map(int, string5.split(",")[1:])))
    
    count_array15_65 = [sum(x) for x in zip(*count_array15_65)]
    count_array15_25 = [sum(x) for x in zip(*count_array15_25)]
    
    print("sum {}".format(sum(count_array15_65)))
    print("sum {}".format(sum(count_array15_25)))
    print("sum {}".format(sum(total_count)))
    
    workbook = xlsxwriter.Workbook('file_xac.xlsx')
    worksheet = workbook.add_worksheet()
    
    write_data_to_worksheet(worksheet, count_array15_65, 0)
    write_data_to_worksheet(worksheet, count_array15_25, 12)
    
    row3 = 25
    col5 = 0
    col6 = 1
    for k, v in keys_values.items():
        worksheet.write(row3, col5, k)
        worksheet.write(row3, col6, v)
        row3 += 1
    
    create_chart(workbook, worksheet, 'Analysis of packets with mtu > 1500 (on 35-2 PL-3) for one hour',
                 '=Sheet1!$B$1:$B$10', '=Sheet1!$A$1:$A$10', 1)
    create_chart(workbook, worksheet, 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                 '=Sheet1!$B$13:$B$22', '=Sheet1!$A$13:$A$22', 13)
    create_chart(workbook, worksheet, 'Analysis of mtu > 1500 (on 35-2 PL-3 eth0) for one hour',
                 '=Sheet1!$B$26:$B$60', '=Sheet1!$A$26:$A$60', 26)
    
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

if __name__ == "__main__":
    main()
