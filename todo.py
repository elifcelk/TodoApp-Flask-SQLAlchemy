from logging import debug
from flask import Flask,redirect,url_for,request
from flask.templating import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/elifc/Desktop/TodoApp/todo.db'
db = SQLAlchemy(app)
@app.route("/")
def index():
    todos = Todo.query.all() #veritabanındaki her bir verinin özelliğini sözlük yapısı şeklinde alır
    return render_template("index.html",todos=todos)

@app.route("/complete/<string:id>")
def completeTodo(id):
    todo=Todo.query.filter_by(id = id).first() #id ye göre filtreleyip değişkene atadık
    todo.complete=not todo.complete #complete durumunu terse çevirdik

    db.session.commit()
    return redirect(url_for("index"))


@app.route("/add",methods=["POST"])
def addTodo():
    title=request.form.get("title")
    newTodo=Todo(title = title,complete=False)
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo=Todo.query.filter_by(id = id).first() #id ye göre filtreleyip değişkene atadık
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title= db.Column(db.String(80))
    complete = db.Column(db.Boolean)

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)

