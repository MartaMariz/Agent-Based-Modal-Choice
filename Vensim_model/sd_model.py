"""
Python model 'sd_model.py'
Translated using PySD
"""

from pathlib import Path
import numpy as np

from pysd.py_backend.functions import if_then_else
from pysd.py_backend.statefuls import Initial, Integ
from pysd.py_backend.lookups import HardcodedLookups
from pysd import Component

__pysd_version__ = "3.14.0"

__data = {"scope": None, "time": lambda: 0}

_root = Path(__file__).parent


component = Component()

#######################################################################
#                          CONTROL VARIABLES                          #
#######################################################################

_control_vars = {
    "initial_time": lambda: 2011,
    "final_time": lambda: 2061,
    "time_step": lambda: 1,
    "saveper": lambda: time_step(),
}


def _init_outer_references(data):
    for key in data:
        __data[key] = data[key]


@component.add(name="Time")
def time():
    """
    Current time of the model.
    """
    return __data["time"]()


@component.add(
    name="FINAL TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def final_time():
    """
    The final time for the simulation.
    """
    return __data["time"].final_time()


@component.add(
    name="INITIAL TIME", units="year", comp_type="Constant", comp_subtype="Normal"
)
def initial_time():
    """
    The initial time for the simulation.
    """
    return __data["time"].initial_time()


@component.add(
    name="SAVEPER",
    units="year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"time_step": 1},
)
def saveper():
    """
    The frequency with which output is stored.
    """
    return __data["time"].saveper()


@component.add(
    name="TIME STEP", units="year", comp_type="Constant", comp_subtype="Normal"
)
def time_step():
    """
    The time step for the simulation.
    """
    return __data["time"].time_step()


#######################################################################
#                           MODEL VARIABLES                           #
#######################################################################


@component.add(
    name="EMISSION PETROL CAR",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_petrol_car():
    return 120


@component.add(
    name="car electricity co2 emission",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"car_electricity_activity": 1, "emission_electricity_car": 1},
)
def car_electricity_co2_emission():
    return car_electricity_activity() * emission_electricity_car() / 1000000.0


@component.add(
    name="railway electricity co2 emission",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"railway_activity_per_year": 1, "emission_electricity_railway": 1},
)
def railway_electricity_co2_emission():
    return railway_activity_per_year() * emission_electricity_railway() / 1000000.0


@component.add(
    name="car petrol co2 emission",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"car_petrol_activity": 1, "emission_petrol_car": 1},
)
def car_petrol_co2_emission():
    return car_petrol_activity() * emission_petrol_car() / 1000000.0


