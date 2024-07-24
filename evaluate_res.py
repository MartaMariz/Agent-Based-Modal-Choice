from scipy import stats
from scipy.optimize import approx_fprime
import numpy as np
import scipy.optimize as opt
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import ABM_model.environment as env
import ABM_model.infrastructure as infra
import numdifftools as nd



# Log-likelihood function (negative for minimization)
def log_likelihood(params):
    print("run logit")
    p_car, p_bus, p_railway, p_walk = abm_2017.runLogit(params)
    print("2017 p_car: ", p_car, "p_bus: ", p_bus, "p_railway: ", p_railway, "p_walk: ", p_walk)
    p_known_car = 0.689044318
    p_known_bus = 0.146875353
    p_known_railway = 0.014330929
    p_known_walk = 0.1486515

    log_likelihood_2017 = (
        np.log(p_car) * p_known_car +
        np.log(p_bus) * p_known_bus +
        np.log(p_railway) * p_known_railway +
        np.log(p_walk) * p_known_walk
    )
    print("2017 log likelihood: ", log_likelihood_2017)


    p_car2011, p_bus2011, p_railway2011, p_walk2011 = abm_2011.runLogit(params)
    print("2011 p_car: ", p_car2011, "p_bus: ", p_bus2011, "p_railway: ", p_railway2011, "p_walk: ", p_walk2011)
    p_known_car2011 = 0.597
    p_known_PT2011 = 0.266
    p_known_walk2011 = 0.129  

    p_pt2011 = p_bus2011 + p_railway2011

    log_likelihood_2011 = (
        np.log(p_car2011) * p_known_car2011 +
        np.log(p_pt2011) * p_known_PT2011 +
        np.log(p_walk2011) * p_known_walk2011
    )
    print("2011 log likelihood: ", log_likelihood_2011)

    total_log_likelihood = log_likelihood_2017 + log_likelihood_2011

    return -total_log_likelihood

optimized_params =  [ 0.27117714 , 1.00859475, -0.58227141, -0.22235262,  0.09974352, -0.12770431,
 -0.47398467, -0.53674531, -0.29782998, -0.21640827 ,-0.3618814,  -0.04602262,
  0.44986636 ,-0.06424772  ,0.19956048 ,-0.96693675]



abm_infra = infra.Infrastructure(400000, 94 ,2, 75 ,18.489, 0.9, 0.268)

abm_2011 = env.Environment(263702.2, [200, 500, 800, 1500], 0.696, abm_infra)
abm_2011.setInfrastructure(18.489, 75, 94, 2, 400000)
abm_2011.setTicketCost(0.456)
abm_2011.setCarCostPerKm(0.2437)

abm_2017 = env.Environment(263702.2, [200, 560, 850, 2000], 0.696, abm_infra)
abm_2017.setInfrastructure(18.489, 75, 94, 2, 400000)
abm_2017.setTicketCost(0.5)
abm_2017.setCarCostPerKm(0.26)


#Calculate the Hessian matrix using numdifftools
hessian_matrix = nd.Hessian(log_likelihood)(optimized_params)
print("Hessian matrix:", hessian_matrix)

# Invert the Hessian matrix to get the covariance matrix
cov_matrix = np.linalg.inv(hessian_matrix)
print("Covariance matrix:", cov_matrix)

# Standard errors are the square roots of the diagonal elements of the covariance matrix
standard_errors = np.sqrt(np.diag(cov_matrix))
print("Standard errors:", standard_errors)

# Calculate t-values (coefficients / standard errors)
t_values = optimized_params / standard_errors
print("t-values:", t_values)

# Calculate p-values
p_values = [2 * (1 - stats.norm.cdf(np.abs(t))) for t in t_values]

# Output the results
print("Parameter Estimates:", optimized_params)
print("Standard Errors:", standard_errors)
print("t-values:", t_values)
print("p-values:", p_values)

#write res to file
res = pd.DataFrame({'Parameter Estimates': optimized_params, 'Standard Errors': standard_errors, 't-values': t_values, 'p-values': p_values})
res.to_csv('res.csv')