import csv


class Infrastructure:
    def __init__(self, init_road_area, init_bus_lines, init_railway_lines, init_railway_trips, init_bus_trips, ticket_cost, car_cost_km, init_bus_access = 0.5, railway_access = 0.3):
        self.__init_road_area = init_road_area
        self.__init_bus_lines = init_bus_lines
        self.__init_bus_trips = init_bus_trips
        self.__init_railway_lines = init_railway_lines
        self.__init_railway_trips = init_railway_trips
        self.__car_cost = car_cost_km
        self.__ticket_cost = ticket_cost
        self.__init_bus_access = init_bus_access
        self.__init_railway_access = railway_access
        self.__time_trip_distribution = self.makeTimeTripDistribution()
        self.__distances_road = self.processMatix('ABM_model\matrices\distances_road.csv')
        self.__time_trip_railway = self.processMatix('ABM_model\matrices\\time_trip_railway.csv')
        self.__wait_time_railway = self.processMatix('ABM_model\matrices\wait_time_railway.csv')
        self.__wait_time_bus = self.processMatix('ABM_model\matrices\wait_time_bus.csv')
        self.__road_capacity = self.processMatix('ABM_model\matrices\\road_capacity.csv')


    def processMatix(self, path):
        with open(path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            time_trip_railway = list(reader)
            time_trip_railway = time_trip_railway[1:]
            
            for i in range(len(time_trip_railway)):
                time_trip_railway[i] = time_trip_railway[i][1:]
                time_trip_railway[i] = [float(val) for val in time_trip_railway[i] if val.strip() ]
        
        return time_trip_railway

    def makeTimeTripDistribution(self):
        with open('ABM_model\matrices\\time_trip_distribution.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            time_trip_distribution = list(reader)[0]
            time_trip_distribution = [float(val) for val in time_trip_distribution if val.strip() ]

        return time_trip_distribution
    
    def getTimeTripDistribution(self):
        return self.__time_trip_distribution

    def getDistanceMatrix(self):
        return self.__distances_road
    
    def getTravelTimeRailwayMatrix(self):
        return self.__time_trip_railway

    def getWaitTimeRailway(self,trips_per_line):
        matrix = []
        for i in range(len(self.__wait_time_railway)):
            matrix.append(self.__wait_time_railway[i])
            for j in range(len(self.__wait_time_railway[i])):
                matrix[i][j] = matrix[i][j] * self.__init_railway_trips / trips_per_line
        return matrix


    def getWaitTimeBus(self,bus_per_route):
        matrix = []
        for i in range(len(self.__wait_time_bus)):
            matrix.append(self.__wait_time_bus[i])
            for j in range(len(self.__wait_time_bus[i])):
                matrix[i][j] = matrix[i][j] * self.__init_bus_trips / bus_per_route
        return matrix

    def getRoadCapacity(self, road_area):
        matrix = []
        for i in range(len(self.__road_capacity)):
            matrix.append(self.__road_capacity[i])
            for j in range(len(self.__road_capacity[i])):
                matrix[i][j] = matrix[i][j] * road_area / self.__init_road_area
        return matrix

    def getBusAccess(self, bus_routes):
        bus = bus_routes*self.__init_bus_access / self.__init_bus_lines
        
        if (bus > 1):
            bus = 1

        bus_access = [1 - bus, bus]

        return bus_access

    def getRailwayAccess(self, railway_lines):
        railway = railway_lines*self.__init_railway_access / self.__init_railway_lines
        if (railway > 1):
            railway = 1
        railway_access = [1 - railway, railway]
        return railway_access
    
    def getCarCostPerKm(self, inc_rate_car):
        self.__car_cost = self.__car_cost * (1 + inc_rate_car)
        return self.__car_cost
    
    def getTicketCost(self, inc_rate_PT):
        self.__ticket_cost = self.__ticket_cost * (1 + inc_rate_PT)
        return self.__ticket_cost

