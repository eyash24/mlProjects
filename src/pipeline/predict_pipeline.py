import sys
import os
import pandas as pd
import numpy as np

from exception import CustomException
from logger import logging
from utils import load_object

class PredictPipeline:
    def __init__(self):
        pass

class CustomData:
    def __init__(
        self,
        gender: str,
        race_ethnicity: str,
        parental_level_of_education: str,
        lunch: str,
        test_preparation_course: str,
        reading_score: int,
        writing_score: int
    )
        self.gender = gender
        self.race_ethnicity = race_ethnicity
        self.parental_level_of_education = parental_level_of_education
        self.lunch = lunch
        self.test_preparation_course = test_preparation_score
        self.reading_score = reading_score
        self.wriiting_score = writing_score
        
