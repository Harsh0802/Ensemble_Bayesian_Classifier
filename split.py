import pandas as pd
import csv
from sklearn.model_selection import train_test_split
data=pd.read_csv('final_data.csv')
#print(data.head())
#data.columns = ['Birads', 'Ages','Mass Shape','Mass Margin','Mass Density','Result']
#data.to_csv('final_data.csv')
y = data.Result
X = data.drop('Result', axis=1)
#print(y)
#print(X)
X_train, X_test, y_train, y_test = train_test_split(data,data,test_size=0.3)
print("\nX_train:\n")
print(X_train)
X_train.to_csv('train.csv')
print(X_train.shape)
print("\nX_test:\n")
print(X_test)
X_test.to_csv('test.csv')
print(X_test.shape)
