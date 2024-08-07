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

from exception import CustomException
from logger import logging
from utils import save_object
from utils import evaluate_models

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

            model_report: dict = evaluate_models(
                X_train=X_train, y_train=y_train, X_test=X_test, y_test=y_test, models=models
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