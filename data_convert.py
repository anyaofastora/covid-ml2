import pandas as pd
import numpy as np
import pymysql
import urllib.request
from crawler import dataConverter_daily_county, dataConverter_daily_metro
#from crawler import dataConverter_daily
from datetime import date
import pysftp

conn = pymysql.connect(
    host='localhost',
    user='root', password='LRc19980307',
    database='us_metro',
    charset='utf8')
cursor = conn.cursor()


def is_added_year(year):
    if year%4 == 0:
        return 366
    else:
        return 365

def number_to_date(num):
    # print(num)
    for i in range(2020,2100):
        if num - is_added_year(i) < 0:
            break
        else:
            num = num - is_added_year(i)
    year = i
    if year%4 == 0:
        leap = 1
    else:
        leap = 0
    num += year-2020
    if num == 365+leap:
        year += 1
        num = 1
    # print(num)
    month_list = [31,28+leap,31,30,31,30,31,30,30,31,30,31]
    for i in range(12):
        if num - month_list[i] <= 0:
            break
        else:
            num -= month_list[i]
    month = i+1
    if month < 10:
        month = "0" + str(month)
    else:
        month = str(month)
    date = num
    if date < 10:
        date = "0" + str(date)
    else:
        date = str(date)
    return str(year) + "-" + month + "-" + date


def get_daily_data():
    from datetime import date
    datetoday = date.today().strftime("%Y-%m-%d")
    urllib.request.urlretrieve("https://api.covidactnow.org/v2/cbsas.csv?apiKey=8a4c770f9e9f4c8fb1ba252374ab4711","./daily/"+datetoday+"cbsas.csv")


def get_state_cbsas_data():
    urllib.request.urlretrieve("https://api.covidactnow.org/v2/cbsas.timeseries.csv?apiKey=8a4c770f9e9f4c8fb1ba252374ab4711","cbsas.timeseries.csv")
    urllib.request.urlretrieve("https://api.covidactnow.org/v2/states.timeseries.csv?apiKey=8a4c770f9e9f4c8fb1ba252374ab4711","states.timeseries.csv")


def date_to_number(date):
    time = date.split("-")
    year = time[0]
    month = time[1]
    day = time[2]
    if int(year)%4 == 0:
        leap_year = 1
    else:
        leap_year = 0
    year_day = [365,366]
    month_day = [31,28+leap_year,31,30,31,30,31,31,30,31,30,31]
    result = 0
    for i in range(int(year)-2020):
        if i % 4 == 0:
            leap = 1
        else:
            leap= 0
        result += year_day[leap]
    for i in range(int(month)-1):
        result += month_day[i]
    result += int(day)
    return result


def convert_metro_daily():
    ##########DAILY##################
    from datetime import date
    datetoday = date.today().strftime("%Y-%m-%d")
    df = pd.read_csv("./daily/"+datetoday+"cbsas.csv")
    df = df.values
    date_list = [datetoday]*df.shape[0]
    # print(date_list)
    fips_list = df[:, 0]
    case_list = df[:, 38]
    print(type(fips_list))
    fips_unique = np.unique(fips_list)
    data = fips_unique
    coord = []
    for i in fips_unique:
        sql = "select latitude,longitude, city,state from metro_fips where fips = %s" % (str(i))
        cursor.execute(sql)
        result = cursor.fetchall()[0]
        # print(result)
        coord.append(list(result))
    print(coord)
    print(data)
    data = np.append(data.reshape(-1, 1), np.array(coord), axis=1)

    census = pd.read_csv('us_metro_confirmed_cases_cdl.csv')
    census = census.values
    # census_data = []
    data = np.append(data, np.multiply(np.ones([data.shape[0], 10]), 20000), axis=1)
    k = 1
    for i in range(len(fips_unique)):
        for k in range(census.shape[0]):
            if fips_unique[i] == census[k][0]:
                for j in range(5, 15):
                    data[i][j] = census[k][j - 3]
    # print(len(census_data))
    # data = np.append(data, np.array(census_data),axis=1)
    data = np.append(data, np.zeros([data.shape[0], 1000]), axis=1)
    print(data)
    for i in range(fips_list.shape[0]):
        # print(fips_list[i])
        location = np.argwhere(fips_unique == fips_list[i])
        data[location[0][0]][date_to_number(date_list[i]) + 14] = 0 if pd.isnull(case_list[i]) else case_list[i]
        # print(location)
        # print(data[location[0]][0])
    data = pd.DataFrame(data)
    print(data)
    data.to_csv("cbsasdata.csv", index_label=False, index=False)


