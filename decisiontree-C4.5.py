from __future__ import print_function
import pandas as pd
import numpy as np
import os
import subprocess
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import tree
from sklearn import preprocessing
from sklearn.model_selection import KFold, cross_val_score


os.environ["PATH"] += os.pathsep + 'C:/Program Files (x86)/Graphviz2.38/bin/'

#OPTION 1: for binary CV (up or down)
#df = pd.read_csv('decTree-Binary.csv')

#OPTION 2: for categorical CV (big up or up or down or big down)
df = pd.read_csv('decTree-Binary.csv')

#OPTION 3: all categorical
#df = pd.read_csv('decTree-AllCategorical.csv')


def encode_CV(df, CV_column):
    df_mod = df.copy()
    CV = df_mod[CV_column].unique()
    map_to_int = {name: n for n, name in enumerate(CV)}
    df_mod["CV"] = df_mod[CV_column].replace(map_to_int)

    return (df_mod, CV)


df2, targets = encode_CV(df, "percentChange")

#displaying new dataframe with numerical CV
#print("* df2.head()", df2[["CV", "percentChange"]].head(), sep="\n", end="\n\n")

expVars = list(df2.columns[:8])
print("* expVars:", expVars, sep="\n")

Y = df2["CV"]
X = df2[expVars]

#decTree = DecisionTreeClassifier(criterion = "entropy", splitter = 'random', max_leaf_nodes = 10, min_samples_leaf = 10, max_depth= 8)


decTree = DecisionTreeClassifier(criterion="entropy", max_depth=2, max_leaf_nodes = 10, max_features = 8, min_samples_leaf= 20, presort=True, splitter='best')
decTree.fit(X, Y)


#DecisionTreeClassifier(class_weight=None, criterion='entropy', max_depth=3, max_features=None, max_leaf_nodes=None, min_samples_leaf=5, min_samples_split=2, min_weight_fraction_leaf=0.0,
            #presort=False, random_state=100, splitter='best')

def visualize_tree(tree, feature_names):

    with open("decTree.dot", 'w') as f:
        export_graphviz(tree, out_file=f, feature_names=feature_names, filled=True)

    command = ["dot", "-Tpng", "decTree.dot", "-o", "decTreeBinary-Nov27.png"]
    try:
        subprocess.check_call(command)
    except:
        exit("Could not run dot, ie graphviz, to produce visualization")

    return

predict = decTree.predict(X)

print("Predictions: \n", np.array([predict]).T)

print("Probability of prediction: \n", decTree.predict_proba(X))

print("Feature importance: ", decTree.feature_importances_)

print("Accuracy score for the model: \n", decTree.score(X,Y))

#OPTION 1: for binary CV (up/down)
#print(metrics.confusion_matrix(Y, predict, labels=[0,1]))

#OPTION 2: for categorical CV (big up/up/down/big down)
print(metrics.confusion_matrix(Y, predict, labels=[0,1,2,3]))

visualize_tree(decTree, expVars)

#Calculating k-fold cross validation results
model = DecisionTreeClassifier()
k = 134
kf = KFold(n_splits=k)
scores = cross_val_score(model, X, Y, cv=kf)
print("MSE of every fold in fold cross validation: ", abs(scores))
print("Mean of the ", k, " fold cross validation: ", abs(scores.mean()))

#print("Does he attend class, if he gets 60 after putting 100 hours of effort: ", DT.predict([100,60]),DT.predict_proba([100,60]))










