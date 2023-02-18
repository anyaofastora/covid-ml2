import tensorflow as tf
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import json
from ftp import transfer
from date_proc import *
state_enum = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
              "IL", "IN", "IA", "KS", "KY", "LA",
              "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
              "ND", "OH", "OK",
              "OR", "PA", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WV", "WI", "WY"]

def get_training_data(state,start_date,end_date):
    """
    obtain training data
    :param date_num:number
    :return: data
    """
    df = pd.read_csv("./State/"+state+".csv")
    df = df.values
    data = df[:,start_date:end_date]
    data = MinMaxScaler().fit(data).transform(data)
    fips_list = df[:,0].squeeze()
    return data.T.tolist(),fips_list


def gru_run(data):
    with tf.device('/CPU:0'):
        input = [0]
        input[0] = data
        input = np.array(input)
        length = input.shape[2]
        #print("len")
        input = tf.convert_to_tensor(input)
        gru = tf.keras.layers.GRU(length)
        final_out = gru(input)
        #print(final_out)
        final_out = final_out.numpy().reshape(-1,1)
        #print(type(final_out))
        #print(final_out)
        #final_out = final_out+2
        final_out = MinMaxScaler().fit_transform(final_out)

    return final_out.squeeze()


def update_predict(date):
    date = date+15+11
    #print(number_to_date(852))
    startdate = date-41
    enddate = date-1
    result = {}
    for state in state_enum:
        #print(state)
        data, fips_list = get_training_data(state, startdate, enddate)
        output = gru_run(data)
        #print(fips_list.shape, output.shape)
        for i in range(len(fips_list)):
            result[str(fips_list[i])] = str(output[i])
        with open("./predicted/%s.json" % (number_to_date(date)), 'w+', encoding='utf-8') as json_file:
            json.dump(result, json_file, ensure_ascii=False)
    transfer("predicted\\%s.json" % (number_to_date(date)),"predicted")






if __name__ == "__main__":

    #print(data)
    #print(gru_run(data))
    update_predict(855)