@component.add(
    name="EMISSION DIESEL CAR",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_diesel_car():
    return 140


@component.add(
    name="bus electricity co2 emission",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bus_electricity_activity": 1, "emission_electricity_bus": 1},
)
def bus_electricity_co2_emission():
    return bus_electricity_activity() * emission_electricity_bus() / 1000000.0


@component.add(
    name="EMISSION ELECTRICITY CAR",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_electricity_car():
    return 42.828


@component.add(
    name="Motorization rate number of motorized vehicles per 1000 inhabitants",
    units="{motorized vehicles/ 1000 inhabitants}",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "number_of_mototized_private_vehicles": 1,
        "number_of_bus": 1,
        "number_of_trains": 1,
        "population": 1,
    },
)
def motorization_rate_number_of_motorized_vehicles_per_1000_inhabitants():
    return (
        (number_of_mototized_private_vehicles() + number_of_bus() + number_of_trains())
        * 1000
        / population()
    )


@component.add(
    name="EMISSION NATURAL GAS BUS",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_natural_gas_bus():
    return 932


@component.add(
    name="car diesel co2 emissions",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"car_diesel_activity": 1, "emission_diesel_car": 1},
)
def car_diesel_co2_emissions():
    return car_diesel_activity() * emission_diesel_car() / 1000000.0


@component.add(
    name="EMISSION DIESEL BUS",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_diesel_bus():
    return 871


@component.add(
    name="EMISSION ELECTRICITY BUS",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_electricity_bus():
    return 348.3


@component.add(
    name="EMISSION ELECTRICITY RAILWAY",
    units="gCO2/km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def emission_electricity_railway():
    return 645


@component.add(
    name="bus diesel co2 emission",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bus_diesel_activity": 1, "emission_diesel_bus": 1},
)
def bus_diesel_co2_emission():
    return bus_diesel_activity() * emission_diesel_bus() / 1000000.0


@component.add(
    name="bus natural gas co2 emission",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bus_natural_gas_activity": 1, "emission_natural_gas_bus": 1},
)
def bus_natural_gas_co2_emission():
    return bus_natural_gas_activity() * emission_natural_gas_bus() / 1000000.0


@component.add(
    name="Affordability of public transport for the poorest group",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"public_transport_ticket_cost": 1, "average_monthly_income_20": 1},
)
def affordability_of_public_transport_for_the_poorest_group():
    return (public_transport_ticket_cost() / average_monthly_income_20()) * 60


@component.add(
    name="change to ticket cost",
    units="euro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"public_transport_ticket_cost": 1, "tci": 1},
)
def change_to_ticket_cost():
    return public_transport_ticket_cost() * tci()


@component.add(
    name="CAR COST KM", units="euro/km", comp_type="Constant", comp_subtype="Normal"
)
def car_cost_km():
    return 0.268


@component.add(
    name="daily walk trips",
    units="trips/day",
    comp_type="Constant",
    comp_subtype="Normal",
)
def daily_walk_trips():
    return 3333


@component.add(
    name="daily chosen bus", units="person", comp_type="Constant", comp_subtype="Normal"
)
def daily_chosen_bus():
    return 33333


@component.add(
    name="daily chosen railway",
    units="person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def daily_chosen_railway():
    return 3333


@component.add(
    name="Public Transport Ticket Cost",
    units="euro",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_public_transport_ticket_cost": 1},
    other_deps={
        "_integ_public_transport_ticket_cost": {
            "initial": {},
            "step": {"change_to_ticket_cost": 1},
        }
    },
)
def public_transport_ticket_cost():
    return _integ_public_transport_ticket_cost()


_integ_public_transport_ticket_cost = Integ(
    lambda: change_to_ticket_cost(),
    lambda: 0.5575,
    "_integ_public_transport_ticket_cost",
)


@component.add(
    name="daily chosen car",
    units="trips/day",
    comp_type="Constant",
    comp_subtype="Normal",
)
def daily_chosen_car():
    return 3333


@component.add(name="TCI", units="factor", comp_type="Constant", comp_subtype="Normal")
def tci():
    return 0


@component.add(
    name="emissions per year",
    units="tons co2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "emissions_of_greenhouse_gases_business": 1,
        "emissions_of_greenhouse_gases_mobility": 1,
        "co2_capture_green_spaces": 1,
        "co2_capture_sea_river": 1,
        "co2_technologies_capture": 1,
    },
)
def emissions_per_year():
    return (
        emissions_of_greenhouse_gases_business()
        + emissions_of_greenhouse_gases_mobility()
        - co2_capture_green_spaces()
        - co2_capture_sea_river()
        - co2_technologies_capture()
    )


@component.add(
    name="enviromental impact on economy",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emissions_per_year": 1, "ehe": 1},
)
def enviromental_impact_on_economy():
    return ehe(emissions_per_year())


@component.add(
    name="business construction",
    units="structure/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "bcn": 1,
        "business_land_multiplier": 1,
        "business_labor_force_multiplier": 1,
        "business_structures": 1,
        "enviromental_impact_on_economy": 1,
    },
)
def business_construction():
    return (
        bcn()
        * business_land_multiplier()
        * business_labor_force_multiplier()
        * business_structures()
        * enviromental_impact_on_economy()
    )


@component.add(
    name="Number of Bus Routes",
    units="routes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_number_of_bus_routes": 1},
    other_deps={
        "_integ_number_of_bus_routes": {
            "initial": {},
            "step": {"increasing_bus_routes": 1},
        }
    },
)
def number_of_bus_routes():
    return _integ_number_of_bus_routes()


_integ_number_of_bus_routes = Integ(
    lambda: increasing_bus_routes(), lambda: 94, "_integ_number_of_bus_routes"
)


@component.add(
    name="Road available",
    units="m2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_road_available": 1},
    other_deps={
        "_integ_road_available": {"initial": {}, "step": {"road_construction": 1}}
    },
)
def road_available():
    return _integ_road_available()


_integ_road_available = Integ(
    lambda: road_construction(), lambda: 400000, "_integ_road_available"
)


@component.add(
    name="Number of Railway Lines",
    units="routes",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_number_of_railway_lines": 1},
    other_deps={
        "_integ_number_of_railway_lines": {
            "initial": {},
            "step": {"increasing_railway_lines": 1},
        }
    },
)
def number_of_railway_lines():
    return _integ_number_of_railway_lines()


_integ_number_of_railway_lines = Integ(
    lambda: increasing_railway_lines(), lambda: 2, "_integ_number_of_railway_lines"
)


