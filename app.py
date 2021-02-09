from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__) # Initialize Flask app variable
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' # Set link/source of Database 
db = SQLAlchemy(app) # Initialize the database

# Todo class/entity inherting the base for each enitty/model
class Todo(db.Model):

    id=db.Column(db.Integer,primary_key=True)
    content=db.Column(db.String(200),nullable=False)
    completed = db.Column(db.Integer,default=0)
    date_created = db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self): #Comparable with the toString() method in Java
        return '<Task %r' % self.id

# Main page / Add tasks / View Tasks
@app.route('/',methods=['POST','GET'])
def index():

    if request.method == 'POST':
        task_content = request.form['content'] # Take the input of user and store it
        new_task = Todo(content=task_content) # Initialize new object

        try:
            db.session.add(new_task) # Add new task to the database
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue creating a new Task'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        # Everytime loading the route '/' So the home page we try to get all Tasks
        # Comparable with named_query in SPring boot java
        # Translation in SQL
        # SELECT * FROM Todo Order By date_created
        # And send the retrieved tasks to the template html page
        return render_template('index.html',tasks=tasks)

# Delete Task
@app.route('/delete/<int:id>')
def delete(id):
    # Try to get the task with the id provided by the user
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'Something went wrong trieng to delete a task'


# Update Task - Comparable with Spring Controller endpoints 
@app.route('/update/<int:id>', methods=['POST','GET'])
def update(id):

    # Try to get the task with the id provided by the user
    task_to_update = Todo.query.get_or_404(id)

    if request.method == 'POST':
        try:
           task_to_update.content = request.form['content']
           db.session.commit()
           return redirect('/')
        except: 
            return 'Updating Task Failed'
    else:
        return render_template('update.html', task = task_to_update)

# Main shizzle? 
if __name__ == '__main__':
    app.run(debug=True)
