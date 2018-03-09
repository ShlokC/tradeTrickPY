from flask import Flask, jsonify, render_template
import pypyodbc
import os
import numpy as np
import io
import base64
from pandas import datetime
import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.cross_validation import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn import tree
import matplotlib.pyplot as plt
app = Flask(__name__)

@app.route('/')
def hello_world():
 
  Connection = pypyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:tradetricksql.database.windows.net,1433;Database=tradeTrickDB;Uid=shlok@tradetricksql;Pwd=MySQL@01;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
  
  cursor = Connection.cursor()
  SQLCommand = ("SELECT * FROM BankNiftyData WHERE id > ?")
  values = [2]
  cursor.execute(SQLCommand,values)
  results = cursor.fetchall()
  #print(results)
  return jsonify(results)
  #return 'Hello, World!'
@app.route('/linearRegression')
def linearRegression():
  try:
    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    filename_path = os.path.join(THIS_FOLDER, 'timedata.csv')
    balance_data = pd.read_csv(filename_path, sep= ',',header= 0)
    headers = list(balance_data.columns.values)
    X = balance_data.values[:,1]
    X =X.reshape(X.size, 1)
    Y = balance_data.values[:,0]
    Y =Y.reshape(Y.size, 1)
    X_train, X_test, y_train, y_test = train_test_split( X, Y, test_size = 0.3, random_state = 100)
    # Create linear regression object
    regr = linear_model.LinearRegression()
    # Train the model using the training sets
    regr.fit(X_train, y_train)
    # Make predictions using the testing set
    y_pred = regr.predict(X_test)

    # The coefficients
    print('Coefficients: \n', regr.coef_)
    # The mean squared error
    print("Mean squared error: %.2f"
      % mean_squared_error(y_test, y_pred))
    mse =mean_squared_error(y_test, y_pred)
    # Explained variance score: 1 is perfect prediction
    print('Variance score: %.2f' % r2_score(y_test, y_pred))
    vScr= r2_score(y_test, y_pred)
    # Plot outputs
    plt.scatter(X_test, y_test,  color='green')
    plt.plot(X_test, y_pred, color='blue', linewidth=3)
    plt.xticks(())
    plt.yticks(())
    plt.show()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    data = base64.encodestring(img.getvalue())

    plot_url = base64.b64encode(img.getvalue()).decode()
    img_tag ='<img src="data:image/png;base64,{}">'.format(plot_url)
    return render_template('output.html',Coefficients=regr.coef_, mse=mse, vscr=vScr, result=data.decode('utf8'))
  except OSError as err:
    return jsonify(err)
if __name__ == '__main__':
  app.run()
