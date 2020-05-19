# This script generates the scoring file
# with the init and run functions needed to 
# operationalize the anomaly detection sample

import pickle
import json
import pandas
from sklearn.externals import joblib
from sklearn.linear_model import Ridge
from azureml.core.model import Model

def init():
    global model
    # this is a different behavior than before when the code is run locally, even though the code is the same.
    model_path = Model.get_model_path('model.pkl')
    # deserialize the model file back into a sklearn model
    model = joblib.load(model_path)
    
input_sample = pd.DataFrame(data=[{
    "Activity(steps/hr)": 186.0,
    "ActivityDeviation(%)": -11.0,
    "Yield(gr)": 11226.0,
    "YieldDeviation(%)": -15.0,
    "Fat(%)": 4.09,
    "FatDeviation(%)": 7.0,
    "Protein(%)": 2.64,
    "ProteinDeviation(%)": -8.0,
    "Lactose(%)": 4.96,
    "LactoseDeviation(%)": 3.0,
    "Conductivity": 8.3,
    "ConductivityDeviation(%)": -2.0,
    "SCC (*1000/ml)": 26363.0,
    "Blood(%)": 0.03,
    "ProductionRate(gr/hr)": 1528.0
}])
output_sample = np.array([0.9974, 0.0026])

# note you can pass in multiple rows for scoring
def run(input_str):
    try:
        result = model.predict(data)
        # You can return any data type, as long as it is JSON serializable.
        print("Prediction is ", result[0])
        return result.tolist()
#         input_json = json.loads(input_str)
#         input_df = pandas.DataFrame([[input_json['machine']['temperature'],input_json['machine']['pressure'],input_json['ambient']['temperature'],input_json['ambient']['humidity']]])
#         pred = model.predict(input_df)
#         print("Prediction is ", pred[0])
    except Exception as e:
        result = str(e)
        
    if pred[0] == 1:
        input_json['anomaly']=True
    else:
        input_json['anomaly']=False
        
    return [json.dumps(input_json)]
