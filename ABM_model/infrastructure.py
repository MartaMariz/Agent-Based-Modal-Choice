import csv


class Infrastructure:
    def __init__(self, init_road_area, init_bus_lines, init_railway_lines, init_railway_trips, init_bus_trips):
        self.init_road_area = init_road_area
        self.init_bus_lines = init_bus_lines
        self.init_bus_trips = init_bus_trips
        self.init_railway_lines = init_railway_lines
        self.init_railway_trips = init_railway_trips

    def processMatix(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            time_trip_railway = list(reader)
            time_trip_railway = time_trip_railway[1:]
            
            for i in range(len(time_trip_railway)):
                time_trip_railway[i] = time_trip_railway[i][1:]
                time_trip_railway[i] = [float(val) for val in time_trip_railway[i] if val.strip() ]
        
        return time_trip_railway

    def getTimeTripDistribution(self):
        with open('ABM_model\matrices\\time_trip_distribution.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            time_trip_distribution = list(reader)[0]
            time_trip_distribution = [float(val) for val in time_trip_distribution if val.strip() ]

        return time_trip_distribution

    def getDistanceMatrix(self):
        return self.processMatix('ABM_model\matrices\distances_road.csv')

    def getTravelTimeRailwayMatrix(self):
        return self.processMatix('ABM_model\matrices\\time_trip_railway.csv')

    def getWaitTimeRailway(self,trips_per_line):
        matrix = self.processMatix('ABM_model\matrices\wait_time_railway.csv')
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = matrix[i][j] * self.init_railway_trips / trips_per_line
        return matrix


    def getWaitTimeBus(self,bus_per_route):
        matrix = self.processMatix('ABM_model\matrices\wait_time_bus.csv')
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = matrix[i][j] * self.init_bus_trips / bus_per_route
        return matrix

    def getRoadCapacity(self, road_area):
        matrix = self.processMatix('ABM_model\matrices\\road_capacity.csv')
        for i in range(len(matrix)):
            for j in range(len(matrix[i])):
                matrix[i][j] = matrix[i][j] * road_area / self.init_road_area
        return matrix






