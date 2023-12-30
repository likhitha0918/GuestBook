from flask 
import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy 
import SQLAlchemy
from datetime 
import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  # Use your preferred DB connection
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    messages = Message.query.order_by(Message.created.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/sign', methods=['POST'])
def sign():
    author = request.form['author']
    content = request.form['content']

    if author and content:
        new_message = Message(author=author, content=content)
        db.session.add(new_message)
        db.session.commit()
    else:
        error = "Please enter both your name and a message!"
        return render_template('error.html', error=error)

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
