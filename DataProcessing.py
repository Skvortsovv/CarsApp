import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle


class DataProcessing:
    def __init__(self):
        self.df = None

    def process(self, file_path):
        self.df = pd.read_csv(file_path, index_col=0).drop(['model', 'vin', 'lot'], axis=1)

        self.df = self.df[self.df['country'] != ' canada']
        self.df = self.df.drop(['country'], axis=1)

        no_pop_brands = self.df.brand.value_counts()[self.df.brand.value_counts() < 5].index
        self.df.loc[self.df['brand'].isin(no_pop_brands), 'brand'] = 'other_brand'

        no_pop_states = self.df.state.value_counts()[self.df.state.value_counts() < 7].index
        self.df.loc[self.df['state'].isin(no_pop_states), 'state'] = 'other_state'

        no_pop_color = self.df.color.value_counts()[
            (self.df.color.value_counts() < 5) | (self.df.color.value_counts().index == 'color:')].index
        self.df.loc[self.df['color'].isin(no_pop_color), 'color'] = 'other_color'

        self.df.condition = self.df.condition.str.extract('(\d+)')
        self.df.condition = self.df.condition.fillna(-9999)
        self.df.condition = self.df.condition.astype('int')

        for col in ['brand', 'state', 'title_status', 'color']:
            self.one_hot_encoding(col)

    def one_hot_encoding(self, col):
        dumm = pd.get_dummies(self.df[col])
        self.df = self.df.drop([col], axis=1)
        self.df = self.df.join(dumm)


    def model(self):
        X = self.df.drop(['price'], axis=1)
        y = self.df.price
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)

        model = RandomForestRegressor(n_jobs=-1)
        model.fit(X_train, y_train)

        pickle.dump(model, open('model.sav', 'wb'))


dataProcessing = DataProcessing()
dataProcessing.process(r'C:\Users\Gleb\Desktop\USA_cars_datasets.csv')
dataProcessing.model()
