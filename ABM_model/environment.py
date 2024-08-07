from mesa import Model
import pandas as pd
from ABM_model.agent import MyAgent
import csv
import random
from collections import defaultdict

class Environment(Model):
    def __init__(self, num_agents,income, active_population, infraestructure, epsilon = 0.1, learning_rate = 5):
        super().__init__()
        self.income = income
        self.num_agents = num_agents
        self.infra = infraestructure
        self.learning_rate = learning_rate 
        self._explore = epsilon

        self.time_distribution = self.infra.getTimeTripDistribution()
        self.distances_road = self.infra.getDistanceMatrix()
        self.time_trip_railway = self.infra.getTravelTimeRailwayMatrix()

        self.population = []

        self.setChoiceCounts()
        self.traffic_distribution = [[ [0 for col in range(24)] for col in range(12)] for row in range(12)]
        self.congestion = [[ [0 for col in range(24)] for col in range(12)] for row in range(12)]
        self.setIncomeDistribution(active_population)
        self.data = pd.DataFrame([], columns = ['id', 'Income','Car cost','Car time', 'Bus cost', 'Bus time', 'Railway cost', 'Railway time', 'Walk cost', 'Walk time'])

    def setInfrastructure(self, bus_per_route, trips_per_line, bus_routes, railway_lines,road_area):
        self.wait_time_bus = self.infra.getWaitTimeBus(bus_per_route)
        self.wait_time_railway = self.infra.getWaitTimeRailway(trips_per_line)
        self.road_capacity = self.infra.getRoadCapacity(road_area)
        self.bus_access = self.infra.getBusAccess(bus_routes)
        self.railway_access = self.infra.getRailwayAccess(railway_lines)

    
    def setTicketCost(self, ticket_cost):
        self.ticket_cost = ticket_cost

    def setCarCostPerKm(self, car_cost_per_km):
        self.car_cost_per_km = car_cost_per_km

    def setChoiceCounts(self):
        self.choice_counts = defaultdict(lambda: {'car': 0, 'bus': 0, 'railway': 0, 'walk': 0})

        
    def runLogit(self, params):
        res = []
        if (self.population == []):
            self.createPopulation()

        for _ in range(self.learning_rate):
            self.setChoiceCounts()
            self.stepLogitModel(params)
            self.buildCongestionMatrix()
            total_car, total_bus, total_railway, total_walk= self.getResults()
            res.append(total_car)
        
        print("Total agents: ", total_car + total_bus + total_railway + total_walk)
        
        return total_car, total_bus, total_railway, total_walk

        percentage_car = total_car/(total_car + total_bus + total_railway + total_walk)
        percentage_bus = total_bus/(total_car + total_bus + total_railway + total_walk)
        percentage_railway = total_railway/(total_car + total_bus + total_railway + total_walk)
        percentage_walk = total_walk/(total_car + total_bus + total_railway + total_walk)

        return percentage_car, percentage_bus, percentage_railway, percentage_walk
    
    def runMatrixBased(self):
        self.createPopulation()

        for _ in range(self.learning_rate):
            self.setChoiceCounts()
            self.step()
            self.buildCongestionMatrix()

        return self.getResults()

    def setIncomeDistribution(self, active_population):
        income_distribution = [0.2, 0.70, 0.10]
        self.income_distribution =[1 - active_population] + [active_population * val for val in income_distribution]

    def createPopulation(self):
        self.population = []

        origin_destination_matrix = self.getDestinationMatrix()
        for i in range(len(origin_destination_matrix)):
            for j in range(len(origin_destination_matrix[i])):      
                num_agents = int(origin_destination_matrix[i][j] * self.num_agents)

                for k in range(num_agents):
                    index_income = random.choices(range(4), weights=self.income_distribution)[0] 
                    bus_access = random.choices(range(2), weights=self.bus_access)[0]
                    metro_access = random.choices(range(2), weights=self.railway_access)[0]
                    time_trip = random.choices(range(24), weights=self.time_distribution)[0]
                    if (index_income == 0):
                        car_access = 0
                    else:
                        car_access = 1
                        
                    agent_id = i * 10000 + j * 100 + k
                    first_km = random.uniform(0,1)
                    last_km = random.uniform(0,1)
                    agent = MyAgent(self,agent_id, i, j, self.income[index_income], time_trip, first_km, last_km, car_access, bus_access, metro_access,1) 
                    self.population.append(agent)
        
    def getDestinationMatrix(self):
        with open('ABM_model\matrices\origin_destination.csv', newline='') as csvfile:
            reader = csv.reader(csvfile)
            matrix = list(reader)
            matrix = [[float(val) for val in row if val.strip()] for row in matrix]
            origin_destination_matrix = []
            for i in range(len(matrix)):
                if (matrix[i] != []):
                    origin_destination_matrix.append(matrix[i])
        return origin_destination_matrix

    def step(self):
        
        for agent in self.population:
            i, j, time = agent.getPos()

            agent.setPVCost(self.distances_road[i][j],self.car_cost_per_km, self.congestion[i][j][time])
            agent.setBusCost(self.wait_time_bus[i][j], self.ticket_cost, self.distances_road[i][j])
            agent.setRailwayCost(self.time_trip_railway[i][j], self.wait_time_railway[i][j], self.ticket_cost)
            agent.setWalkCost(self.distances_road[i][j])
            time, choice = agent.step(self._explore)

            if (choice == "car"):
                self.traffic_distribution[i][j][time] += 1

            if choice in self.choice_counts[i,j]:
                self.choice_counts[i,j][choice] += 1


    def stepLogitModel(self, params):
        for agent in self.population:
            i, j, time = agent.getPos()

            agent.setPVLogitCost(self.distances_road[i][j],self.car_cost_per_km, self.congestion[i][j][time])
            agent.setBusLogitCost(self.wait_time_bus[i][j], self.ticket_cost, self.distances_road[i][j])
            agent.setRailwayLogitCost(self.time_trip_railway[i][j], self.wait_time_railway[i][j], self.ticket_cost)
            agent.setWalkLogitCost(self.distances_road[i][j])
        
            time, choice, line = agent.LMstep(params)
            
            if (choice == "car"):
                self.traffic_distribution[i][j][time] += 1

            if choice in self.choice_counts[i,j]:
                self.choice_counts[i,j][choice] += 1
            
    def displayResults(self, total_car, total_bus, total_railway, total_walk):
        print("Total agents: ", total_car + total_bus + total_railway + total_walk)
        print("Percentage car: ", total_car/(total_car + total_bus + total_railway + total_walk))
        print("Percentage bus: ", total_bus/(total_car + total_bus + total_railway + total_walk))
        print("Percentage railway: ", total_railway/(total_car + total_bus + total_railway + total_walk))
        print("Percentage walk: ", total_walk/(total_car + total_bus + total_railway + total_walk))


    
    def getResults(self):
        total_car = 0
        total_bus = 0
        total_railway = 0
        total_walk = 0
        for key in self.choice_counts:
            total_car += self.choice_counts[key]['car']
            total_bus += self.choice_counts[key]['bus']
            total_railway += self.choice_counts[key]['railway']
            total_walk += self.choice_counts[key]['walk']

        

        return total_car, total_bus, total_railway, total_walk
    
    def buildCongestionMatrix(self):
        for i in range(len(self.traffic_distribution)):
            for j in range(len(self.traffic_distribution[i])):
                for h in range(len(self.traffic_distribution[i][j])):
                    self.congestion[i][j][h] = self.traffic_distribution[i][j][h]/self.road_capacity[i][j]
                    self.traffic_distribution[i][j][h] = 0

                    
        

    def getAverageDistanceCar(self):
        total_car_choice = 0
        total_distance = 0
        for key in self.choice_counts:
            total_car_choice += self.choice_counts[key]['car']
            total_distance += self.choice_counts[key]['car'] * self.distances_road[key[0]][key[1]]
        return total_distance/total_car_choice
 