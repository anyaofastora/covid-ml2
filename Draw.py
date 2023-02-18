from createBatch import CreateBatch
from dnn import dnn_model
from KDE import KDE_extractor
import numpy as np
from data_convert import number_to_date
import pandas as pd
from array import array
import pickle
from ftp import transfer

def Draw_Predicted_Results(data_coord, model, K, time_index, state,datenum):
    from sklearn.preprocessing import MinMaxScaler
    date = number_to_date(datenum)
    batch = CreateBatch(data_coord)
    print(batch)

    # from mpl_toolkits.basemap import Basemap
    #from sklearn.datasets.species_distributions import construct_grids

    xgrid, ygrid = construct_grids(batch)
    X, Y = np.meshgrid(xgrid[::5], ygrid[::5][::-1])
    xy = np.vstack([Y.ravel(), X.ravel()]).T
    xy = np.radians(xy)

    from sklearn.neighbors import KernelDensity
    import matplotlib.pyplot as plt

    # fig, ax = plt.subplots(1, 2, figsize=(20, 20))
    # fig.subplots_adjust(left=0.05, right=0.95, wspace=0.05)
    # species_names = ['Ohio Hotspot', 'Predicted Risk Hotspot Map']
    # cmaps = ['Purples', 'Reds']
    # #
    # for i, axi in enumerate(ax):
    #     axi.set_title(species_names[i])

    # plot coastlines with basemap
    # m = Basemap(projection='cyl', llcrnrlat=Y.min(),
    #             urcrnrlat=Y.max(), llcrnrlon=X.min(),
    #             urcrnrlon=X.max(), resolution='c', ax=axi)
    # # m.drawmapboundary(fill_color='#DDEEFF')
    # # m.drawcoastlines()
    # # m.drawcountries()
    # m.drawmapboundary(fill_color='aqua')
    # # m.fillcontinents(color='coral',lake_color='aqua')
    # m.drawcoastlines()
    # m.readshapefile('/Users/qianlongwang/Downloads/tl_2017_us_county/tl_2017_us_county', 'tl_2017_us_county')

    # construct a spherical kernel density estimate of the distribution
    #     kde = KernelDensity(bandwidth=0.006, metric='haversine')
    #     kde.fit(np.radians(data_coord))

    # evaluate only on the land: -9999 indicates ocean
    '''
    Z = np.full(land_mask.shape[0], -9999.0)
    Z[land_mask] = np.exp(kde.score_samples(xy))
    Z = Z.reshape(X.shape)
    '''

    #     Z = np.exp(kde.score_samples(xy))
    #     Z = Z.reshape(X.shape)

    DNN_input = K.f_generator(xy, time_index)
    DNN_input = np.append(DNN_input[:, 0:2], DNN_input[:, -5:], axis=1)
    DNN_input = MinMaxScaler().fit(DNN_input).transform(DNN_input)

    DNN_output = model.predict(DNN_input)
    Z = DNN_output

    Z = Z.reshape(X.shape)

    output = np.append(X.reshape(-1,1),Y.reshape(-1,1),axis=1)
    Z = MinMaxScaler().fit(Z).transform(Z)
    print("Zshape", np.shape(Z))

    Z = Z.reshape(-1,1)
    Z = np.power(np.power(2,Z),2) #30 5

    Z = MinMaxScaler().fit(Z).transform(Z)
    #Z = np.sqrt(Z)
    Z = np.multiply(Z,0.8)
    print("Zshape", np.shape(Z))
    for i in range(np.shape(Z)[0]):
        #print("Z",i*np.shape(Z)[1]+j,Z[i][0])
        if Z[i][0] <= 0.000002:
            #print("is 0")
            Z[i][0] = 0.000002
    #output = np.append(output,Z,axis=1)
    # row, col = np.shape(output)
    # output = list(output.reshape(1,-1))
    # output.append(row)
    # output.append(col)
    #output = np.append(output,np.divide(np.power(np.power(30,Z.reshape(-1,1)),3),10),axis=1)
    np.set_printoptions(suppress=True)
    # fp = open("./heatmap/"+state+"_2021-12-27.txt", 'wb')
    # array("d", output).tofile(fp)
    pickle.dump(output, open("./coordinates/" + state, "wb"))
    pickle.dump(Z, open("./heatmap/"+state+'_' + date, "wb"))
    transfer("heatmap\\"+state+'_' + date, "heatmap")
    #
    # plot contours of the density
    #     levels = np.linspace(0, Z.max(), 50)(X, Y, Z, levels=levels, cmap=cmaps[i])
#     #
#     # plt.show()
    #     axi.contourf


def construct_grids(batch):  # 这个函数在现在版本的sklearn中被废弃了，从网上找到了以前的源码
    """Construct the map grid from the batch object

    Parameters
    ----------
    batch : Batch object
        The object returned by :func:`fetch_species_distributions`

    Returns
    -------
    (xgrid, ygrid) : 1-D arrays
        The grid corresponding to the values in batch.coverages
    """
    # x,y coordinates for corner cells
    xmin = batch.x_left_lower_corner + batch.grid_size
    xmax = xmin + (batch.Nx * batch.grid_size)
    ymin = batch.y_left_lower_corner + batch.grid_size
    ymax = ymin + (batch.Ny * batch.grid_size)

    # x coordinates of the grid cells
    xgrid = np.arange(xmin, xmax, batch.grid_size)
    # y coordinates of the grid cells
    ygrid = np.arange(ymin, ymax, batch.grid_size)

    return xgrid, ygrid