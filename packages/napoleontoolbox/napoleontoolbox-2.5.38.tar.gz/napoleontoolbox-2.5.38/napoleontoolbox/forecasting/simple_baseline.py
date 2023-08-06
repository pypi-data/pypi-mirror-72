from napoleontoolbox.forecasting import preprocessing_features
import numpy as np
import pandas as pd

class BaselineModel():

    def __init__(self, threshold, number_per_year=252):
        self.model = 'simple_model'
        self.threshold = threshold
        self.output_ways = []
        self.last_avg_return = pd.DataFrame()

    def fit(self, X_train, y_train, X_val, y_val):#, method = 'standard'):
        self.columns_to_drop = preprocessing_features.most_correlated_features(X_train, self.threshold)
        X_train = X_train.drop(self.columns_to_drop, axis=1)
        X_val = X_val.drop(self.columns_to_drop, axis=1)
        way_last_return = np.sign(y_train[-1])

        for daily_feat in X_train.columns:
            # print(daily_feat)
            # print(f'number of distinct {X[daily_feat].nunique()} values')
            self.last_avg_return = pd.DataFrame(pd.DataFrame(y_train).mean())
            correlation_matrix = np.corrcoef(X_train[daily_feat], y_train)
            if (way_last_return>0 and correlation_matrix[0][1]>0):
                self.output_ways.append(1)

            elif (way_last_return < 0 and correlation_matrix[0][1] < 0):
                self.output_ways.append(0)
            else:
                self.output_ways.append(0.5)

    def predict(self, X_test):
        X_test = X_test.drop(self.columns_to_drop, axis=1)
        self.last_avg_return = self.last_avg_return.append([self.last_avg_return] * (len(X_test) - 1), ignore_index=True)
        next_way = np.max(self.output_ways)
        if next_way>0:
            y_pred = self.last_avg_return
        elif next_way<0:
            y_pred = 0*self.last_avg_return
        else:
            y_pred=0.5*self.last_avg_return
        return y_pred.values

    def get_features_importance(self, features_names):
        run_importances = {}
        # for (name, imp) in zip(features_names, self.model.coef_):
        #     run_importances[name] = imp
        return run_importances