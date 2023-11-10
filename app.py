from flask import Flask, render_template, request, url_for, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.app_context().push()
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class TODO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable= False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' %self.id 

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_name = request.form['name']
        new_task = TODO(name=task_name)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding your Task!"
    else:
        tasks = TODO.query.order_by(TODO.date).all()
        return render_template("index.html", tasks=tasks)
@app.route('/delete/<int:id>')
def delete(id):
    task_to_del = TODO.query.get_or_404(id)

    try:
        db.session.delete(task_to_del)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting that task!"
    
@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    task = TODO.query.get_or_404(id)
    if request.method == 'POST':
        task.name = request.form['name']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was a problem updating the task!"
    else:
        return render_template('update.html', task= task)



if __name__=="__main__":
    app.run(debug=True) 