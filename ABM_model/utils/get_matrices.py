import csv

def processMatix(path):
    with open(path, newline='') as csvfile:
        reader = csv.reader(csvfile)
        time_trip_railway = list(reader)
        time_trip_railway = time_trip_railway[1:]
        
        for i in range(len(time_trip_railway)):
            time_trip_railway[i] = time_trip_railway[i][1:]
            time_trip_railway[i] = [float(val) for val in time_trip_railway[i] if val.strip() ]
       
    return time_trip_railway

def getTimeTripDistribution():
    with open('ABM_model\matrices\\time_trip_distribution.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        time_trip_distribution = list(reader)[0]
        time_trip_distribution = [float(val) for val in time_trip_distribution if val.strip() ]

    return time_trip_distribution

def getDistanceMatrix():
    return processMatix('ABM_model\matrices\distances_road.csv')

def getTravelTimeRailwayMatrix():
    return processMatix('ABM_model\matrices\\time_trip_railway.csv')

def getWaitTimeRailway(trips_per_line):
    matrix = processMatix('ABM_model\matrices\wait_time_railway.csv')
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] * 75 / trips_per_line
    return matrix


def getWaitTimeBus(bus_per_route):
    matrix = processMatix('ABM_model\matrices\wait_time_bus.csv')
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            matrix[i][j] = matrix[i][j] * 18.489 / bus_per_route
    return matrix

def getRoadCapacity():
    return processMatix('ABM_model\matrices\\road_capacity.csv')

def getTimeDistribution():
    return getTimeTripDistribution()

