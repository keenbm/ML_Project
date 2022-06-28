from collections import namedtuple


# Configuration for DataIngestion
# 1. dataset_download_url --> File location from server/website 
# 2. tgz_download_dir -->Compressepythond File
# 3. raw_data_dir --> Extracted FileHandle
# 4. ingested_train_dir --> Train Dataset Folder
# 5. ingested_test_dir --> Testing Dataset folder 

DataIngestionConfig=namedtuple("DataIngestionConfig",["dataset_download_url",
                                                     "tgz_download_dir",
                                                     "raw_data_dir",
                                                     "ingested_train_dir",
                                                     "ingested_test_dir"])

# Configuration for DataValidation
# 6. schema_file_path --> Schema File
DataVaildationConfig=namedtuple("DataVaildationconfig",["schema_file_path"])


# Configuration for DataTransformation
# 7. add_bedroom_per_room --> Adding this column in dataset
# 8. transformed_train_dir --> Train Data after Transformation
# 9. transformed_test_dir -->  Test Data after Transformation
# 10. preprocessed_object_file_path --> Data Transformation PICKEL file location
DataTransformationConfig=namedtuple("DataTransformationconfig",["add_bedroom_per_room",
                                                                "transformed_train_dir",
                                                                "transformed_test_dir",
                                                                "preprocessed_object_file_path"])

# Configuration for ModelTraining
# 11. trained_model_file_path --> Path for Trained model Pickel file
# 12. base_accuracy
ModelTrainerConfig = namedtuple("ModelTrainerConfig",["trained_model_file_path",
                                                            "base_accuracy"])

#Configuration for ModelEvaluation
# 13.model_evaluation_file_path
# 14. time_stamp
ModelEvaluationConfig = namedtuple("ModelEvaluationConfig",["model_evaluation_file_path",
                                                            "time_stamp"])