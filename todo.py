import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'example.db')
# SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
app.config['SQLALCHEMY_DATABASE_URI']=SQLALCHEMY_DATABASE_URI
db= SQLAlchemy(app)
class ToDo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(200))

@app.route("/")
def index():
    todos=ToDo.query.all()
    return render_template('index.html',todos=todos)

@app.route("/add", methods=['POST'])
def add():
    todo = ToDo(text=request.form['todoitem'])
    db.session.add(todo)
    db.session.commit()
    return redirect('/')


@app.route("/delete/<int:id>")
def delete(id):
    task = ToDo.query.get(id)
    # abc=task.text
    db.session.delete(task)
    db.session.commit()
    # return '{}'.format(abc)
    return redirect('/')

@app.route("/edit/<int:id>/<text>")
def edit(id, text):
    todos=ToDo.query.all()
    task = ToDo.query.get(id)
    db.session.delete(task)
    # db.session.add(task)
    db.session.commit()
    return render_template('index.html', todos=todos, val = text )

if __name__ == "__main__":
    app.run(debug=True)
