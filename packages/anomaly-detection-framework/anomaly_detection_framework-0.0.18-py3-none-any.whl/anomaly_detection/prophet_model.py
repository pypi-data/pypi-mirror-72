from pandas import DataFrame, Series
from fbprophet import Prophet
import random
import numpy as np
from itertools import product
import pandas as pd

from functions import *
from utils import *
from logger import LoggerProcess


def get_anomaly(fact, yhat_upper, yhat_lower):
    ad = Series([0, 0])
    if fact > yhat_upper:
        ad = Series([1, abs((fact - yhat_upper) / fact)])
    if fact < yhat_lower:
        ad = Series([1, abs((yhat_lower - fact)/ fact)])
    return ad


def get_anomaly_score(anomaly, fact, yhat_upper, yhat_lower):
    if anomaly == 1:
        return abs((fact - yhat_upper) / fact)
    if anomaly == -1:
        return abs((yhat_lower - fact)/ fact)


def get_tuning_params(parameter_tuning, params, job):
    arrays = []
    for p in params:
        if p not in list(parameter_tuning.keys()):
            arrays.append([params[p]])
        else:
            arrays.append(
                          np.arange(float(parameter_tuning[p].split("*")[0]),
                                    float(parameter_tuning[p].split("*")[1]),
                                    float(parameter_tuning[p].split("*")[0])).tolist()
            )
    comb_arrays = list(product(*arrays))
    if job != 'parameter_tuning':
        return random.sample(comb_arrays, int(len(comb_arrays)*0.5))
    else:
        return comb_arrays


def get_params(params, comb):
    count = 0
    for p in params:
        _p = type(params[p])(comb[count])
        params[p] = _p
        count += 1
    return params


def mean_absolute_percentage_error(y_true, y_pred):
    y_true, y_pred = np.array(y_true), np.array(y_pred)
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100