@component.add(
    name="ITBR", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def itbr():
    return 0


@component.add(
    name="Number of Trips per Bus Route",
    units="routes/bus",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_number_of_trips_per_bus_route": 1},
    other_deps={
        "_integ_number_of_trips_per_bus_route": {
            "initial": {},
            "step": {"increaing_bus_trips": 1},
        }
    },
)
def number_of_trips_per_bus_route():
    return _integ_number_of_trips_per_bus_route()


_integ_number_of_trips_per_bus_route = Integ(
    lambda: increaing_bus_trips(),
    lambda: 18.489,
    "_integ_number_of_trips_per_bus_route",
)


@component.add(
    name="Number of Trips per Railway line",
    units="trips",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_number_of_trips_per_railway_line": 1},
    other_deps={
        "_integ_number_of_trips_per_railway_line": {
            "initial": {},
            "step": {"increasing_railway_trips": 1},
        }
    },
)
def number_of_trips_per_railway_line():
    return _integ_number_of_trips_per_railway_line()


_integ_number_of_trips_per_railway_line = Integ(
    lambda: increasing_railway_trips(),
    lambda: 75,
    "_integ_number_of_trips_per_railway_line",
)


@component.add(
    name="ILRR", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def ilrr():
    return 0


@component.add(
    name="construction",
    units="m2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "pedestrian_sidewalk_construction": 1,
        "private_parking_construction": 1,
        "road_construction": 1,
    },
)
def construction():
    return (
        pedestrian_sidewalk_construction()
        + private_parking_construction()
        + road_construction()
    )


@component.add(
    name="increasing railway trips",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"itrr": 1, "number_of_trips_per_railway_line": 1},
)
def increasing_railway_trips():
    return itrr() * number_of_trips_per_railway_line()


@component.add(
    name="increaing bus trips",
    units="bus trips",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"itbr": 1, "number_of_trips_per_bus_route": 1},
)
def increaing_bus_trips():
    return itbr() * number_of_trips_per_bus_route()


@component.add(
    name="ITRR", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def itrr():
    return 0


@component.add(
    name="Land Use for mobility",
    units="m2",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_land_use_for_mobility": 1},
    other_deps={
        "_integ_land_use_for_mobility": {"initial": {}, "step": {"construction": 1}}
    },
)
def land_use_for_mobility():
    return _integ_land_use_for_mobility()


_integ_land_use_for_mobility = Integ(
    lambda: construction(), lambda: 9000, "_integ_land_use_for_mobility"
)


@component.add(
    name="daily railway capacity",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_capacity_railway": 1,
        "number_of_trips_per_railway_line": 1,
        "number_of_railway_lines": 1,
    },
)
def daily_railway_capacity():
    return (
        max_capacity_railway()
        * number_of_trips_per_railway_line()
        * number_of_railway_lines()
    )


@component.add(
    name="Daily railway trips",
    units="trips/day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"number_of_railway_lines": 1, "number_of_trips_per_railway_line": 1},
)
def daily_railway_trips():
    return number_of_railway_lines() * number_of_trips_per_railway_line()


@component.add(
    name="road construction",
    units="m2",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"road_available": 1, "rcr": 1},
)
def road_construction():
    return road_available() * rcr()


@component.add(
    name="increasing railway lines",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"ilrr": 1, "number_of_railway_lines": 1},
)
def increasing_railway_lines():
    return ilrr() * number_of_railway_lines()


@component.add(
    name="increasing bus routes",
    units="bus routes",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"number_of_bus_routes": 1, "irbr": 1},
)
def increasing_bus_routes():
    return number_of_bus_routes() * irbr()


@component.add(
    name="RCR", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def rcr():
    return 0


@component.add(
    name="IRBR", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def irbr():
    return 0


@component.add(
    name="gdp growth rate",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"business_growth": 1, "gdpgn": 1},
)
def gdp_growth_rate():
    return (business_growth() + gdpgn()) / 2


@component.add(
    name="emissions of greenhouse gases mobility",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "car_diesel_co2_emissions": 1,
        "car_electricity_co2_emission": 1,
        "car_petrol_co2_emission": 1,
        "bus_diesel_co2_emission": 1,
        "bus_electricity_co2_emission": 1,
        "bus_natural_gas_co2_emission": 1,
        "railway_electricity_co2_emission": 1,
    },
)
def emissions_of_greenhouse_gases_mobility():
    return (
        car_diesel_co2_emissions()
        + car_electricity_co2_emission()
        + car_petrol_co2_emission()
        + bus_diesel_co2_emission()
        + bus_electricity_co2_emission()
        + bus_natural_gas_co2_emission()
        + railway_electricity_co2_emission()
    )


@component.add(
    name="number of trains",
    units="vehicle",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"vehicles_per_line": 1, "number_of_railway_lines": 1},
)
def number_of_trains():
    return vehicles_per_line() * number_of_railway_lines()


@component.add(
    name="bus electricity activity",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bus_activity_per_year": 1, "percentage_bus_electricity": 1},
)
def bus_electricity_activity():
    return bus_activity_per_year() * percentage_bus_electricity()