def convert_metro():
    df = pd.read_csv("cbsas.timeseries.csv")
    df = df.values
    date_list = df[:,0]
    #print(date_list)
    fips_list = df[:,4]
    case_list = df[:,21]
    print(type(fips_list))
    fips_unique = np.unique(fips_list)
    data = fips_unique.reshape(-1,1)
    coord = []
    for i in fips_unique:
        sql = "select latitude,longitude,city,state from metro_fips where fips = %s" % (str(i))
        cursor.execute(sql)
        result = cursor.fetchall()[0]
        #print(result)
        coord.append(list(result))
    print(coord)
    print(data)
    data = np.append(data, np.array(coord), axis=1)

    census =  pd.read_csv('us_metro_confirmed_cases_cdl.csv')
    census = census.values
    #census_data = []
    data = np.append(data, np.multiply(np.ones([data.shape[0], 10]),20000), axis=1)
    k = 1
    for i in range(len(fips_unique)):
        for k in range(census.shape[0]):
            if fips_unique[i] == census[k][0]:
                for j in range(5,15):
                    data[i][j] = census[k][j-3]
    #print(len(census_data))
    #data = np.append(data, np.array(census_data),axis=1)
    data = np.append(data, np.zeros([data.shape[0],1000]),axis=1)
    print(data)
    for i in range(fips_list.shape[0]):
        #print(fips_list[i])
        location = np.argwhere(fips_unique == fips_list[i])
        data[location[0][0]][date_to_number(date_list[i])+14] = 0 if pd.isnull(case_list[i]) else case_list[i]
        #print(location)
        #print(data[location[0]][0])

    ##########DAILY##################
    from datetime import date
    datetoday = date.today().strftime("%Y-%m-%d")
    df = pd.read_csv("./daily/"+datetoday+"cbsas.csv")
    df = df.values
    date_list = [datetoday]*df.shape[0]
    # print(date_list)
    fips_list = df[:, 0]
    case_list = df[:, 38]
    date_number = date_to_number(datetoday) + 14 - 1  # the daily update is yesterday's data
    for i in range(len(case_list)):
        data[i][date_number] = case_list[i]
        print(i,case_list[i])
    #print(type(fips_list))


    data = pd.DataFrame(data)
    print(data)
    data.to_csv("cbsasdata.csv", index_label=False,index=False)
    return datetoday


def convert_state():
    df = pd.read_csv("states.timeseries.csv")
    df = df.values
    date_list = df[:,0]
    #print(date_list)
    fips_list = df[:,4]
    state_list = df[:,2]
    case_list = df[:,21]
    #print(type(fips_list))
    fips_unique = np.unique(fips_list)
    state_unique = np.unique(state_list)
    data = fips_unique.reshape(-1,1)

    census =  pd.read_csv('us_state_confirmed_case.csv')
    census = census.values
    #census_data = []
    data = np.append(data,state_unique.reshape(-1,1),axis=1)
    data = np.append(data, np.zeros([data.shape[0], 10]), axis=1)
    k = 1
    for i in range(len(fips_unique)):
        for k in range(census.shape[0]):
            if fips_unique[i] == census[k][0]:
                for j in range(2, 12):
                    data[i][j] = census[k][j]
    #print(len(census_data))
    #data = np.append(data, np.array(census_data),axis=1)
    data = np.append(data, np.zeros([data.shape[0],1000]),axis=1)
    print(data)
    for i in range(date_list.shape[0]):
        #print(fips_list[i])
        location = np.argwhere(fips_unique == fips_list[i])
        data[location[0][0]][date_to_number(date_list[i])+11] = 0 if pd.isnull(case_list[i]) else case_list[i]
        #print(location)
        #print(data[location[0]][0])
    data = pd.DataFrame(data)
    print(data)
    data.to_csv("statedata.csv",index_label=False,index=False)


def sort_state():
    df = np.array(pd.read_csv("cbsasdata.csv"))
    state_list = df[:, 4]
    #print(state_list)
    state_data = []
    state_enum = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID",
                              "IL", "IN", "IA", "KS", "KY", "LA",
                              "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC",
                              "ND", "OH", "OK",
                              "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    state_data = {}
    for state in range(len(state_enum)):
        state_data[state_enum[state]] = []
    for state in range(len(state_enum)):
        for i in range(len(state_list)):
            if state_list[i].find(state_enum[state]) != -1:
                #print(state_list[i],state_enum[state])
                state_data[state_enum[state]].append(df[i])
    for state in range(len(state_enum)):
        result = pd.DataFrame(state_data[state_enum[state]])
        result.to_csv("./State/%s.csv" % (state_enum[state]),index_label=False,index=False)


def daily_update_metro():
    get_daily_data()
    get_state_cbsas_data()
    convert_state()
    today = convert_metro()
    sort_state()
    dataConverter_daily_metro(today)
    return today


if __name__ == "__main__":
    # print(date_to_number("2022-1-12"))
    daily_update_metro()
    # for i in range(733):
    #     print(number_to_date(i))
    # print(number_to_date(date_to_number(date.today().strftime("%Y-%m-%d")) - 3))
    # print(number_to_date(+41-15))