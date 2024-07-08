import numpy as np
from scipy.optimize import minimize

RA = 400000
CC = 0.2
TP_bus = 0.9
BR = 94
BTR = 18.4
TP_rail = 0.9
RR = 2
RTR = 75
I = 1400

P_known_car = 0.689044318
P_known_bus = 0.146875353
P_known_rail = 0.014330929
P_known_walk = 0.1486515

# Initial guesses 
initial_guess = [0] * 15

def utilities(params):
    beta_car = params[:4]
    beta_bus = params[4:9]
    beta_rail = params[9:14]
    beta_walk = params[14]
    
    U_car = beta_car[0] + beta_car[1] * RA + beta_car[2] * CC + beta_car[3] * I
    U_bus = beta_bus[0] + beta_bus[1] * TP_bus + beta_bus[2] * BR + beta_bus[3] * BTR + beta_bus[4] * I
    U_rail = beta_rail[0] + beta_rail[1] * TP_rail + beta_rail[2] * RR + beta_rail[3] * RTR + beta_rail[4] * I
    U_walk = beta_walk
    
    return U_car, U_bus, U_rail, U_walk

def objective(params):
    U_car, U_bus, U_rail, U_walk = utilities(params)
    
    exp_U_car = np.exp(U_car)
    exp_U_bus = np.exp(U_bus)
    exp_U_rail = np.exp(U_rail)
    exp_U_walk = np.exp(U_walk)
    
    sum_exp_U = exp_U_car + exp_U_bus + exp_U_rail + exp_U_walk
    
    P_car = exp_U_car / sum_exp_U
    P_bus = exp_U_bus / sum_exp_U
    P_rail = exp_U_rail / sum_exp_U
    P_walk = exp_U_walk / sum_exp_U
    
    error = ((P_car - P_known_car)**2 + (P_bus - P_known_bus)**2 + 
             (P_rail - P_known_rail)**2 + (P_walk - P_known_walk)**2)
    
    write_str = f"Car: {P_car}, Bus: {P_bus}, Rail: {P_rail}, Walk: {P_walk} -- Params: {params} Error: {error}\n"
    open('log_sd_only.txt', 'a').write(write_str)
    
    return error

result = minimize(objective, initial_guess, method='Nelder-Mead')

beta_estimated = result.x

print("Estimated coefficients:")
print(f"Car: {beta_estimated[:4]}")
print(f"Bus: {beta_estimated[4:9]}")
print(f"Rail: {beta_estimated[9:14]}")
print(f"Walk: {beta_estimated[14]}")