@component.add(
    name="bus natural gas activity",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_bus_natural_gas": 1, "bus_activity_per_year": 1},
)
def bus_natural_gas_activity():
    return percentage_bus_natural_gas() * bus_activity_per_year()


@component.add(
    name="AVERAGE DISTANCE RAILWAY TRIP",
    units="km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_distance_railway_trip():
    return 16.3


@component.add(
    name="PERCENTAGE BUS DIESEL",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percentage_bus_diesel():
    return 0.18


@component.add(
    name="PERCENTAGE BUS ELECTRICITY",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percentage_bus_electricity():
    return 0.05


@component.add(
    name="PERCENTAGE BUS NATURAL GAS",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def percentage_bus_natural_gas():
    return 0.77


@component.add(
    name="railway activity per year",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_distance_railway_trip": 1, "daily_railway_trips": 1},
)
def railway_activity_per_year():
    return average_distance_railway_trip() * daily_railway_trips() * 365


@component.add(
    name="Railway Daily Occupancy rate",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"daily_chosen_railway": 1, "daily_railway_capacity": 1},
)
def railway_daily_occupancy_rate():
    return daily_chosen_railway() / daily_railway_capacity()


@component.add(
    name="bus diesel activity",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_bus_diesel": 1, "bus_activity_per_year": 1},
)
def bus_diesel_activity():
    return percentage_bus_diesel() * bus_activity_per_year()


@component.add(
    name="MAX CAPACITY RAILWAY",
    units="person",
    comp_type="Constant",
    comp_subtype="Normal",
)
def max_capacity_railway():
    return 252


@component.add(
    name="VEHICLES PER LINE",
    units="vehicle",
    comp_type="Constant",
    comp_subtype="Normal",
)
def vehicles_per_line():
    return 10


@component.add(
    name="business income multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"business_growth": 1, "bim": 1},
)
def business_income_multiplier():
    return bim(business_growth())


@component.add(
    name="number of bus",
    units="bus",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"vehicles_per_route": 1, "number_of_bus_routes": 1},
)
def number_of_bus():
    return vehicles_per_route() * number_of_bus_routes()


@component.add(
    name="VEHICLES PER ROUTE", units="bus", comp_type="Constant", comp_subtype="Normal"
)
def vehicles_per_route():
    return 0.65


@component.add(
    name="CO2 CAPTURE PER GREEN AREA",
    units="tons co2/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_capture_per_green_area():
    return 0.00113


@component.add(
    name="business growth",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "business_structures": 4,
        "business_demolition": 2,
        "business_construction": 2,
    },
)
def business_growth():
    """
    rate of business growth
    """
    return (
        business_structures() - business_demolition() + business_construction()
    ) / business_structures() - (
        business_structures() - business_demolition() + business_construction()
    ) / business_structures()


@component.add(
    name="DIESEL PETROL RATIO",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"initial_ratio_car_diesel": 1, "initial_ratio_car_petrol": 1},
)
def diesel_petrol_ratio():
    return initial_ratio_car_diesel() / initial_ratio_car_petrol()


@component.add(
    name="increase amount",
    units="euro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"gdp_growth_rate": 1, "average_monthly_income": 1},
)
def increase_amount():
    return gdp_growth_rate() * average_monthly_income()


@component.add(
    name="INITIAL RATIO CAR PETROL",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_ratio_car_petrol():
    return 0.389


@component.add(
    name="number of mototized private vehicles",
    units="cars",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"daily_chosen_car": 1, "tpc": 1},
)
def number_of_mototized_private_vehicles():
    return daily_chosen_car() / tpc()


@component.add(
    name="GDPGN", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def gdpgn():
    return 0.05


@component.add(
    name="Emissions of greenhouse gases",
    units="tons co2/captita/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"emissions_of_greenhouse_gases_mobility": 1, "population": 1},
)
def emissions_of_greenhouse_gases():
    return emissions_of_greenhouse_gases_mobility() / population()


@component.add(
    name="TPC", units="trips/day/car", comp_type="Constant", comp_subtype="Normal"
)
def tpc():
    """
    trips per car
    """
    return 2.3


@component.add(
    name="percentage car diesel",
    units="fraction",
    limits=(0.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_car_eletricity": 1, "diesel_petrol_ratio": 1},
)
def percentage_car_diesel():
    return (1 - percentage_car_eletricity()) / (1 + diesel_petrol_ratio())


@component.add(
    name="percentage car petrol",
    units="fraction",
    limits=(0.0, 1.0),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"percentage_car_diesel": 1, "percentage_car_eletricity": 1},
)
def percentage_car_petrol():
    return 1 - percentage_car_diesel() - percentage_car_eletricity()


@component.add(
    name="INITIAL RATIO CAR DIESEL",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_ratio_car_diesel():
    return 0.69


@component.add(
    name="INITIAL RATIO CAR ELECTRICITY",
    units="fraction",
    comp_type="Constant",
    comp_subtype="Normal",
)
def initial_ratio_car_electricity():
    return 0.001


@component.add(
    name="percentage car eletricity",
    units="fraction",
    limits=(0.0, 1.0),
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_percentage_car_eletricity": 1},
    other_deps={
        "_integ_percentage_car_eletricity": {
            "initial": {"initial_ratio_car_electricity": 1},
            "step": {"percentage_car_eletricity": 2, "gdp_growth_rate": 1},
        }
    },
)
def percentage_car_eletricity():
    return _integ_percentage_car_eletricity()


_integ_percentage_car_eletricity = Integ(
    lambda: if_then_else(
        percentage_car_eletricity() < 0.9,
        lambda: gdp_growth_rate() * 5 * percentage_car_eletricity(),
        lambda: 0,
    ),
    lambda: initial_ratio_car_electricity(),
    "_integ_percentage_car_eletricity",
)


@component.add(
    name="PRIVATE PARKING CONSTRUCTION",
    units="m2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def private_parking_construction():
    return 20


@component.add(
    name="MAX CAPACITY BUS", units="person", comp_type="Constant", comp_subtype="Normal"
)
def max_capacity_bus():
    return 160


@component.add(
    name="BUS Daily Occupancy rate",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"daily_chosen_bus": 1, "daily_bus_capacity": 1},
)
def bus_daily_occupancy_rate():
    return daily_chosen_bus() / daily_bus_capacity()


@component.add(
    name="daily bus capacity",
    units="person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "max_capacity_bus": 1,
        "number_of_trips_per_bus_route": 1,
        "number_of_bus_routes": 1,
    },
)
def daily_bus_capacity():
    return max_capacity_bus() * number_of_trips_per_bus_route() * number_of_bus_routes()


@component.add(
    name="PEDESTRIAN SIDEWALK CONSTRUCTION",
    units="m2",
    comp_type="Constant",
    comp_subtype="Normal",
)
def pedestrian_sidewalk_construction():
    return 20


@component.add(
    name="Daily bus trips",
    units="trips/day",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"number_of_bus_routes": 1, "number_of_trips_per_bus_route": 1},
)
def daily_bus_trips():
    return number_of_bus_routes() * number_of_trips_per_bus_route()


@component.add(
    name="Mobility space usage",
    units="m2/person",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_use_for_mobility": 1, "population": 1},
)
def mobility_space_usage():
    return land_use_for_mobility() / population()


@component.add(
    name="AVERAGE DISTANCE BUS ROUTES",
    units="km",
    comp_type="Constant",
    comp_subtype="Normal",
)
def average_distance_bus_routes():
    return 16.3


@component.add(
    name="AVERAGE DISTANCE CAR", units="km", comp_type="Constant", comp_subtype="Normal"
)
def average_distance_car():
    return 12.8


@component.add(
    name="co2 capture green spaces",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"co2_capture_per_green_area": 1, "green_area": 1},
)
def co2_capture_green_spaces():
    return co2_capture_per_green_area() * green_area()


