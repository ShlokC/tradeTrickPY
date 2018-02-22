from flask import Flask, jsonify
import pypyodbc 
app = Flask(__name__)

@app.route('/')
def hello_world():
 
  Connection = pypyodbc.connect('Driver={ODBC Driver 13 for SQL Server};Server=tcp:tradetricksql.database.windows.net,1433;Database=tradeTrickDB;Uid=shlok@tradetricksql;Pwd=MySQL@01;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
  
  cursor = Connection.cursor()
  SQLCommand = ("SELECT * FROM BankNiftyData WHERE id > ?")
  values = [2]
  cursor.execute(SQLCommand,values)
  results = cursor.fetchone()
  print(results)
  return jsonify(results)
  #return 'Hello, World!'

if __name__ == '__main__':
  app.run()
