'''
This file contains code that is used for transforming data attained from data_ingestion
Transformation, feature engineering, data cleaning

Imagine you're teaching someone how to fold clothes:
fit_transform: You teach them how to fold (learn rules) and fold your first pile (clean training data).
transform: They fold the next pile (test data) using the same technique — no relearning, just applying.
'''

import sys
import os
from dataclasses import dataclass
import numpy as np
import pandas as pd 

'''
Apply different preprocessing steps to different columns
Example use: Apply OneHotEncoder to categorical columns and StandardScaler to numerical columns — all in one pipeline.
'''
from sklearn.compose import ColumnTransformer 
# Handle missing values
from sklearn.impute import SimpleImputer 
# Chains together preprocessing steps (e.g., imputation → encoding → scaling) into a single pipeline that you can fit and transform easily
from sklearn.pipeline import Pipeline
'''
OneHotEncoder: Converts categorical variables into binary columns (0s and 1s).
StandardScaler: Scales numerical features so they have a mean of 0 and standard deviation of 1.
'''
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

# We use dataclass since we are create a class that only has variables defined and no functions
# Purpose of the class below is to provide input to the DataTransformation (similar to DataIngestion) and specify preprocessor object (pipeline) will be saved.
@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifacts',"preprocessor.pkl")

# Defining the actual preprocessing steps
class DataTransformation:
        def __init__(self):
            self.data_transformation_config=DataTransformationConfig()
        
        # This function is to creata pickle files, categorical to numerical
        def get_data_transformer_object(self):
            try:
                numerical_features = ["writing_score", "reading_score"]
                categorical_features = ["gender","race_ethnicity","parental_level_of_education","lunch","test_preparation_course"]
                
                # Pipeline for numerical features on training dataset
                numerical_pipeline=Pipeline(
                    steps=[
                        ("imputer",SimpleImputer(strategy="median")),
                        ("scaler",StandardScaler())
                    ]
                )
                logging.info("Scaling for numerical features are done")
                
                # Pipeline for categorical features on training dataset
                categorical_pipeline=Pipeline(
                    steps=[
                        ("imputer",SimpleImputer(strategy="most_frequent")),
                        ("one_hot_encoder",OneHotEncoder()),
                        ("scaler",StandardScaler(with_mean=False))
                    ]
                )
                logging.info("Encoding for categorical features are done")
                
                # Combined preprocessing step
                preprocessor=ColumnTransformer(
                    [
                        ("numerical_pipeline",numerical_pipeline,numerical_features),
                        ("categorical_pipeline",categorical_pipeline,categorical_features)
                    ]
                )
                
                return preprocessor
                 
            except Exception as e:
                raise CustomException(e,sys)
        
        def initiate_data_transformation(self,train_path,test_path):
            try:
                train_df = pd.read_csv(train_path)
                test_df = pd.read_csv(test_path)
                logging.info("Read train and test CSV as dataframe successfully")
                
                logging.info("Now obtaining preprocessing object")
                preprocessing_obj=self.get_data_transformer_object()
                
                
                target_col = "math_score"
                numerical_col = ["writing_score", "reading_score"]
                
                # Split training data into input features (X) and target feature (y)
                input_feature_train_df = train_df.drop(columns=[target_col], axis=1)  # Drop the target column to get input features
                target_feature_train_df = train_df[target_col]                        # Extract only the target column

                # Split test data into input features (X) and target feature (y)
                input_feature_test_df = test_df.drop(columns=[target_col], axis=1)   # Drop the target column to get input features
                target_feature_test_df = test_df[target_col]                         # Extract only the target column

                # Log that preprocessing is being applied
                logging.info("Applied preprocessing object on training and testing dataframe")

                # Fit the preprocessing pipeline ONLY ON INPUT FEATURES and transform them
                # This step learns scaling, encoding, and imputing based on training data
                input_feature_train_arr = preprocessing_obj.fit_transform(input_feature_train_df)
                input_feature_test_arr = preprocessing_obj.transform(input_feature_test_df) # Transform test input features using the same preprocessing rules learned from training

                # Combine the processed input features and target column back into single arrays for train and test sets
                # Final format: [feature1, feature2, ..., featureN, target]
                train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
                test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

                # Log that preprocessing is completed and ready to be saved or used
                logging.info("Saved preprocessing object")

                
                save_object(self.data_transformation_config.preprocessor_obj_file_path,preprocessing_obj)
                
                return(train_arr,test_arr,self.data_transformation_config.preprocessor_obj_file_path)
                
                
            except Exception as e:
                raise CustomException(e,sys)
