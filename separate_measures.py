"""
The following script reads all the files regarding the measurements and, 
for each location, creates a folder with the same name and inserts inside 
a sequence of .csv files equal to the number of different roads in the locations,
to each road it associates the measurement read and the interval of the measurement itself.
"""
import csv
def read_csv_file(file_name):
    grouped_data = {}
    with open(file_name, 'r') as csv_file:
        reader = csv.reader(csv_file)
        grouping_column = input("Enter the index of the column for grouping: ")
        for row in reader:
            timestamp = row[0]
            column_value = row[int(grouping_column)]
            if(('.' not in column_value or '.0' in column_value) and int(float(column_value)) <= 6000 and timestamp != ""):
                column_value = str(int(float(column_value)))
                if column_value not in grouped_data:
                    grouped_data[column_value] = []
                row.append('30')
                grouped_data[column_value].append(row)
    return grouped_data
def write_csv_file(grouped_data, file_prefix):
    for column_value, rows in grouped_data.items():
        file_name = file_prefix + column_value + ".csv"
        with open(file_name, 'a', newline='') as csv_file:
            writer = csv.writer(csv_file)
            for row in rows:
                writer.writerow(row)
input_file_name = "archive\\Bxl_30min_1303_0606_2021.csv"
output_file_prefix = "archive\\groups\\bruxelles\\"
grouped_data = read_csv_file(input_file_name)
write_csv_file(grouped_data, output_file_prefix)
print("Grouping has been completed, and the data has been written to separate files.")