class TrainProphet:
    def __init__(self,
                 job=None, groups=None, time_indicator=None, feature=None,
                 data_source=None, data_query_path=None, time_period=None):
        self.job = job
        self.params = conf('parameter_3')
        self.query_date = get_query_date(job, period=time_period, dates=None, params=self.params)
        self.data, self.groups = data_manipulation(job=job,
                                                   date=self.query_date,
                                                   time_indicator=time_indicator,
                                                   feature=feature,
                                                   data_source=data_source,
                                                   groups=groups,
                                                   data_query_path=data_query_path)
        self.date = time_indicator
        self.f_w_data = self.data
        self.optimized_parameters = self.params
        self.hyper_params = conf('parameter_tuning')['prophet']
        self.split_date = get_split_date(period=time_period, dates=list(self.data[self.date]), params=self.params)
        self.feature = feature
        self.anomaly = []
        self.model = None
        self.count = 1
        self.levels = get_levels(self.data, self.groups)
        self.levels_tuning = get_tuning_params(self.hyper_params, self.params, self.job)
        self.logger = LoggerProcess(job=job,
                                    model='prophet',
                                    total_process=len(self.levels)
                                    if job != 'parameter_tuning' else len(self.levels_tuning))
        self.comb = None
        self.prediction = None

    def get_query(self):
        count = 0
        query = ''
        for c in self.comb:
            if type(c) != str:
                query += self.groups[count] + ' == ' + str(c) + ' and '
            else:
                query += self.groups[count] + " == '" + str(c) + "' and "
            count += 1
        query = query[:-4]
        return query

    def convert_date_feature_column_for_prophet(self):
        renaming = {self.date: 'ds', self.feature: 'y'}
        self.f_w_data = self.f_w_data.rename(columns=renaming)
        self.f_w_data['ds'] = self.f_w_data['ds'].dt.tz_convert(None)
        return self.f_w_data

    def fit_predict_model(self, save_model=True):
        self.f_w_data = self.convert_date_feature_column_for_prophet()
        self.model = Prophet(daily_seasonality=False, yearly_seasonality=False, weekly_seasonality=False,
                             seasonality_mode='multiplicative',
                             interval_width=float(self.params['interval_width']),
                             changepoint_range=float(self.params['changepoint_range']),
                             n_changepoints=int(self.params['n_changepoints'])
                             ).fit(self.f_w_data[['ds', 'y']])
        if save_model:
            model_from_to_pkl(directory=conf('model_main_path'),
                              path=model_path(self.comb, self.groups, 'prophet'),
                              model=self.model, is_writing=True)

    def detect_anomalies(self):
        self.model = model_from_to_pkl(directory=conf('model_main_path'),
                                       path=model_path(self.comb, self.groups, 'prophet'))
        try:
            self.prediction = self.model.predict(self.convert_date_feature_column_for_prophet())
            self.f_w_data = pd.merge(self.f_w_data,
                                     self.prediction.rename(columns={'ds': self.date}),
                                     on=self.date,
                                     how='left')
            self.f_w_data = self.f_w_data[self.f_w_data[self.date] >= self.split_date]
            self.f_w_data[['ad_label_3', 'anomaly_score_3']] = self.f_w_data.apply(lambda row:
                                                                                   get_anomaly(row[self.feature],
                                                                                            row['yhat_upper'],
                                                                                            row['yhat_lower']), axis=1)
            self.anomaly += self.f_w_data[['ad_label_3', self.date, 'anomaly_score_3'] + self.groups].to_dict("results")
            print(self.f_w_data[['ad_label_3', self.date, 'anomaly_score_3'] + self.groups])
        except Exception as e:
            print(e)

    def train_execute(self):
        if not conf('has_param_tuning_first_run')['prophet']:
            self.parameter_tuning()
        for self.comb in self.levels:
            print("*" * 4, "PROPHET - ", self.get_query().replace(" and ", "; ").replace(" == ", " - "), "*" * 4)
            self.f_w_data = self.data.query(self.get_query()).sort_values(by=self.date)
            print("data size :", len(self.f_w_data))
            self.convert_date_feature_column_for_prophet()
            self.fit_predict_model()
            self.logger.counter()
            if not check_request_stoped(self.job):
                break

    def prediction_execute(self):
        for self.comb in self.levels:
            print("*" * 4, "PROPHET - ", self.get_query().replace(" and ", "; ").replace(" == ", " - "), "*" * 4)
            if check_model_exists(model_path(self.comb, self.groups, 'prophet'), conf('model_main_path')):
                self.f_w_data = self.data.query(self.get_query()).sort_values(by=self.date)
                print("prediction size :", len(self.f_w_data))
                self.detect_anomalies()
            self.logger.counter()
            if not check_request_stoped(self.job):
                break
        self.anomaly = DataFrame(self.anomaly)

    def parameter_tuning(self):
        error = 1000000
        self.f_w_data = self.data.pivot_table(index=self.date,
                                              aggfunc={self.feature: 'mean'}
                                              ).reset_index().sort_values(by=self.date, ascending=True)
        for pr in self.levels_tuning:
            self.params = get_params(self.params, pr)
            print("hyper parameters : ", self.params)
            self.convert_date_feature_column_for_prophet()
            self.fit_predict_model(save_model=False)
            self.prediction = self.model.predict(self.convert_date_feature_column_for_prophet())
            if mean_absolute_percentage_error(self.f_w_data['y'], abs(self.prediction['yhat'])) < error:
                error = mean_absolute_percentage_error(self.f_w_data['y'], abs(self.prediction['yhat']))
                self.optimized_parameters = self.params
            self.logger.counter()
            if not check_request_stoped(self.job):
                break
        print("updating model parameters")
        config = read_yaml(conf('docs_main_path'), 'configs.yaml')
        config['hyper_parameters']['prophet'] = self.optimized_parameters
        config['has_param_tuning_first_run']['prophet'] = True
        write_yaml(conf('docs_main_path'), "configs.yaml", config)
        self.params = conf('parameter_3')