@component.add(
    name="CO2 CAPTURE PER M2 BODY OF WATER",
    units="tons co2/m2/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_capture_per_m2_body_of_water():
    return 0.001


@component.add(
    name="co2 capture sea river",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"body_of_water_m2": 1, "co2_capture_per_m2_body_of_water": 1},
)
def co2_capture_sea_river():
    return body_of_water_m2() * co2_capture_per_m2_body_of_water()


@component.add(
    name="CO2 TECHNOLOGIES CAPTURE",
    units="tons co2/year",
    comp_type="Constant",
    comp_subtype="Normal",
)
def co2_technologies_capture():
    return 9


@component.add(
    name="emissions of greenhouse gases business",
    units="tons co2/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"business_structures": 1, "epb": 1},
)
def emissions_of_greenhouse_gases_business():
    return business_structures() * epb()


@component.add(
    name="BODY OF WATER M2", units="m2", comp_type="Constant", comp_subtype="Normal"
)
def body_of_water_m2():
    return 4731800.0


@component.add(
    name="bus activity per year",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_distance_bus_routes": 1, "daily_bus_trips": 1},
)
def bus_activity_per_year():
    return average_distance_bus_routes() * daily_bus_trips() * 365


@component.add(
    name="car activity per year",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_distance_car": 1, "daily_chosen_car": 1},
)
def car_activity_per_year():
    return average_distance_car() * daily_chosen_car() * 365


