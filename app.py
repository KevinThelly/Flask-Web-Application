from flask import Flask, render_template, jsonify, request, redirect, url_for, flash
import sqlite3
import os.path
from datetime import datetime
from wtforms import Form, StringField, TextAreaField, DateField, BooleanField
import logging


app = Flask(__name__)
app.debug=True
app.config['SECRET_KEY'] = 'you-will-never-guess'


def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d



# , methods=['GET']
@app.route('/',methods=['GET','POST'])
def api_all():
    form=TaskEntry(request.form)
    conn = sqlite3.connect('Database/test.db')

    if request.method=='POST':
        # form=TaskEntry(request.form)
        
        t1=form.task.data
        d1=form.date.data
        query="select ID from TASKS ORDER BY id DESC LIMIT 1;"
        cur=conn.cursor()
        id=cur.execute(query).fetchall()


        query="INSERT INTO TASKS(ID,Task,Due_By,Status) VALUES("+str(id[0][0]+1)+",'"+str(t1)+"','"+str(d1)+"','Not Started');"
        # conn = sqlite3.connect('Database/test.db')
        # conn.row_factory = dict_factory
        cur= conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return redirect(url_for('api_all'))
    
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute("SELECT * FROM TASKS where Status !='Finished' ;")
    
    return render_template('tasks.html',Tasks=tasks, form=form)

    
@app.route("/due",methods=['GET'])
def getdue():
    query_parameters=request.args
    duedate=query_parameters.get('due_date')
    query="SELECT * FROM TASKS WHERE Due_By = '" + duedate + "';"
    conn = sqlite3.connect('Database/test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute(query)
    return render_template('onlytasks.html',Tasks=tasks)

@app.route("/finished",methods=['GET'])
def getfin():
    query="SELECT * FROM TASKS WHERE Status = 'Finished' ;"
    conn = sqlite3.connect('Database/test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute(query)
    return render_template('onlytasks.html',Tasks=tasks)

@app.route("/overdue",methods=['GET'])
def getoverdue():
    today=datetime.today().strftime('%Y-%m-%d')
    query="SELECT * FROM TASKS WHERE Due_By < '" + today + "';"
    conn = sqlite3.connect('Database/test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    tasks = cur.execute(query)
    return render_template('onlytasks.html',Tasks=tasks)


class TaskEntry(Form):
    task=StringField('Task')
    date=DateField('Duedate')


app.run()