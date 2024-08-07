import os
import sys
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor, GradientBoostingRegressor, RandomForestRegressor
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object
from src.utils import evaluate_models

@dataclass 
class ModelTrainerConfig:
    trained_model_file_path = os.path.join("artifacts", 'model.pkl')
     
class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()
    
    def initiate_model_trainer(self,train_array, test_array):
        try:
            logging.info("Splitting train and test data")
            X_train, y_train, X_test,y_test = (
            train_array[:, :-1], train_array[:,-1],
            test_array[:,:-1], test_array[:, -1]
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                'Decision Tree': DecisionTreeRegressor(),
                'Gradient Boosting': GradientBoostingRegressor(),
                'Linear Regression': LogisticRegression(),
                'K-Neighbor Regression': KNeighborsRegressor(),
                'XGB Regression': XGBRegressor(),
                'CatBoosting Regression': CatBoostRegressor(verbose=False),
                'Adaboost Regression': AdaBoostRegressor()
            }

            params = {
                'Decision Tree': {
                    'criterion': ['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter': ['best', 'random'],
                    # 'max_features': ['sqrt', 'log2'],
                },
                'Random Forest': {
                    'n_estimators': [8,16,32,64,128,256]
                },
                'Gradient Boosting':{
                    'learning_rate': [.1, .01, .05, .001],
                    'subsample': [.6, .7, .75, .8, .85, .9],
                    'n_estimators': [8,16,32,64,128,256]
                ,
                },
                'Linear Regression': {},
                'K-Neighbor Regression': {
                    'n_neighbors':[5,7,9,11,13]
                },
                'XGB Regression': {
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                'CatBoosting Regression': {
                    'learning_rate': [.1, .01, .05, .001],
                    'depth': [6,8,10],
                    # 'iteration': [30,50,100]
                },
                'Adaboost Regression':{
                    'learning_rate': [.1, .01, .05, .001],
                    'n_estimators': [8,16,32,64,128,256]
                }

            }

            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, 
                models=models, params=params
            )

            best_model_score = max(sorted(model_report.values()))
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            best_model = models[best_model_name]
            
            if best_model_score < 0.6:
                raise CustomException('No best model found', sys)
            
            logging.info('Best model found on both training and testing dataset')

            save_object(
                file_path = self.model_trainer_config.trained_model_file_path,
                obj=best_model
            )

            predicted = best_model.predict(X_test)
            r2_result = r2_score(y_test, predicted)
            return r2_result

        except Exception as e:
            raise CustomException(e, sys)