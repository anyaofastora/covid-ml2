import pymysql
import pandas as pd
import numpy as np
# df = pd.read_excel("uscities.xlsx")
# print(df)
# data_row = df.iloc[2,:].values
# print(data_row[2])
conn = pymysql.connect(
    host='localhost',
    user='root', password='LRc19980307',
    database='us_metro',
    charset='utf8')
cursor = conn.cursor()
count = 10172
# sql = """
# CREATE TABLE USER1 (
# id INT auto_increment PRIMARY KEY ,
# name CHAR(10) NOT NULL UNIQUE,
# age TINYINT NOT NULL
# )ENGINE=innodb DEFAULT CHARSET=utf8;  #注意：charset='utf8' 不能写成utf-8
# """


def search_column(cursor, table):
    """
    查找数据库所有属性名称
    :param table: 数据库
    :param cursor:指针
    :return:全属性列表（按设计顺序排列）
    """

    sql = "select *from information_schema.COLUMNS where table_name = 'metro' ORDER BY ordinal_position;"
    col = []
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        col.append(row[3])
    # print("searchcol", col)
    return col


def get_comment_dict(cursor, table="compl"):
    """
    查找数据库所有属性的注释
    :param cursor:
    :return:
    """
    if table == "compl":
        cursor.execute('select column_name,column_comment from information_schema.COLUMNS where TABLE_NAME=%s',
                       "pepperdata")
    else:
        cursor.execute('select column_name,column_comment from information_schema.COLUMNS where TABLE_NAME=%s',
                       "pepperbriefdata")
    # print("col", get_columns(cursor2,"pepperdata"))
    return_columns = cursor.fetchall()
    # print(return_columns)
    col_dict = {}
    for col in return_columns:
        col_dict[col[0]] = col[1]
    return col_dict


def get_coord_multi(cities, states, cursor):

    lat = []
    lon = []
    for city in cities:
        for state in states:
            sql = 'select latitude,longtitude from metro where city="%s" and state_id="%s";' % (city, state)
            cursor.execute(sql)
            result = cursor.fetchall()
            print(result,city,state)
            if result != ():
                # print(sql)
                lat.append(result[0][0])
                lon.append(result[0][1])
                # latlist.append(result[0][0])
                # lonlist.append(result[0][1])
    if len(lat) != 0:
        return sum(lat)/len(lat),sum(lon)/len(lon)
    else:
        print("not found",cities,states)
        return 0,0


#
# names = search_column(cursor,"compl")
# col_dict = get_comment_dict(cursor,"compl")
# print("names",names)
# for i in range(len(names)):
#     print(i,names[i],col_dict[names[i]])


#names = ['city', 'city_ascii', 'state_id', 'state_name', 'latitude', 'longtitude', 'population', 'density', 'id',"fips"]
names = ["fips","county","state","lat","lon"]
def insert(row):
    sqlcmd = "INSERT INTO county_fips ("
    for k in range(len(names)-1):
        sqlcmd = sqlcmd + str(names[k]) + ","
    sqlcmd = sqlcmd + str(names[len(names)-1])+") VALUES ("
    for k in range(0,4):
        sqlcmd = sqlcmd + "'"
        row[k] = str(row[k]).replace("'", "\\'")
        sqlcmd = sqlcmd+row[k] + "',"
    # row[len(row)-2] = str(row[len(row)-2]).replace("'", "\\'")
    # sqlcmd = sqlcmd + row[len(row)-2] + ","
    sqlcmd = sqlcmd + "'"
    row[len(row)-1] = str(row[len(row)-1]).replace("'", "\\'")
    sqlcmd = sqlcmd + row[len(row)-1] + "');"
    print(sqlcmd)
    cursor.execute(sqlcmd)
    conn.commit()



# df = pd.read_excel("C:/Users/Li Runchao/PycharmProjects/pepper/2000-2010.xlsx")
# for i in range(1,173):
#     data_row = df.iloc[i,:].values
#     insert(data_row,count,2000)
#     count += 1
#
# df = pd.read_excel("C:/Users/Li Runchao/PycharmProjects/pepper/2010-2020.xlsx")
# for i in range(1,219):
#     data_row = df.iloc[i,:].values
#     insert(data_row,count,2010)
#     count += 1
#df = pd.read_excel("C:/Users/Li Runchao/PycharmProjects/pepper/2018.xlsx")
# for i in range(1,42):
#     data_row = df.iloc[i,:].values
#     insert_test_data(data_row,count,2018)
#     count += 1

