from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)


class ToDoWithFlask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(150))
    completed = db.Column(db.Boolean)

    def __repr__(self):
        return f"ToDoWithFlask('{self.content}')"



@app.route('/')
@app.route('/todo')
def todo():
    completed_todo_items = ToDoWithFlask.query.filter_by(completed=True).all()
    incomplete_todo_items = ToDoWithFlask.query.filter_by(completed=False).all()
    return render_template('index.html', title='Todo List App', completed_todos=completed_todo_items, incomplete_todos=incomplete_todo_items)


@app.route('/add', methods=['POST'])
def add():
    todo_item = ToDoWithFlask(content=request.form['todo'], completed=False)
    db.session.add(todo_item)
    db.session.commit()
    return redirect(url_for('todo'))


@app.route('/completed/<id>')
def completed(id):
    todo_item = ToDoWithFlask.query.get(id)
    todo_item.completed = True
    db.session.commit()
    return redirect(url_for('todo'))



@app.route('/delete/<id>')
def delete(id):
    todo_item = ToDoWithFlask.query.get(id)
    db.session.delete(todo_item)
    db.session.commit()
    return redirect(url_for('todo'))




if __name__ == '__main__':
    app.run(debug=True)