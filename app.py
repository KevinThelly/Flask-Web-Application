from flask import Flask, render_template, jsonify, request
import sqlite3
import os.path


app = Flask(__name__)
app.debug=True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


# , methods=['GET']
@app.route('/')
def api_all():
    conn = sqlite3.connect('Database/test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute('SELECT * FROM TASKS;')
    return render_template('tasks.html',Tasks=tasks)

    
@app.route("/due",methods=['GET'])
def getdue():
    query_parameters=request.args
    duedate=query_parameters.get('due_date')
    query="SELECT * FROM TASKS WHERE Due_By = '" + duedate + "';"
    conn = sqlite3.connect('Database/test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute(query)
    return render_template('tasks.html',Tasks=tasks)

@app.route("/finished",methods=['GET'])
def getfin():
    query="SELECT * FROM TASKS WHERE Status = 'Finished' ;"
    conn = sqlite3.connect('Database/test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute(query)
    return render_template('tasks.html',Tasks=tasks)





app.run()