import matplotlib.pyplot as plt

def getLaborIncomeRelationship():
    labor_to_job_ratio = [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2, 4]

    income_growth = [0.5, 0.6, 0.65, 0.7, 0.75,0.7, 0.65, 0.45, 0.25, 0.15, 0.075, 0, -0.01, -0.015, -0.02, -0.025, -0.03, -0.035, -0.04, -0.045, -0.05, -0.1]

    res = []
    for i in range(len(labor_to_job_ratio)):
        res.append((labor_to_job_ratio[i], income_growth[i]))
    print(res)


    print(labor_to_job_ratio)
    print(income_growth)


    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(labor_to_job_ratio, income_growth, marker='o', linestyle='-', color='b')

    # Add titles and labels
    plt.title('Relationship between Labor-to-Job Ratio and Income Growth for the 25th Percentile')
    plt.xlabel('Labor-to-Job Ratio')
    plt.ylabel('Income Growth')

    # Show the plot
    plt.grid(True)
    plt.show()

def getBusinessIncomeRelationship():
    res = [(-0.4, -0.07),(-0.2, -0.05), (0, 0), (0.2, 0.05), (0.4, 0.15), (0.6, 0.25), (0.8, 0.35), (1, 0.5), (1.2, 0.7), (1.4, 0.8), (1.6, 0.9), (1.8, 0.95), (2, 1)]
    business = []
    income_growth = []
    for i in range(len(res)):
        business.append(res[i][0])
        income_growth.append(res[i][1])
    

    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(business, income_growth, marker='o', linestyle='-', color='b')

    # Add titles and labels
    plt.title('Relationship between Business growth and Income Growth for the 95th Percentile')
    plt.xlabel('Business Growth')
    plt.ylabel('Income Growth')

    # Show the plot
    plt.grid(True)
    plt.show()

def getEnvironmentalImpact():
    impact = [(0,1),(9e+06,0.7)]
    emissions = []
    impact_value = []
    for i in range(len(impact)):
        emissions.append(impact[i][0])
        impact_value.append(impact[i][1])
    
    # Create the plot
    plt.figure(figsize=(10, 6))
    plt.plot(emissions, impact_value, marker='o', linestyle='-', color='b')
    # Add titles and labels
    plt.title('Relationship between GHG Emissions and Business construction ')
    plt.xlabel('GHG Emissions (tons of CO2)')
    plt.ylabel('Impact Value')

    # Show the plot
    plt.grid(True)
    plt.show()
    


    

getEnvironmentalImpact()