from flask import Flask, render_template, request, redirect, url_for, send_from_directory, flash
import pandas as pd
import os
import subprocess
import threading
import logging
from flask_socketio import SocketIO, emit

app = Flask(__name__, template_folder='../templates')
app.secret_key = 'supersecretkey'
socketio = SocketIO(app, async_mode='eventlet')
UPLOAD_FOLDER = '../data/'
RESUME_FOLDER = '../resumes/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESUME_FOLDER'] = RESUME_FOLDER

process = None

if not os.path.exists(RESUME_FOLDER):
    os.makedirs(RESUME_FOLDER)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

def run_script():
    global process
    script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'linkedin_automation.py'))
    process = subprocess.Popen(['python', script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    for stdout_line in iter(process.stdout.readline, ""):
        socketio.emit('log_message', {'message': stdout_line.strip()})
    process.stdout.close()

@app.route('/')
def index():
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        entries = df.to_dict(orient='records')
    else:
        entries = []
    return render_template('index.html', entries=enumerate(entries))

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv'))
        flash('File successfully uploaded')
        return redirect(url_for('index'))

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    if 'resume' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['resume']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        resume_path = os.path.join(app.config['RESUME_FOLDER'], file.filename)
        file.save(resume_path)
        
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
        else:
            df = pd.DataFrame(columns=['First Name', 'Last Name', 'Phone', 'Email', 'Resume Path', 'Job Application URL'])
        
        new_entry = pd.DataFrame([{
            'First Name': '',
            'Last Name': '',
            'Phone': '',
            'Email': '',
            'Resume Path': resume_path,
            'Job Application URL': ''
        }])
        
        df = pd.concat([df, new_entry], ignore_index=True)
        df.to_csv(csv_path, index=False)
        
        flash('Resume successfully uploaded and added to CSV')
        return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_entry():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    phone = request.form['phone']
    email = request.form['email']
    resume_path = request.form['resume_path']
    job_url = request.form['job_url']
    
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
    else:
        df = pd.DataFrame(columns=['First Name', 'Last Name', 'Phone', 'Email', 'Resume Path', 'Job Application URL'])
    
    new_entry = pd.DataFrame([{
        'First Name': first_name,
        'Last Name': last_name,
        'Phone': phone,
        'Email': email,
        'Resume Path': resume_path,
        'Job Application URL': job_url
    }])
    
    df = pd.concat([df, new_entry], ignore_index=True)
    df.to_csv(csv_path, index=False)
    
    flash('Entry successfully added')
    return redirect(url_for('index'))

@app.route('/delete/<int:index>', methods=['POST'])
def delete_entry(index):
    csv_path = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        df = df.drop(index)
        df.to_csv(csv_path, index=False)
    flash('Entry successfully deleted')
    return redirect(url_for('index'))

@app.route('/download')
def download_file():
    return send_from_directory(app.config['UPLOAD_FOLDER'], 'data.csv')

@app.route('/run_automation')
def run_automation():
    thread = threading.Thread(target=run_script)
    thread.start()
    flash('Automation started')
    return render_template('run_automation.html')

@app.route('/stop_automation')
def stop_automation():
    global process
    if process:
        process.terminate()
        process = None
        flash('Automation stopped')
    return redirect(url_for('index'))

@socketio.on('connect')
def handle_connect():
    emit('log_message', {'message': 'Connected to server'})

if __name__ == '__main__':
    socketio.run(app, debug=True)
