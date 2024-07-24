import pysd 
from pysd.py_backend.output import ModelOutput
import pandas as pd


model = pysd.read_vensim('testing_dumb.mdl', split_views=True)

model1 = model.select_submodel(vars = ['v1', 'variable1','variable2'], inplace=False)
model2 = model.select_submodel(vars = ['variable2', 'variable3'],
                               exogenous_components={ 'variable1':1}
                               , inplace=False)

output1 = ModelOutput()
output2 = ModelOutput()
model1.set_stepper(output1,
                  step_vars=["v1"],
                  final_time=5)

model2.set_stepper(output2,
                  step_vars=["variable2"],
                  final_time=5)
temp = model2['variable3'] + 1

for i in range(5):
    model1.step(1,  {'v1' : temp})
    print(model1['variable1'])
    model2.step(1, {'variable2' : model1['variable2']})
    print(model2['variable3'])
    temp = model2['variable3'] + 1


result_df = output1.collect(model1)
result_df2 = output2.collect(model2)
res = result_df.merge(result_df2, on = ['time', 'FINAL TIME', 'INITIAL TIME', 'TIME STEP', 'SAVEPER', 'variable2'], how = 'outer')

print(res)