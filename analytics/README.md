TASK -- Part A -- Point 3: Univariate Analysis

The fare distribution is right-skewed because the mean is greater than the median, and the median is greater than the mode (Mean > Median > Mode). This indicates that a relatively small number of passengers paid very high fares, creating a long right tail. The IQR rule was used to identify the outliers in both age and fare.




![Survival Rate of SEX Histogram](analytics/plots/sr_by_sex.png)
The bar plot shows that female passengers had a higher survival rate than male passengers. This indicates a strong association between sex and survival in the Titanic dataset

![Survival Rate of CLASS Histogram](analytics/plots/sr_by_class.png)
The survival rate differs across passenger classes. First-class passengers had a higher observed survival rate than second- and third-class passengers.

![Survival Rate of CLASS and SEX Histogram](analytics/plots/sr_by_sex_and_class.png)
The combination of sex and passenger class provides a clearer picture of survival. Female passengers generally had higher survival rates within each class, while survival also varied across passenger classes.

![Survival Rate of AGE Group Histogram](analytics/plots/sr_by_age_grp.png)
Survival rates also varied across age groups. The plot shows how survival differed between children, teenagers, adults, middle-aged passengers, and seniors, providing another dimension to the survival story.


![Residual Plot of Linear regression](analytics/plots/residual_plot_for_linear_model.png)
Residual Plot Interpretation: The residual plot shows a clear non-random pattern in the residuals. The residuals form distinct patterns and their spread is not constant across the predicted fare values. Therefore, the plot provides visual evidence of heteroscedasticity, meaning that the variance of the regression errors is not constant.




Final model decision:
For the classification task, Random Forest is suitable for this dataset because it has the highest accuracy (0.820) and F1 score (0.758). It also has the highest recall (0.735) with good precision (0.781). However, Logistic Regression has a higher AUC score (0.861) compared with Random Forest (0.821), showing better class separation. Overall, I would choose Random Forest because it gives better accuracy, recall, and F1 score.
