import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import classification_report
from scipy.stats import iqr
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix,accuracy_score
import logging
import pickle

logging.basicConfig(filename='modelLogs.log',level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

data=pd.DataFrame()
try:
    data=pd.read_csv('cardio_train.csv',sep=';')
    logging.info('File Read Successfully')
except FileNotFoundError:
    logging.error('File Not Found')

#Converting age from days to years
data['age_years']=data['age']/365
data.drop(['id','age'], axis=1, inplace=True)

healthy = data[(data['cardio'] ==0) ].count()[1]
sick = data[(data['cardio'] ==1) ].count()[1]
print ("num of pepole without heart deacise: "+ str(healthy))
print ("num of pepole with chance for heart deacise: "+ str(sick))

#OutLier Analysis
logging.info('Outlier Analysis Starting')
for col in ['height', 'weight', 'ap_hi', 'ap_lo']:
    InterQuartileRange=iqr(data[col])
    print('InterQuartileRange for',col,' =',InterQuartileRange)
    InterQuartileRangeLower=np.quantile(data[col], .25)
    print('InterQuartileRangeLower for',col,' =',InterQuartileRangeLower)
    InterQuartileRangeHigher=np.quantile(data[col], .75)
    print('InterQuartileRangeHigher for ',col,' =',InterQuartileRangeHigher)
    print('Max of ',col,' =',data[col].max())
    print('Min of ',col,' =',data[col].min())
    print('Lower Limit for ',col,' =',InterQuartileRangeLower-(1.5*InterQuartileRange))
    print('Upper Limit ',col,' =',InterQuartileRangeHigher+(1.5*InterQuartileRange))
    InRange=0
    OutRange=0
    for i in data[col]:
        if((InterQuartileRangeLower-(1.5*InterQuartileRange))<=i<=(InterQuartileRangeHigher+(1.5*InterQuartileRange))):
            InRange=InRange+1
        else:
            OutRange=OutRange+1
    print('InRange for ',col,' =',InRange)
    print('OutRange for ',col,' =',OutRange)
    logging.info('Outlier Analysis Complete for {} column'.format(col))

#Removing ourliers from the dataset
logging.info('Cleaning data based on Outlier Analysis')
data_Clean=data.loc[
    (data['height']>142.5) & (data['height']<186.5) &
    (data['weight']>39.5) & (data['weight']<107.5) &
    (data['ap_hi']>90.0) & (data['ap_hi']<170.0) &
    (data['ap_lo']>65.0) & (data['ap_lo']<105.0)
]
logging.info('Cleaning data completed based on Outlier Analysis')

data_Clean = data_Clean[['gender', 'age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc',
                         'smoke', 'alco', 'active', 'cardio']]

X=data_Clean.loc[:, data_Clean.columns != 'cardio']
Y=data_Clean['cardio']

#Train Test Split
logging.info('Splitting data into Train and Test')
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)
print('X_train shape =',X_train.shape)
print('X_test shape =',X_test.shape)
print('Y_train shape =',Y_train.shape)
print('Y_test shape =',Y_test.shape)

logging.info('Starting Gradient Boost Classifier')
GradientBoostingClassifier=GradientBoostingClassifier()
param_grid_gbc = {'n_estimators': [300,500,600,800,1000],
                  'learning_rate': [0.01,0.02,0.03],
                  'max_features':[2,3,4,5,6]
                 }

try:
    grid_search_GBC = GridSearchCV(estimator = GradientBoostingClassifier,param_grid=param_grid_gbc,cv=3)
    logging.info('Model Initiated successfully')
    GBC_GS = grid_search_GBC.fit(X_train, Y_train)
    logging.info('Model Fitted Successfully')
    print('Best Estimator for GradientBoostingClassifier is',grid_search_GBC.best_estimator_)
    Y_pred1 = GBC_GS.predict(X_test)
    logging.info('Model Predicted Successfully')
    print('Confusion Matrix for GradientBoostingClassifier is :',confusion_matrix(Y_test, Y_pred1))
    print('Accuracy for GradientBoostingClassifier is:- ',accuracy_score(Y_test, Y_pred1))
    # Saving model to disk
    pickle.dump(grid_search_GBC, open('model.pkl','wb'))
    logging.info('Model dumped to .pkl file')
except:
    logging.error('Model did not run as expected')

try:
    # Loading model to compare the results
    model = pickle.load(open('model.pkl','rb'))
    logging.info('.pkl loaded Successfully')
    #'gender', 'age_years', 'height', 'weight', 'ap_hi', 'ap_lo', 'cholesterol', 'gluc','smoke', 'alco', 'active'
    #print(model.n_features)
    print('Test Result:-')
    print(model.predict([[1,25,178,76,120,80,1,1,0,0,1]]))
    logging.info('.pkl file predicted successfully')
except:
    logging.error('.pkl file not found')
