#csv로 만들어 
from selectors import SelectSelector
from tabnanny import verbose
from sklearn.datasets import load_breast_cancer, load_wine,fetch_covtype
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler,MinMaxScaler
from xgboost import XGBClassifier,XGBRegressor
import time 
from sklearn.metrics import accuracy_score,r2_score,f1_score
import warnings
warnings.filterwarnings(action="ignore")
from sklearn.feature_selection import SelectFromModel
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import LabelEncoder
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from imblearn.over_sampling import SMOTE 

path = 'D:/study_data/_data/'
datasets = pd.read_csv(path + 'winequality-white.csv', index_col=None, header=0, sep=';') # sep';'< csv 

print(datasets.shape)   #(4898, 12)
print(datasets.describe())   #(4898, 12)
print(datasets.info())

datasets2 = datasets.to_numpy()    #pandas 를 numpy로 바꿀때 

print(type(datasets2))
print(datasets.shape)

x = datasets2[:, :11]
y = datasets2[:, 11]
print(x.shape, y.shape)  # (4898, 11) (4898,)

print(np.unique(y, return_counts = True)) #다중분류에서는 데이터 무조건 확인하기
# (array([3., 4., 5., 6., 7., 8., 9.]), array([  20,  163, 1457, 2198,  880,  175,    5], dtype=int64))
print(datasets['quality'].value_counts())


x_train, x_test, y_train, y_test = train_test_split(
    x, y, train_size=0.8, shuffle=True, random_state=123, stratify= y
) 

smote = SMOTE(random_state=123, k_neighbors = 3)                             #SMOTE 증폭 
x_train, y_train = smote.fit_resample(x_train, y_train)


#2, 모델
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier()

print(pd.Series(y_train).value_counts())


#3.훈련
model.fit(x_train,y_train)

#4. 평가,예측
y_predict  = model.predict(x_test)

score = model.score(x_test,y_test)  
print("model.score:", score)
print('acc_score:',accuracy_score (y_test,y_predict))
print('f1_score(macro): ',f1_score(y_test,y_predict , average="macro")) #F1_score 은 2진분류에서 많이 사용 다중분류에서 average="macro" 사용
print('f1_score(micro): ',f1_score(y_test,y_predict , average="micro")) #F1_score 은 2진분류에서 많이 사용 
########과제 프리시즌 리콜 precisi


###########증폭후#############
# model.score: 0.6989795918367347
# acc_score: 0.6989795918367347
# f1_score(macro):  0.43996926092651084
# f1_score(micro):  0.6989795918367347