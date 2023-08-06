import numpy as np
import pandas as pd

def most_correlated_features(X,threshold):
    generic_features = ['close','high', 'low', 'open', 'volume']
    columns_to_compute = [col for col in X.columns if col not in generic_features]
    output_correlations = []
    for i in range(len(columns_to_compute)):
        for j in range(i+1,len(columns_to_compute)):
            left_feature = columns_to_compute[i]
            right_feature=columns_to_compute[j]
            if left_feature != right_feature:
                # print(left_feature, right_feature)
                # print(X[left_feature].nunique())
                # print('done')
                correlation_matrix = np.corrcoef(X[left_feature],X[right_feature])
                output_correlations.append(
                    {
                        'daily_feature_1':left_feature,
                        'daily_feature_2':right_feature,
                        'correlation':correlation_matrix[0][1]
                    }
                )

    output_correlations_df = pd.DataFrame(output_correlations)
    output_correlations_df['abs_correlation'] = abs(output_correlations_df['correlation'] )
    output_correlations_df = output_correlations_df.sort_values(by='abs_correlation', ascending=False)
    columns_to_drop = output_correlations_df.loc[output_correlations_df['abs_correlation'] > threshold]['daily_feature_2'].unique()
    return columns_to_drop


def get_binarization_threshold(X):
        return X.mean().to_dict()

def binarize_features(X,features_threshold):
    X[list(features_threshold.keys())] = (X[features_threshold.keys()] >= list(features_threshold.values())).astype(int)
    return X