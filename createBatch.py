import math

class functions():
    def __init__(self):
        import numpy as np
        self.spots = []
    def generate_spots(self, data, index):
        import numpy as np
        self.spots = []
        for i in range(np.shape(data)[0]):
            m = data[i][index]
            print("data", data[i][3:15],index,data[i][index])
            print("index",index)
            print("m",m,type(m))
            if m == 0:
                m = 1
            if m == "nan":
                m = 1
            if math.isnan(m):
                m = 1
            self.spots = np.append(self.spots, list(data[i,1:3].astype('float64')) * int(m))
        self.spots = np.reshape(self.spots, (-1,2))
        return self.spots

class CreateBatch():
    def __init__(self, coord):
        self.grid_size = 0.005
        lat = coord[:,0]
        lon = coord[:,1]
        self.x_left_lower_corner = min(lon)
        self.y_left_lower_corner = min(lat)
        x_right_corner = max(lon)
        y_up_corner = max(lat)
        self.Nx = int(abs(self.x_left_lower_corner - x_right_corner) / self.grid_size) + 1
        self.Ny = int(abs(self.y_left_lower_corner - y_up_corner) / self.grid_size) + 1