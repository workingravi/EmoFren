from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    therapies = ['supportive', 'collaborative', 'challenging']
    return render_template('index.html', therapies=therapies)

@app.route('/handle_data', methods=['POST'])
def handle_data():
    username = request.form['username']
    tt = request.form['therapist_type']
    domain = request.form['domain']
    l1="username="+username+'\n'
    l2="therapist_type="+tt+'\n'
    l3="domain="+domain+'\n'
    lines = [l1, l2, l3] 
    with open('params.txt', 'w') as f:
        f.writelines(lines)
    return render_template('index.html', therapies=[])