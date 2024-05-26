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
    with open('.\matrices\\time_trip_distribution.csv', newline='') as csvfile:
        reader = csv.reader(csvfile)
        time_trip_distribution = list(reader)[0]
        time_trip_distribution = [float(val) for val in time_trip_distribution if val.strip() ]

    return time_trip_distribution

def getDistanceMatrix():
    return processMatix('.\matrices\distances_road.csv')

def getTravelTimeRailwayMatrix():
    return processMatix('.\matrices\\time_trip_railway.csv')

def getWaitTimeRailway():
    return processMatix('.\matrices\wait_time_railway.csv')

def getWaitTimeBus():
    return processMatix('.\matrices\wait_time_bus.csv')

def getRoadCapacity():
    return processMatix('.\matrices\\road_capacity.csv')

def getTimeDistribution():
    return getTimeTripDistribution()

