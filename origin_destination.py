import csv

def getFreguesiaProportion():
    total = 0
    population = []
    with open('data/populacao15+_freguesia.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        reader = list(reader)
        reader = reader[10:]
        for row in reader:

            total += int(row[2])
            population.append(int(row[2]))

    for i in range(len(population)):
        population[i] = population[i]/total

    return population

def getIntermunicipalOriginDestination():
    intramunicipal = []
    with open('data/origem_destino_inter.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';', quotechar='|')
        reader = list(reader)
        intra_index = reader[1].index("Gondomar")
        values = reader[2] 
        intra = values[intra_index]
        intra_inter = values[-2]
        intra = intra.replace(' ', '')
        intra_inter = intra_inter.replace(' ', '')
        percentage_intra = int(intra)/int(intra_inter)

        for num in range(len(values) - 2):
            if len(values[num]) <3:
                continue
            if num == intra_index:
                continue

            trips = values[num].replace(' ', '')


            if int(trips) > 5500:
                intramunicipal.append(int(trips))
        total = sum(intramunicipal)
        for i in range(len(intramunicipal)):
            intramunicipal[i] = intramunicipal[i]/total * (1-percentage_intra)
    

        

    return intramunicipal, percentage_intra

def total(matrix):
    total = 0
    for i in range(len(matrix)):
        total += sum(matrix[i])
    print(total)



def buildMatrice():
    freguesia = getFreguesiaProportion()
    intermunicipal, percentage_intra = getIntermunicipalOriginDestination()

    #for i in range(len(freguesia)):
     #   freguesia[i] = freguesia[i] * percentage_intra

    intra_matrix = []
    for i in range(len(freguesia)):
        intra_matrix.append([])
        for j in range(len(freguesia)):
            intra_matrix[i].append(freguesia[i]*freguesia[j])
    

    intra_inter_matrix = []
    for i in range(len(freguesia)):
        intra_inter_matrix.append([])
        for j in range(len(intermunicipal)):
            intra_inter_matrix[i].append(freguesia[i]*intermunicipal[j])
 

    inter_intra_matrix = []
    for i in range(len(intermunicipal)):
        inter_intra_matrix.append([])
        for j in range(len(freguesia)):
            inter_intra_matrix[i].append(intermunicipal[i]*freguesia[j])
    


    total_matrix = []
    for i in range(len(freguesia)):
        total_matrix.append(intra_matrix[i] + intra_inter_matrix[i])

    rest = [0]*len(intermunicipal)
    for i in range(len(intermunicipal)):
        total_matrix.append(inter_intra_matrix[i] + rest)

    
    for i in range(len(total_matrix)):
        total_matrix[i] = [x/(1 + 2*(1-percentage_intra)) for x in total_matrix[i]]

    print(len(total_matrix))
    print(len(total_matrix[0]))
    print("Total matrix", total(total_matrix))
    
    with open('matrices/origin_destination.csv', 'w') as csvfile:
        csvwriter = csv.writer(csvfile)    
        csvwriter.writerows(total_matrix)

      
    return total_matrix

buildMatrice()