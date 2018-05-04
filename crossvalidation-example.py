import csv as csv
import numpy as np
import pandas as pd

from sklearn.model_selection import cross_val_score, cross_val_predict

scores = cross_val_score(model, data, CV, cv=number_of_folds)

dataset = pd.read_csv('train.csv') #loads csv file


# MSE when all of training data used for testing
print("Mean residual sum of squares when all the data is used for training: %0.2f" % np.mean((regr.predict(data) - CV) ** 2))

#MSE when 80% of the data is used to obtain a model (training), tested on the rest 20%
i=0
for i in range (0,5):
      X_train, X_test, y_train, y_test = train_test_split(data, CV, test_size=.2)
      regr.fit(X_train, y_train)
      print("MSE with 80-20 split iteration %s : %0.2f" % (i , mean_squared_error(y_test,regr.predict(X_test))))
      i=i+1

model = linear_model.LinearRegression()
# Calculating cross-validated scores for the model
kf = KFold(len(CV), n_folds=5, shuffle=True, random_state=0)
scores = cross_val_score(model, data, CV, scoring = 'mean_squared_error', cv=kf)
print("MSE of every fold with K=5: ", abs(scores))
print("Mean of 5-fold cross-validated MSE: %0.2f (+/- %0.2f)" % (abs(scores.mean()), scores.std() * 2))

# Calculating leave one out cross validation scores for the model
# can use the built in function LeaveOneOut()
kf = KFold(len(CV), n_folds=10)
scores = cross_val_score(model, data, CV, scoring = 'mean_squared_error', cv=kf)
print("MSE of every fold in leave one out cross validation: ", abs(scores))
print("Mean of 10-fold cross-validated MSE: %0.2f (+/- %0.2f)" % (abs(scores.mean()), scores.std() * 2))

# Estimating output: what was CV when data row was in training dataset
estimated_results = cross_val_predict(regr, data, CV, cv=5)
print(estimated_results)
