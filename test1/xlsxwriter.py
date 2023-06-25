import xlsxwriter

def read_file():
    total_count = []
    arrays = [[] for _ in range(10)]

    with open('/home/vidyadhar/output.txt') as f:
        lines = f.readlines()
        for line in lines:
            if "length of timestamps" in line:
                total_count.append(int(line[21:27]))
            if "frequency" in line:
                for i in range(10):
                    start_index = 13 + (i * 6)
                    end_index = start_index + 4
                    arrays[i].append(int(line[start_index:end_index]))

    return total_count, arrays


def write_data_to_worksheet(worksheet, total_count, sums):
    ranges = ['1500-1600', '1600-1700', '1700-1800', '1800-1900', '1900-2000',
              '2000-2100', '2100-2200', '2200-2300', '2300-2400', '2400-2500', '< 2500']

    for i, range_val in enumerate(ranges):
        worksheet.write(i, 0, range_val)

    for i, sum_val in enumerate(sums):
        worksheet.write(i, 1, sum_val)

    worksheet.write(10, 1, 90)


def create_chart(workbook, worksheet):
    chart = workbook.add_chart({'type': 'column'})
    chart.set_x_axis({'name': 'range of packets'})
    chart.set_y_axis({'name': 'count'})
    chart.set_title({'name': 'Analysis of packets with mtu > 1500',
                     'name_font': {'size': 10, 'bold': True, 'italic': True}})

    chart.add_series({
        'values': '=Sheet1!$B$1:$B$11',
        'categories': '=Sheet1!$A$1:$A$11',
        'name': 'packet count',
        'data_labels': {'value': True, 'position': 'outside_end'}
    })

    worksheet.insert_chart('C1', chart)


def main():
    total_count, arrays = read_file()

    sums = [sum(arr) for arr in arrays]

    workbook = xlsxwriter.Workbook('file.xlsx')
    worksheet = workbook.add_worksheet()

    write_data_to_worksheet(worksheet, total_count, sums)
    create_chart(workbook, worksheet)

    workbook.close()

    print("array with total packets in each file: {}".format(total_count))
    print("length: {}".format(len(total_count)))
    print("total packets received with mtu > 1500: {}".format(sum(total_count)))


if __name__ == "__main__":
    main()
