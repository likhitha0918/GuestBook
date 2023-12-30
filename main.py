from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///messages.db'  # Use any preferred DB connection

db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(100))
    content = db.Column(db.Text)
    created = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def index():
    messages = Message.query.order_by(Message.created.desc()).all()
    return render_template('templates.html', messages=messages)

@app.route('/sign', methods=['POST'])
def sign():
    author = request.form.get('author')
    content = request.form.get('content')

    if author and content:
        new_message = Message(author=author, content=content)
        db.session.add(new_message)
        db.session.commit()
        return redirect(url_for('index'))
    else:
        error = "Please enter both your name and a message!"
        return render_template('templates.html', error=error)

if __name__ == '__main__':
    db.create_all()
    app.run()
