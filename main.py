from flask import Flask, render_template, request, redirect, url_for
from google.cloud import ndb
from datetime import datetime

app = Flask(__name__)
app.config['DEBUG'] = True

# Set up Google Cloud NDB client
client = ndb.Client()

class Message(ndb.Model):
    author = ndb.StringProperty()
    content = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)

@app.route('/')
def index():
    with client.context():
        messages = Message.query().order(-Message.created).fetch()
        return render_template('templates.html', messages=messages)

@app.route('/sign', methods=['POST'])
def sign():
    author = request.form.get('author')
    content = request.form.get('content')

    if author and content:
        with client.context():
            message = Message(author=author, content=content)
            message.put()
        return redirect('/')
    else:
        error = "Please enter both your name and a message!"
        return render_template('templates.html', error=error)

if __name__ == '__main__':
    app.run()
