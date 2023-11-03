import os
from flask import Flask, send_file

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello world'

@app.route('/dataset')
def get_dataset():
    csv_dir  = './static'
    csv_file = 'dataset.csv'
    csv_path = os.path.join(csv_dir, csv_file)

    if not os.path.isfile(csv_path):
        return f'ERROR: file {csv_file} was not found on the server'
    # Send the file back to the client
    return send_file(csv_path, as_attachment=True)