@component.add(
    name="car diesel activity",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"car_activity_per_year": 1, "percentage_car_diesel": 1},
)
def car_diesel_activity():
    return car_activity_per_year() * percentage_car_diesel()


@component.add(
    name="car electricity activity",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"car_activity_per_year": 1, "percentage_car_eletricity": 1},
)
def car_electricity_activity():
    return car_activity_per_year() * percentage_car_eletricity()


@component.add(
    name="car petrol activity",
    units="km/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"car_activity_per_year": 1, "percentage_car_petrol": 1},
)
def car_petrol_activity():
    return car_activity_per_year() * percentage_car_petrol()


@component.add(
    name="GREEN AREA", units="m2", comp_type="Constant", comp_subtype="Normal"
)
def green_area():
    return 59937500.0


@component.add(
    name="EpB", units="tons co2/year", comp_type="Constant", comp_subtype="Normal"
)
def epb():
    return 3.439


@component.add(
    name="average monthly income 90",
    units="euro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_monthly_income": 1,
        "income_90_multiplier": 1,
        "business_income_multiplier": 1,
    },
)
def average_monthly_income_90():
    return average_monthly_income() * (
        business_income_multiplier() + income_90_multiplier()
    )


@component.add(
    name="average monthly income 20",
    units="euro",
    limits=(765.0, np.nan),
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "average_monthly_income": 1,
        "income_20_multiplier": 1,
        "labor_force_income_multiplier": 1,
    },
)
def average_monthly_income_20():
    return average_monthly_income() * (
        income_20_multiplier() + labor_force_income_multiplier()
    )


@component.add(
    name="average monthly income 50",
    units="euro",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"average_monthly_income": 1, "income_50_multiplier": 1},
)
def average_monthly_income_50():
    return average_monthly_income() * income_50_multiplier()


@component.add(
    name="income 90 multiplier",
    units="euro",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_income_90_multiplier": 1},
    other_deps={
        "_initial_income_90_multiplier": {
            "initial": {"imi90": 1, "average_monthly_income": 1},
            "step": {},
        }
    },
)
def income_90_multiplier():
    return _initial_income_90_multiplier()


_initial_income_90_multiplier = Initial(
    lambda: imi90() / average_monthly_income(), "_initial_income_90_multiplier"
)


@component.add(
    name="income 50 multiplier",
    units="factor",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_income_50_multiplier": 1},
    other_deps={
        "_initial_income_50_multiplier": {
            "initial": {"imi50": 1, "average_monthly_income": 1},
            "step": {},
        }
    },
)
def income_50_multiplier():
    return _initial_income_50_multiplier()


_initial_income_50_multiplier = Initial(
    lambda: imi50() / average_monthly_income(), "_initial_income_50_multiplier"
)


@component.add(
    name="average monthly income",
    units="euro",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_average_monthly_income": 1},
    other_deps={
        "_integ_average_monthly_income": {"initial": {}, "step": {"increase_amount": 1}}
    },
)
def average_monthly_income():
    return _integ_average_monthly_income()


_integ_average_monthly_income = Integ(
    lambda: increase_amount(), lambda: 784, "_integ_average_monthly_income"
)


@component.add(
    name="income 20 multiplier",
    units="fraction",
    comp_type="Stateful",
    comp_subtype="Initial",
    depends_on={"_initial_income_20_multiplier": 1},
    other_deps={
        "_initial_income_20_multiplier": {
            "initial": {"imi20": 1, "average_monthly_income": 1},
            "step": {},
        }
    },
)
def income_20_multiplier():
    return _initial_income_20_multiplier()


_initial_income_20_multiplier = Initial(
    lambda: imi20() / average_monthly_income(), "_initial_income_20_multiplier"
)


@component.add(
    name="BIM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_bim"},
)
def bim(x, final_subs=None):
    return _hardcodedlookup_bim(x, final_subs)


_hardcodedlookup_bim = HardcodedLookups(
    [-0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
    [-0.05, 0.0, 0.05, 0.15, 0.25, 0.35, 0.5, 0.7, 0.8, 0.9, 0.95, 1.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_bim",
)


@component.add(
    name="LFIM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_lfim"},
)
def lfim(x, final_subs=None):
    return _hardcodedlookup_lfim(x, final_subs)


_hardcodedlookup_lfim = HardcodedLookups(
    [
        0.0,
        0.1,
        0.2,
        0.3,
        0.4,
        0.5,
        0.6,
        0.7,
        0.8,
        0.9,
        1.0,
        1.1,
        1.2,
        1.3,
        1.4,
        1.5,
        1.6,
        1.7,
        1.8,
        1.9,
        2.0,
        8.0,
    ],
    [
        1.0,
        1.15,
        1.3,
        1.4,
        1.45,
        1.4,
        1.3,
        0.9,
        0.5,
        0.25,
        0.1,
        0.0,
        -0.01,
        -0.015,
        -0.02,
        -0.025,
        -0.03,
        -0.035,
        -0.04,
        -0.045,
        -0.05,
        -0.1,
    ],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_lfim",
)


@component.add(
    name="labor force income multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labor_to_job_ratio": 1, "lfim": 1},
)
def labor_force_income_multiplier():
    return lfim(labor_to_job_ratio())


