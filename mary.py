from subprocess import call

from flask import Flask, render_template, request, session

SAY_COMMAND = 'say'

app = Flask(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'

def say(text):
    command = [SAY_COMMAND, text]
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

if __name__ == "__main__":
    app.run('0.0.0.0')
