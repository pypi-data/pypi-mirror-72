import pandas as pd
import numpy as np
import cvxopt
from joblib import load

from sklearn.base import BaseEstimator

class TrustiiAggregateModel(BaseEstimator):
    def __init__(self,
                 models=[],
                 alphaStar=1,
                 type = 'TRUSTII-AGGREGATE-MODEL-v0.2',
                 mlType='classification',
                 ):
        self.models = models
        self.alphaStar = alphaStar
        self.mlType = mlType
        self.type =type
    def __repr__(self):
        return self.type

    def get_models_prediction(self,X):
        preds=[]
        if self.mlType=='classification':
            for model in self.models:
                #model = load(modelId)
                preds+=[model.predict_proba(X)[:,1]]
        else:
            for model in self.models:
                #model = load(modelId)
                preds+=[model.predict(X)]
        return np.array(preds).transpose()


    def predict_proba(self, X):
        if self.mlType != 'classification':
            raise ValueError(
                "predic_proba method is allowed only with classification problems, but the current problem is : {}".format(self.mlType)
            )
        M = self.get_models_prediction(X)
        y_pred = np.ndarray(shape=(len(X),2), dtype=float)
        for feature in range(len(X)):
            s=0
            for model in range(len(self.models)):
                s += self.alphaStar[model]*M[feature,model]
            y_pred[feature,:] = np.array([1.- s[0], s[0] ])
        return y_pred


    def __find_optimal_cuttof(self,fpr,tpr,thresholds):
      '''this is based on the Youden Index '''
      optimal_idx = np.argmax(tpr - fpr)
      return thresholds[optimal_idx]#,optimal_idx


    def predict(self,X,y_test=None,threshold=None):
      from sklearn.metrics import roc_curve
      '''
      if threshold is not None, the user is providing a value, otherwise we
       optimize it for classification problems
       if y_test and threshold are  not given, the default threshold is .5
      '''

      if self.mlType=='classification':
        y_score = self.predict_proba(X)[:,1]
        if threshold is None :
          if y_test is None:return np.where(y_score>=.5, 1, 0)
          fpr,tpr,thresholds=roc_curve(y_test,y_score)
          threshold = self.__find_optimal_cuttof(fpr,tpr,thresholds)
        return np.where(y_score>=threshold, 1, 0)
          #print("Using optimized threshold ... : "+ str(threshold))
        
      else :
        M = self.get_models_prediction(X)
        y = []
        for feature in range(len(X)):
          s=0
          for model in range(len(self.models)):
            s += self.alphaStar[model]*M[feature,model]
          y+= [s[0]]
        return y