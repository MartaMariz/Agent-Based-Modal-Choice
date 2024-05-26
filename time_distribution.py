import csv

def getTimeProportions():
    total = 0
    total_per_hour = []
    with open('data\IMOB_2017a_AMP.csv', newline='\n', encoding="utf8") as csvfile:
        reader = csv.reader(csvfile, delimiter='\n', quotechar='|')
        reader = list(reader)
        reader = reader[5:29]
        for row in reader:
            row = row[0].split(';')
            total_hour = 0
            for i in range(1,len(row)):
                row[i] = row[i].replace(" ", "")
                if (row[i] == '' or row[i] == '§' or row[i] == 'x'):
                    row[i] = 0
                num = int(row[i])
                total_hour += num
                total += num
            total_per_hour.append(total_hour)
    for i in range(len(total_per_hour)):
        total_per_hour[i] = total_per_hour[i]/total
        total_per_hour[i] = round(total_per_hour[i], 2)


    with open('ABM_model/matrices/traffic_distribution.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)    
        csvwriter.writerow(total_per_hour)




getTimeProportions()


