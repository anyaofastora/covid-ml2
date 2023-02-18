from createBatch import functions
from numba import int32, float32    # import the types

class KDE_extractor():
    def build(self, ccis,ccie,state,KDE_bandwidth=0.006, KDE_metric='haversine', KDE_kernel='gaussian'):
        import pandas as pd
        import numpy as np
        # from mpl_toolkits.basemap import Basemap
        # from sklearn.datasets.species_distributions import construct_grids
        from sklearn.neighbors import KernelDensity
        import matplotlib.pyplot as plt
        import copy
        self.ccis = ccis
        self.ccie = ccie
        self.state = state
        df = pd.read_csv('statedata.csv')
        self.state_confirmed = df.values
        for i, ele in enumerate(self.state_confirmed[:, 1]):
            if ele == state:
                row = i
        # pick time slots 4/1 to 5/11 in Ohio
        # self.state_confirmed = self.state_confirmed[row, 83:124].reshape(-1, 1)
        self.state_confirmed = self.state_confirmed[row, self.ccis:self.ccie].reshape(-1, 1)

        metro_confirmed = pd.read_csv('./State/'+state+'.csv')
        #print(metro_confirmed)
        metro_confirmed = metro_confirmed.values
        self.data_len = np.shape(metro_confirmed)[0]
        metro_confirmed_copy = copy.copy(metro_confirmed)
        extracted_feature = metro_confirmed[:, 1:3].astype('float64')
        #print(np.shape(extracted_feature))
        self.data_coord = extracted_feature
        self.radians = np.radians(extracted_feature)

        '''
        Normalize census data
        '''
        self.metro_confirmed = copy.copy(metro_confirmed_copy)
        mini = np.array(self.metro_confirmed[:, 5:15]).min()
        i = len(str(mini)) - 1
        self.metro_confirmed[:, 5:15] = np.divide(self.metro_confirmed[:, 5:15], 10 ** i).astype(int)

        f = functions()
        # spots = f.generate_spots(self.metro_confirmed, -3)
        # print(np.shape(spots))
        #
        self.extracted_feature_census = extracted_feature
        self.extracted_feature_confirmed_case = extracted_feature
        #
        # self.KDE_extractors = []

        #        for i in list(range(3,13)) + list(range(83, 124)):
        self.KDE_extractors = []
        for i in list(range(5, 15)) + list(range(self.ccis, self.ccie)):
            print('Creating feature map with KDE, for column ', i)
            spots = f.generate_spots(self.metro_confirmed, i)
            data_coord = spots
            print("train",np.shape(data_coord))
            #print(data_coord)
            kde = KernelDensity(kernel=KDE_kernel, bandwidth=KDE_bandwidth, metric=KDE_metric)
            kde.fit(np.radians(data_coord))

            self.KDE_extractors.append(kde)

            print("radian",np.shape(self.radians))
            #print(self.radians)
            results = np.exp(kde.score_samples(self.radians))
            results = np.reshape(results, (len(results), 1))

            if i < 15:
                self.extracted_feature_census = np.append(self.extracted_feature_census, results, axis=1)
            else:
                self.extracted_feature_confirmed_case = np.append(self.extracted_feature_confirmed_case, results,
                                                                  axis=1)

    def f_generator(self, coords, time_index):
        import numpy as np
        x = coords
        radians = x
        # radians = np.radians(coords)
        for i in range(0, 10):
            results = np.exp(self.KDE_extractors[i].score_samples(radians)).reshape(-1, 1)
            x = np.append(x, results, axis=1)

        x = np.append(x, [[time_index]] * len(x), axis=1)
        results = np.exp(self.KDE_extractors[10 + time_index].score_samples(radians)).reshape(-1, 1)
        x = np.append(x, results, axis=1)
        x = np.append(x, [[int(self.state_confirmed[time_index])]] * len(x), axis=1)
        x = np.append(x, np.multiply(x[:, -1], x[:, -2]).reshape(-1, 1), axis=1)

        return x

    def RiskLabel(value):
        import numpy as np
        from sklearn.preprocessing import MinMaxScaler
        c = value
        c = c.reshape(-1, 1)
        size = MinMaxScaler().fit(c).transform(c)
        # print(size)
        size = (size + 1) * 1.5
        size = np.log(size)
        for i in range(len(size)):
            if size[i] > 1:
                size[i] = 1
        # size = MinMaxScaler().fit(size).transform(size)
        return size

    def generate_training_samples(self):
        import numpy as np
        import pandas as pd
        import copy
        '''
        Make training samples. Each row is a training sample 'x', first two columns are coordinate, last two are time index
        and confirmed case feature extracted by KDE of that time index. 
        '''
        training_samples_x = []
        row_length = np.shape(self.extracted_feature_census)[1] + 2
        #        row_length, np.shape(self.extracted_feature_census)

        for i in range(np.shape(self.extracted_feature_census)[0]):
            for j in range(np.shape(self.extracted_feature_confirmed_case)[1]):
                if j >= 2:
                    training_samples_x = np.append(training_samples_x, self.extracted_feature_census[i])
                    training_samples_x = np.append(training_samples_x, j - 2)
                    training_samples_x = np.append(training_samples_x, self.extracted_feature_confirmed_case[i, j])

        training_samples_x = np.reshape(training_samples_x, (-1, row_length))
        print(training_samples_x.shape)
        print(training_samples_x)

        '''
        Now, we start to label the risk level for each sample x. 
        '''

        from sklearn.preprocessing import MinMaxScaler

        # concerned_cases = copy.deepcopy(self.metro_confirmed[:,83:124])
        concerned_cases = copy.deepcopy(self.metro_confirmed[:, self.ccis:self.ccie])

        concerned_case_ = MinMaxScaler().fit(concerned_cases).transform(concerned_cases)
        print(concerned_case_)

        #         shape1 = concerned_case_.shape

        #         #np.max(concerned_case_[1, :]), np.max(concerned_cases)
        #         concerned_case_ = concerned_case_.reshape(1, -1)
        #         print(concerned_case_[0])
        #         for i, ele in enumerate(concerned_case_[0]):
        #             if ele < 0.5:
        #                 concerned_case_[0,i] *= 2
        #         concerned_case_ = concerned_case_.reshape(shape1)

        #         risk_label_2 = (concerned_case_*10).astype(float)
        #         #pd.DataFrame(risk_label_2).to_csv('Risk_Label_2.csv')

        # New risk labeling method.
        concerned_case_ = concerned_case_.reshape(1, -1)
        risk = (concerned_case_ + 1) * 1.5
        risk = np.log(risk)
        for i in range(len(risk[0])):
            if risk[0, i] > 1:
                risk[0, i] = 1
        # size = MinMaxScaler().fit(size).transform(size)

        training_sample_xy = np.append(training_samples_x, risk.reshape(-1, 1), axis=1)

        '''
        df = pd.read_csv('us_state_confirmed_case.csv')
        state_confirmed = df.values
        for i, ele in enumerate(state_confirmed[:,1]):
            if ele == 'Ohio':
                row = i
        #pick time slots 4/1 to 5/11 in Ohio
        state_confirmed = state_confirmed[row, 83:124].reshape(-1, 1)
        state_confirmed.shape
        '''
        state_confirmed_2 = np.reshape(([self.state_confirmed, ] * self.data_len), (-1, 1)).astype(int)
        # state_confirmed_2.shape, state_confirmed_2
        training_sample_xy_2 = np.insert(training_sample_xy, -1, state_confirmed_2.T, axis=1)
        # Further add a feature by multiplying kde output and current state info.
        f_add = state_confirmed_2.T * training_sample_xy_2[:, -3]
        # f_add.shape
        training_sample_xy_3 = np.insert(training_sample_xy_2, -1, f_add, axis=1)
        # training_sample_xy_3
        df = pd.DataFrame(training_sample_xy_3)
        df.to_csv('TrainingSample_XY_3.csv')
        return training_sample_xy_3