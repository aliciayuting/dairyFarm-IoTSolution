import csv
import time

result = []

columns = [
    'Activity(steps/hr)',
    'ActivityDeviation(%)',
    'Yield(gr)',
    'YieldDeviation(%)',
    'Fat(%)',
    'FatDeviation(%)',
    'Protein(%)',
    'ProteinDeviation(%)',
    'Lactose(%)',
    'LactoseDeviation(%)',
    'Conductivity',
    'ConductivityDeviation(%)',
    'SCC (*1000/ml)',
    'Blood(%)',
    'ProductionRate(gr/hr)']
# with open('./record_data_large.csv', mode='r') as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     line_count = 0

#     for row in csv_reader:

#         if line_count < 1:
#             result.append(row)
#         elif int(row[2]) < 20 or (int(row[2]) > 4990 and int(row[2]) < 5010):
#             result.append(row)
#         line_count += 1

# with open('./test_dairy_data.csv', mode='w') as dairy_data:
#     dairywriter = csv.writer(dairy_data, delimiter=',')
#     dairywriter.writerows(result)


# Check saving result
with open('./test_dairy_data.csv', mode='r') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    filter = []
    row = csv_file.readline()

    for row in csv_reader:
        # while row:
        row = csv_file.readline()
        print(row)

        if line_count == 0:
            print(row)
            filter = [i for i in range(len(row)) if row[i] in columns]
        line_count += 1
        print([int(row[index]) for index in filter])

        # time.sleep(2)
        # print(row)
    print(line_count)