# df = pd.read_excel("C:/Users/Li Runchao/PycharmProjects/pepper/2020.xlsx")
# for i in range(2,38):
#     data_row = df.iloc[i,:].values
#     insert_test_data(data_row,count,2020)
#     count += 1

if __name__ == "__main__":
    insert([69100, "Rota Municipality", "MP",14.153611,145.203056])
    insert([69110, "Saipan Municipality", "MP",15.183333,145.75])
    insert([69120, "Tinian Municipality", "MP",15.029,145.616])
    insert([72001, "Adjuntas Municipio", "PR",18.162778,-66.722222])
    insert([72003, "Aguada Municipio", "PR",18.379444,-67.188333])
    insert([72005, "Aguadilla Municipio", "PR",18.43,-67.154444])
    insert([72007, "Aguas Buenas Municipio", "PR",18.256944,-66.103056])
    insert([72009, "Aibonito Municipio", "PR",18.14,-66.266111])
    insert([72011, "Añasco Municipio", "PR",18.316111,-67.139722])
    insert([72013, "Arecibo Municipio", "PR",18.375,-66.625])
    insert([72015, "Arroyo Municipio", "PR",17.965833,-66.061389])
    insert([72017, "Barceloneta Municipio", "PR",18.450556,-66.538611])
    insert([72019, "Barranquitas Municipio", "PR",18.186667,-66.306389])
    insert([72021, "Bayamón Municipio", "PR",18.38,-66.163333])
    insert([72023, "Cabo Rojo Municipio", "PR",18.086667,-67.145833])
    insert([72025, "Caguas Municipio", "PR",18.231389,-66.039444])
    insert([72027, "Camuy Municipio", "PR",18.483889,-66.845])
    insert([72029, "Canóvanas Municipio", "PR",18.379167,-65.901389])
    insert([72031, "Carolina Municipio", "PR",18.406111,-65.967222])
    insert([72033, "Cataño Municipio", "PR",18.445,-66.117778])
    insert([72035, "Cayey Municipio", "PR",18.111667,-66.165833])
    insert([72037, "Ceiba Municipio", "PR",18.238056,-65.627778])
    insert([72039, "Ciales Municipio", "PR",18.336173,-66.468875])
    insert([72041, "Cidra Municipio", "PR",18.175833,-66.161389])
    insert([72043, "Coamo Municipio", "PR",18.08,-66.358056])
    insert([72045, "Comerío Municipio", "PR",18.218056,-66.226111])
    insert([72047, "Corozal Municipio", "PR",18.341667,-66.316944])
    insert([72049, "Culebra Municipio", "PR",18.316944,-65.29])
    insert([72051, "Dorado Municipio", "PR",18.458889,-66.267778])
    insert([72053, "Fajardo Municipio", "PR",18.325833,-65.6525])
    insert([72054, "Florida Municipio", "PR",18.363611,-66.571389])
    insert([72055, "Guánica Municipio", "PR",17.971667,-66.908056])
    insert([72057, "Guayama Municipio", "PR",17.974167,-66.11])
    insert([72059, "Guayanilla Municipio", "PR",18.019167,-66.791944])
    insert([72061, "Guaynabo Municipio", "PR",18.366667,-66.1])
    insert([72063, "Gurabo Municipio", "PR",18.254444,-65.973056])
    insert([72065, "Hatillo Municipio", "PR",18.486389,-66.825556])
    insert([72067, "Hormigueros Municipio", "PR",18.139722,-67.1275])
    insert([72069, "Humacao Municipio", "PR",18.149722,-65.8275])
    insert([72071, "Isabela Municipio", "PR",18.513056,-67.07])
    insert([72073, "Jayuya Municipio", "PR",18.218611,-66.591667])
    insert([72075, "Juana Díaz Municipio", "PR",18.0525,-66.506667])
    insert([72077, "Juncos Municipio", "PR",18.2275,-65.921111])
    insert([72079, "Lajas Municipio", "PR",18.05194,-67.05972])
    insert([72081, "Lares Municipio", "PR",18.295,-66.878611])
    insert([72083, "Las Marías Municipio", "PR",18.251389,-66.993333])
    insert([72085, "Las Piedras Municipio", "PR",18.183056,-65.866389])
    insert([72087, "Loíza Municipio", "PR",18.419722,-65.873056])
    insert([72089, "Luquillo Municipio", "PR",18.3725,-65.716667])
    insert([72091, "Manatí Municipio", "PR",18.4325,-66.484444])
    insert([72093, "Maricao Municipio", "PR",18.180833,-66.98])
    insert([72095, "Maunabo Municipio", "PR",18.006944,-65.899167])
    insert([72097, "Mayagüez Municipio", "PR",18.201111,-67.139722])
    insert([72099, "Moca Municipio", "PR",18.394722,-67.113333])
    insert([72101, "Morovis Municipio", "PR",18.333333,-66.416667])
    insert([72103, "Naguabo Municipio", "PR",18.219444,-65.736667])
    insert([72105, "Naranjito Municipio", "PR",18.300833,-66.245])
    insert([72107, "Orocovis Municipio", "PR",18.226944,-66.391111])
    insert([72109, "Patillas Municipio", "PR",18.006389,-66.015833])
    insert([72111, "Peñuelas Municipio", "PR",18.059444,-66.7225])
    insert([72113, "Ponce Municipio", "PR",18.001717,-66.606662])
    insert([72115, "Quebradillas Municipio", "PR",18.466357,-66.927603])
    insert([72117, "Rincón Municipio", "PR",18.33898,-67.250771])
    insert([72119, "Río Grande Municipio", "PR",18.376369,-65.798434])
    insert([72121, "Sabana Grande Municipio", "PR",18.084483,-66.947609])
    insert([72123, "Salinas Municipio", "PR",17.971485,-66.262252])
    insert([72125, "San Germán Municipio", "PR",18.1078,-67.037263])
    insert([72127, "San Juan Municipio", "PR",18.422249,-66.069081])
    insert([72129, "San Lorenzo Municipio", "PR",18.147107,-65.976167])
    insert([72131, "San Sebastián Municipio", "PR",18.331064,-66.969064])
    insert([72133, "Santa Isabel Municipio", "PR",17.952922,-66.387588])
    insert([72135, "Toa Alta Municipio", "PR",18.364556,-66.244669])
    insert([72137, "Toa Baja Municipio", "PR",18.45691,-66.193193])
    insert([72139, "Trujillo Alto Municipio", "PR",18.335387,-66.003787])
    insert([72141, "Utuado Municipio", "PR",18.270865,-66.702989])
    insert([72143, "Vega Alta Municipio", "PR",18.43622,-66.336412])
    insert([72145, "Vega Baja Municipio", "PR",18.455128,-66.397883])
    insert([72147, "Vieques Municipio", "PR",18.125418,-65.432474])
    insert([72149, "Villalba Municipio", "PR",18.130718,-66.472244])
    insert([72151, "Yabucoa Municipio", "PR",18.059858,-65.859871])
    insert([72153, "Yauco Municipio", "PR",18.085669,-66.857901])

    # with open("county_coord.txt",encoding="utf-8") as f:
    #     data = f.readlines()
    # for i in data:
    #     data_split = i.split("\t")
    #     print(data_split)
    #     lon = data_split[13].strip("-")
    #     print(lon.strip("\n").strip("°"))
    #     insert([data_split[2],data_split[3],data_split[1],float(data_split[12].strip("+").strip("°")),data_split[13].strip("\n").strip("°").replace("–","-")])


# df = pd.read_excel("list1_2020.xlsx")
# fips = []
# for i in range(0,1916):
#     data_row = df.iloc[i,:].values
#     citystate = data_row[3]
#     city = citystate.split(", ")[0]
#     state = citystate.split(", ")[1]
#     city_list = []
#     state_list = []
#     if data_row[0] not in fips:
#         if "-" in city:
#             for i in city.split("-"):
#                 city_list.append(i)
#         else:
#             city_list.append(city)
#         if "-" in state:
#             for i in state.split("-"):
#                 state_list.append(i)
#         else:
#             state_list.append(state)
#         lat,lon = get_coord_multi(city_list,state_list,cursor)
#         fips.append(data_row[0])
#         row = [data_row[0],city,state,lat,lon]
#         print(row)
#         insert(row)


cursor.close()
# 关闭数据库连接
conn.close()