@component.add(name="IMI50", units="euro", comp_type="Constant", comp_subtype="Normal")
def imi50():
    return 744


@component.add(name="IMI90", units="euro", comp_type="Constant", comp_subtype="Normal")
def imi90():
    return 3237


@component.add(name="IMI20", units="euro", comp_type="Constant", comp_subtype="Normal")
def imi20():
    return 566


@component.add(
    name="AHM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_ahm"},
)
def ahm(x, final_subs=None):
    return _hardcodedlookup_ahm(x, final_subs)


_hardcodedlookup_ahm = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
    [1.4, 1.4, 1.35, 1.3, 1.15, 1.0, 0.8, 0.65, 0.5, 0.45, 0.4],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_ahm",
)


@component.add(
    name="housing construction",
    units="structure/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "hcn": 1,
        "housing_land_multiplier": 1,
        "housing_availability_multiplier": 1,
        "housing": 1,
    },
)
def housing_construction():
    return (
        hcn()
        * housing_land_multiplier()
        * housing_availability_multiplier()
        * housing()
    )


@component.add(
    name="net births",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bn": 1, "dn": 1, "population": 1},
)
def net_births():
    return (bn() - dn()) * population()


@component.add(
    name="outmigration",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population": 1, "omn": 1},
)
def outmigration():
    return population() * omn()


@component.add(
    name="inmigration",
    units="people/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={
        "population": 1,
        "imn": 1,
        "attractiveness_from_jobs_multiplier": 1,
        "attractiveness_from_housing_multiplier": 1,
    },
)
def inmigration():
    return (
        population()
        * imn()
        * attractiveness_from_jobs_multiplier()
        * attractiveness_from_housing_multiplier()
    )


@component.add(
    name="Population",
    units="people",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_population": 1},
    other_deps={
        "_integ_population": {
            "initial": {},
            "step": {"net_births": 1, "inmigration": 1, "outmigration": 1},
        }
    },
)
def population():
    return _integ_population()


_integ_population = Integ(
    lambda: net_births() + inmigration() - outmigration(),
    lambda: 168363,
    "_integ_population",
)


@component.add(
    name="EHE",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_ehe"},
)
def ehe(x, final_subs=None):
    return _hardcodedlookup_ehe(x, final_subs)


_hardcodedlookup_ehe = HardcodedLookups(
    [0.0, 600000.0, 9000000.0],
    [1.0, 0.9, 0.7],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_ehe",
)


@component.add(name="AREA", units="m2", comp_type="Constant", comp_subtype="Normal")
def area():
    return 22814900.0


@component.add(
    name="attractiveness from jobs multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labor_to_job_ratio": 1, "ehe": 1},
)
def attractiveness_from_jobs_multiplier():
    return ehe(labor_to_job_ratio())


@component.add(
    name="attractiveness from housing multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_to_housing_ratio": 1, "ahm": 1},
)
def attractiveness_from_housing_multiplier():
    return ahm(households_to_housing_ratio())


@component.add(
    name="BCN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def bcn():
    return 0.02565


@component.add(
    name="BDN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def bdn():
    return 0.02758


@component.add(
    name="BLFM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_blfm"},
)
def blfm(x, final_subs=None):
    return _hardcodedlookup_blfm(x, final_subs)


_hardcodedlookup_blfm = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
    [0.2, 0.25, 0.35, 0.5, 0.7, 1.0, 1.35, 1.6, 1.8, 1.95, 2.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_blfm",
)


@component.add(
    name="BLM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_blm"},
)
def blm(x, final_subs=None):
    return _hardcodedlookup_blm(x, final_subs)


_hardcodedlookup_blm = HardcodedLookups(
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    [1.0, 1.15, 1.3, 1.4, 1.45, 1.4, 1.3, 0.9, 0.5, 0.25, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_blm",
)


@component.add(
    name="BN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def bn():
    return 0.0083


@component.add(
    name="business demolition",
    units="structure/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"bdn": 1, "business_structures": 1},
)
def business_demolition():
    return bdn() * business_structures()


@component.add(
    name="business labor force multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labor_to_job_ratio": 1, "blfm": 1},
)
def business_labor_force_multiplier():
    return blfm(labor_to_job_ratio())


@component.add(
    name="business land multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_fraction_occupied": 1, "blm": 1},
)
def business_land_multiplier():
    return blm(land_fraction_occupied())


