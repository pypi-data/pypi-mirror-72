import numpy as np
import scipy
import pandas as pd
from scipy.stats import linregress

from napoleontoolbox.signal import signal_utility

from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from functools import partial
from numpy.lib.stride_tricks import as_strided as stride
import pandas as pd
from scipy.optimize import Bounds, LinearConstraint, minimize
from napoleontoolbox.utility import metrics
import numpy as np
from napoleontoolbox.signal import signal_utility
from napoleontoolbox.connector import napoleon_connector
import json

from napoleontoolbox.parallel_run import signal_result_analyzer
from sklearn.metrics import accuracy_score
from functools import partial


class SimpleThresholdModel():

    def __init__(self, nb_selected=10, number_per_year=365):
        self.model = None
        self.seed = 0
        self.nb_selected = nb_selected
        self.number_per_year = number_per_year

    def calibrate(self, X, y):
        return

    def fit(self, X_train, y_train, X_val, y_val):
        print(f'finding the {self.nb_selected} most correlated features with the output')
        output_correlations = []
        X = X_train.copy().fillna(0.)
        y = y_train.copy().fillna(0.)
        for daily_feat in X_train.columns:
            #print(daily_feat)
            #print(f'number of distinct {X[daily_feat].nunique()} values')
            correlation_matrix = np.corrcoef(X[daily_feat], y)
            output_correlations.append(
                {
                    'feature': daily_feat,
                    'correlation': correlation_matrix[0][1]
                }
            )
        output_correlations_df = pd.DataFrame(output_correlations)
        output_correlations_df['abs_correlation'] = abs(output_correlations_df['correlation'])
        output_correlations_df = output_correlations_df.sort_values(by='abs_correlation', ascending=False)
        output_correlations_df['effect_sign']=np.sign(output_correlations_df['correlation'])
        output_correlations_df.index = output_correlations_df.feature
        selected_output_correlations_df = output_correlations_df.head(self.nb_selected)
        self.selected_features = list(selected_output_correlations_df.feature)
        correlation_effects = selected_output_correlations_df['effect_sign'].to_dict()
        selected_X = X[self.selected_features].copy()
        scaler = StandardScaler()
        scaler.fit(selected_X)
        transformed_selected_X = scaler.transform(selected_X)
        transformed_selected_X_df = pd.DataFrame(data = transformed_selected_X, columns = selected_X.columns, index = selected_X.index)
        #print(transformed_selected_X.shape)
        threshold_dic = {}
        for feature_to_investigate in self.selected_features:
            #print(feature_to_investigate)
            signal_way = correlation_effects[feature_to_investigate]
            x = transformed_selected_X_df[feature_to_investigate].values.copy()
            np.random.seed(self.seed)
            def find_best_threshold(number_per_year, way,y,x,w):
                if np.sign(way)>0:
                    y_pred_discrete = x > w[0]
                else:
                    y_pred_discrete = x < w[0]
                perf_df = signal_utility.reconstitute_prediction_perf(y_pred=y_pred_discrete, y_true=y,
                                                                      transaction_cost=False,
                                                                      print_turnover=False)
                sharpe_strat = metrics.sharpe(perf_df['perf_return'].dropna(), period=number_per_year, from_ret=True)
                return -1*sharpe_strat
            f_to_optimize = partial(find_best_threshold, self.number_per_year, signal_way, y, x)
            N_ = 1
            w0 = np.array([0.5])
            # Set constraints
            # const_sum = LinearConstraint(np.ones([1, N_]), [1], [1])
            up_bound_ = 1.
            low_bound_ = 0.
            const_ind = Bounds(low_bound_ * np.ones([N_]), up_bound_ * np.ones([N_]))
            splitting_quantile_threshold = 0.5
            trouble = False
            try:
                # Optimize f
                conv_results = minimize(
                    f_to_optimize,
                    w0,
                    method='SLSQP',
                    # constraints=[const_sum],
                    bounds=const_ind
                )
                w__=conv_results.x
                print(f'sharpe conv reults {conv_results.fun}')
                splitting_quantile_threshold = w__[0]
            except Exception as e:
                trouble = True
                ## we should print
                print(e)
            if np.isnan(splitting_quantile_threshold):
                splitting_quantile_threshold = 0.5
            threshold_dic[feature_to_investigate] = splitting_quantile_threshold
            #print('done')
        self.threshold_dic = threshold_dic
        self.correlation_effects = correlation_effects
        self.scaler = scaler
        return

    def predict(self, X_test):
        X = X_test.copy()
        selected_X = X[self.selected_features].copy()
        transformed_selected_X = self.scaler.transform(selected_X)
        transformed_selected_X_df = pd.DataFrame(data = transformed_selected_X, columns = selected_X.columns, index = selected_X.index)
        for feature_to_investigate in self.selected_features:
            #print(feature_to_investigate)
            signal_way = self.correlation_effects[feature_to_investigate]
            x = transformed_selected_X_df[feature_to_investigate].values.copy()
            if np.sign(signal_way) > 0:
                y_pred_discrete = x > self.threshold_dic[feature_to_investigate]
            else:
                y_pred_discrete = x < self.threshold_dic[feature_to_investigate]
            transformed_selected_X_df[feature_to_investigate] = y_pred_discrete
        return transformed_selected_X_df.mean(axis=1)

    def get_features_importance(self, features_names):
        return
