from KDE import KDE_extractor
from dnn import dnn_model
from Draw import Draw_Predicted_Results
from data_convert import date_to_number
from numba import jit
#Main
import pandas as pd
from data_convert import daily_update_metro
from county_data_convert import daily_update_county
import os
from gru import update_predict
from crawler import history_data
state_enum = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
              "IL", "IN", "IA", "KS", "KY", "LA",
              "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
              "ND", "OH", "OK",
              "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WV", "WI", "WY"]
#state_enum = ["OH"] # not for numba
'''We first test different bandwidth.'''
bandwidth = [0.002, 0.004, 0.006, 0.008, 0.010, 0.012, 0.014, 0.016]
#bandwidth = [0.006]



@jit
def run(num):
    startdate = num
    for state in state_enum:
        K = KDE_extractor()
        print('******************************* For state:', state)
        print('*******************************')
        K.build(startdate, startdate+41, state, KDE_bandwidth=0.006)
        training_samples = K.generate_training_samples()
        df = pd.DataFrame(training_samples)
        df.to_csv('TrainingSample_XY_3.csv')
        d = dnn_model()
        d.run_regression(epochs = 150)
        time_index = 40
        Draw_Predicted_Results(K.data_coord, d.model_reg, K, time_index,state,startdate+41-15)

# confirmed = pd.read_csv('confirmed_2.csv').values
# x = confirmed[:, -1]  # lon
# y = confirmed[:, -2]  # lat
# print(x)
# print(y)
# K = KDE_extractor()
# K.build()
#
# training_samples = K.generate_training_samples()
# df = pd.DataFrame(training_samples)
# df.to_csv('TrainingSample_XY_3.csv')
# # So far training samples generated, next we train the DNN.
# d = dnn_model()`
# d.run_regression(epochs=150)
# Model trained, next we print out the hotspot map of predicted result.
# for i in range(41):
#     print('Draw hotspot map of predicted risk level for time index:', i)
#     Draw_Predicted_Results(K.data_coord, d.model_reg, i)
#     # Compared with the owned metroplolitan data
#     print('This is the display of the owned metropolitan confirmed case data at time index:', i)
#     c = confirmed[:, -3 - 40 + i]
#     show_coord_vs_value(x, y, c)

#716 2022-1-13
#735 2022-2-1
#763 2022-3-1
#794 2022-4-1
#824 2022-5-1
#855 2022-6-1
#885 2022-7-1
#916 2022-8-1
if __name__ == "__main__":

    try:
        os.remove("cbsas.timeseries.csv")
    except:
        pass
    try:
        os.remove("states.timeseries.csv")
    except:
        pass

    daily_update_metro()
    daily_update_county()
    history_data()
    date = 929
    dist = 14
    for i in range(date,date+dist):
        run(i)
        try:
            os.remove("./heatmap/desktop.ini")
        except:
            pass
    for i in range(date,date+dist):
        update_predict(i)

    # for i in range(3):
    #     run(716-i)