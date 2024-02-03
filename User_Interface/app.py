from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from calls import call

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    complete = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])

def index():
    if request.method == 'POST':
        print(request.form)
        task_content = request.form['link']
        new_task = Todo(content=task_content)
        songs = call(task_content)
        #try:
         #   db.session.add(new_task)
          #  db.session.commit()
           # return redirect('/')
        #except:
         #   return 'There was an issue adding the task'
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
    
    


# import sys
# print(sys.executable)