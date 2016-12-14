import os
import requests
from subprocess import call

from flask import Flask, render_template, request, session

PROJECT_ROOT = os.path.dirname(__file__)

SAY_COMMAND = 'say'

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

def say(text):
    command = [SAY_COMMAND, text]
    call(command)

def play(_file='dong.wav'):
    command = ['play', os.path.join(PROJECT_ROOT, _file)]
    call(command)

@app.route("/", methods=['GET', 'POST'])
def home():
    text = request.args.get('text')
    if request.method == 'POST':
        text = request.form['text']
        if not session.get('texts'):
            session['texts'] = []
        session['texts'].append(text)
        session.modified = True
        session.permanent = True
    if text:
        say(text)
    return render_template('home.html')

@app.route("/dong/", methods=['POST'])
def dong():
    if request.method == 'POST':
        play()
    return 'ok'

@app.route("/gif/<search_term>", methods=['POST'])
def gif(search_term):
    giphy_url = 'http://api.giphy.com/v1/gifs/search?q=%s&api_key=dc6zaTOxFJmzC'

    results = requests.get(giphy_url % search_term)
    data = results.json()
    download_link = data['data'][0]['images']['downsized']['url']
    r = requests.get(download_link)
    
    file_path = '/tmp/ft.gif'

    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)

        call(['timeout', '10', 'send-video', '-h', 'ft.noise', '-l', '15', file_path])

    return 'ok'

if __name__ == "__main__":
    app.run('0.0.0.0')
