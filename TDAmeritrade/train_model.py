"""
Train Gradient Boosting model for stock prediction
"""
import os
import sys
sys.path.append('../')
from config.tda.config import JSON_PATH, CONSUMER_KEY, REDIRECT_URI, WEBDRIVER, tda_login

import pandas as pd
pd.options.mode.chained_assignment = None
from preprocessing import time_processing, preprocessing

from sklearn.pipeline import make_pipeline
from sklearn.ensemble import GradientBoostingRegressor, GradientBoostingClassifier
from sklearn.feature_selection import f_regression, SelectKBest
from sklearn.model_selection import TimeSeriesSplit, GridSearchCV
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score
import pickle
from datetime import datetime

stock_ticker = 'VOO'
now = datetime.now().strftime("%m%d%Y%H%M")
c = tda_login(JSON_PATH, CONSUMER_KEY, REDIRECT_URI, WEBDRIVER)
data = pd.DataFrame(c.get_price_history_every_minute(stock_ticker).json()['candles'])
data['target'] = data['close'].shift(-1)
data, best_d_value, weights = preprocessing(data, price_offset = 1.000001)


"""
test/train/ver split
"""
train_size = round(.9*len(data))

train = data[:train_size]
test = data[train_size:]

y_train = train.pop('target_classifier')
X_train = train
# X_train.drop('datetime', axis=1, inplace=True)

y_test = test.pop('target_classifier')
X_test = test


"""
ML Pipeline
with Verification
"""
pipe = make_pipeline(SelectKBest(score_func=f_regression, k=10), GradientBoostingClassifier())
tscv = TimeSeriesSplit(n_splits=10)
parameters = {
    'gradientboostingclassifier__max_depth': range (2, 10, 1),
    'gradientboostingclassifier__n_estimators': range(60, 220, 40),
    'gradientboostingclassifier__learning_rate': [0.1, 0.01, 0.05]
}
clf = GridSearchCV(pipe, parameters, n_jobs=-1, cv=tscv, scoring = 'precision')
# clf = GridSearchCV(pipe, parameters, n_jobs=-1, cv=tscv, scoring = 'roc_auc')
clf.fit(X_train,y_train)
print(f"Current best parameters: {clf.best_params_}")

y_pred = clf.predict(X_train)
print(f"Training set scores:\n  Precision - {precision_score(y_train, y_pred)}\n  Accuracy - {accuracy_score(y_train, y_pred)}")

y_pred = clf.predict(X_test)
print(f"Training set scores:\n  Precision - {precision_score(y_test, y_pred)}\n  Accuracy - {accuracy_score(y_test, y_pred)}")

# save

os.rename('model/model.pkl', f'model/dep/model{now}.pkl')
with open('model/model.pkl','wb') as f:
    pickle.dump(clf,f)