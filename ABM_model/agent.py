from mesa import Agent
import random


class MyAgent(Agent):
    def __init__(self, environment, unique_id, start, end, income, time_trip, first_mile, last_mile, metro_access, bus_access, walk_access, car_access, a = 0.15, b = 4):
        super().__init__(unique_id, environment)
        self._start = start
        self._end = end
        self._income = income
        self._time_trip = time_trip
        self._first_mile = first_mile
        self._last_mile = last_mile
        self._metro_access = metro_access
        self._bus_access = bus_access
        self._walk_access = walk_access
        self._car_access = car_access
        self._a = a
        self._b = b
        self._hours_month = 176
        self._car_speed = 90
        self._bus_speed = 50
        self._walking_speed = 4.54
        self._value_of_travel_time = self.getValueOfTravelTime()
        #print("Hello from agent", unique_id, "from", start, "to", end)
    
    def getValueOfTravelTime(self):
        return self._income / self._hours_month
    
    def setPreferences(self, withPref):
        if (withPref == 0):
            self._car_pref = 1
            self._bus_pref = 1
            self._railway_pref = 1
            self._walk_pref = 1
            self._car_pref = 1
            return
        self._car_pref = random.uniform(0.5,1)
        self._bus_pref = random.uniform(0.5,1)
        self._railway_pref = random.uniform(0.5,1)
        self._walk_pref = random.uniform(0.5,1)

    

    def setPVCost(self, distance, cost_per_km, congestion):
        if (self._car_access == 0):
            self._car_cost = 100000
            return
        time_travel = (1 + self._b * congestion ** self._a) * distance / self._car_speed
        self._car_cost = distance * cost_per_km + time_travel * self._value_of_travel_time
    
    def setBusCost(self, wait_time, ticket_cost, distance):
        if (self._bus_access == 0):
            self._bus_cost = 100000
            return
        self._bus_cost = (( wait_time/60 + self._first_mile / self._walking_speed + self._last_mile / self._walking_speed + distance / self._bus_speed) * self._value_of_travel_time + ticket_cost )
    
    def setRailwayCost(self, time_trip, wait_time, ticket_cost):
        if (self._metro_access == 0):
            self._railway_cost = 100000
            return
        self._railway_cost = ((time_trip/60 + wait_time/60 + self._first_mile / self._walking_speed + self._last_mile / self._walking_speed) * self._value_of_travel_time + ticket_cost) 

    def setWalkCost(self, distance):
        self._walk_cost = (distance / self._walking_speed * self._value_of_travel_time) 

    def getPos(self):
        return self._start, self._end, self._time_trip
    
    def step(self):
        if (self._car_cost < self._bus_cost and self._car_cost < self._railway_cost and self._car_cost < self._walk_cost):
            return self._time_trip,"car"
        elif (self._bus_cost < self._railway_cost and self._bus_cost < self._walk_cost):
            return self._time_trip,"bus"
        elif (self._railway_cost < self._walk_cost ):
            return self._time_trip,"railway"
        else:
            return self._time_trip,"walk"

