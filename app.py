import os
import json
from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
CORS(app)

# Function to read data from a JSON file
def read_data_from_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    else:
        return []

@app.route('/')
def index():
    return "Flask server is running!"

@app.route('/api/data', methods=['GET'])
def get_data():
    file_path = r"C:\Users\shain\OneDrive\Desktop\sample2.json"  # Corrected file path
    data = read_data_from_file(file_path)
    df = pd.DataFrame(data)
    return jsonify(df.to_dict(orient='records'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