@component.add(
    name="Business structures",
    units="structure",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_business_structures": 1},
    other_deps={
        "_integ_business_structures": {
            "initial": {},
            "step": {"business_construction": 1, "business_demolition": 1},
        }
    },
)
def business_structures():
    return _integ_business_structures()


_integ_business_structures = Integ(
    lambda: business_construction() - business_demolition(),
    lambda: 14502,
    "_integ_business_structures",
)


@component.add(
    name="DN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def dn():
    return 0.00732


@component.add(
    name="HAM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_ham"},
)
def ham(x, final_subs=None):
    return _hardcodedlookup_ham(x, final_subs)


_hardcodedlookup_ham = HardcodedLookups(
    [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
    [0.2, 0.25, 0.35, 0.5, 0.7, 1.0, 1.35, 1.6, 1.8, 1.95, 2.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_ham",
)


@component.add(
    name="HCN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def hcn():
    return 0.001076


@component.add(
    name="HDN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def hdn():
    return 0


@component.add(
    name="HLM",
    units="fraction",
    comp_type="Lookup",
    comp_subtype="Normal",
    depends_on={"__lookup__": "_hardcodedlookup_hlm"},
)
def hlm(x, final_subs=None):
    return _hardcodedlookup_hlm(x, final_subs)


_hardcodedlookup_hlm = HardcodedLookups(
    [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0],
    [0.4, 0.7, 1.0, 1.25, 1.45, 1.5, 1.5, 1.4, 1.0, 0.5, 0.0],
    {},
    "interpolate",
    {},
    "_hardcodedlookup_hlm",
)


@component.add(
    name="households to housing ratio",
    units="family/structure",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"population": 1, "hs": 1, "housing": 1},
)
def households_to_housing_ratio():
    return (population() / hs()) / housing()


@component.add(
    name="Housing",
    units="structure",
    comp_type="Stateful",
    comp_subtype="Integ",
    depends_on={"_integ_housing": 1},
    other_deps={
        "_integ_housing": {
            "initial": {},
            "step": {"housing_construction": 1, "housing_demolition": 1},
        }
    },
)
def housing():
    return _integ_housing()


_integ_housing = Integ(
    lambda: housing_construction() - housing_demolition(),
    lambda: 73416,
    "_integ_housing",
)


@component.add(
    name="housing availability multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"households_to_housing_ratio": 1, "ham": 1},
)
def housing_availability_multiplier():
    return ham(households_to_housing_ratio())


@component.add(
    name="housing demolition",
    units="structure/year",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"hdn": 1, "housing": 1},
)
def housing_demolition():
    return hdn() * housing()


@component.add(
    name="housing land multiplier",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"land_fraction_occupied": 1, "hlm": 1},
)
def housing_land_multiplier():
    return hlm(land_fraction_occupied())


@component.add(
    name="HS", units="people/family", comp_type="Constant", comp_subtype="Normal"
)
def hs():
    return 2.7


@component.add(
    name="IMN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def imn():
    return 0.0283


@component.add(
    name="jobs",
    units="job",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"jpbs": 1, "business_structures": 1},
)
def jobs():
    return jpbs() * business_structures()


@component.add(
    name="JPBS", units="job/structure", comp_type="Constant", comp_subtype="Normal"
)
def jpbs():
    return 2.3


@component.add(
    name="labor force",
    units="people",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"lpf": 1, "population": 1},
)
def labor_force():
    return lpf() * population()


@component.add(
    name="labor to job ratio",
    units="people/job",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"labor_force": 1, "jobs": 1},
)
def labor_to_job_ratio():
    return labor_force() / jobs()


@component.add(
    name="land fraction occupied",
    units="fraction",
    comp_type="Auxiliary",
    comp_subtype="Normal",
    depends_on={"business_structures": 1, "lpbs": 1, "housing": 1, "lph": 1, "area": 1},
)
def land_fraction_occupied():
    return (business_structures() * lpbs() + housing() * lph()) / area()


@component.add(
    name="LPBS", units="m2/structure", comp_type="Constant", comp_subtype="Normal"
)
def lpbs():
    return 80


@component.add(
    name="LPF", units="fraction", comp_type="Constant", comp_subtype="Normal"
)
def lpf():
    return 0.696


@component.add(
    name="LPH", units="m2/structure", comp_type="Constant", comp_subtype="Normal"
)
def lph():
    return 80


@component.add(
    name="OMN", units="fraction/year", comp_type="Constant", comp_subtype="Normal"
)
def omn():
    return 0.0215
