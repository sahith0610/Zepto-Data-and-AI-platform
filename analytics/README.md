# Titanic Analytics and Machine Learning

This project performs data analysis and machine learning on the Titanic dataset.

## Tasks

- Load and inspect the Titanic dataset.
- Perform data quality checks.
- Handle missing values.
- Perform exploratory data analysis (EDA).
- Analyze distributions, correlations, and outliers.
- Build classification models to predict passenger survival.
- Build a regression model to predict passenger fare.
- Compare model performance using evaluation metrics.
- Save the best-performing classification pipeline using Joblib.

## Data Preprocessing

Missing values were handled using appropriate techniques. Missing `age` values were replaced using the median, rows with missing `embarked` and `embark_town` were removed, and the `deck` column was removed because it contained a large number of missing values.

Numerical and categorical features were processed using a preprocessing pipeline. Numerical features were scaled and categorical features were one-hot encoded.

## Exploratory Data Analysis

The dataset was analyzed using statistical summaries and visualizations.

The fare distribution is right-skewed because the mean is greater than the median, and the median is greater than the mode (Mean > Median > Mode). This indicates that a relatively small number of passengers paid very high fares, creating a long right tail.

The IQR rule was used to identify the outliers in both age and fare.

## Classification

Three classification models were evaluated:

- Logistic Regression
- Decision Tree
- Random Forest

The models were evaluated using:

- Accuracy
- Precision
- Recall
- F1 Score
- AUC

Random Forest achieved an accuracy of 0.820 and an F1 score of 0.758.

## Regression

Linear Regression was used to predict passenger fare.

The regression model was evaluated using:

- MAE
- RMSE
- R²
- Adjusted R²

Results:

- MAE: 0.302
- RMSE: 0.380
- R²: 0.388
- Adjusted R²: 0.352

The residual plot showed a non-random pattern and provided visual evidence of heteroscedasticity.

## Saved Pipeline

The final Random Forest pipeline, including preprocessing and the model, was saved using Joblib as:

`titanic_random_forest_pipeline.joblib`

The saved pipeline can be loaded later and used to make predictions without repeating the preprocessing steps.
