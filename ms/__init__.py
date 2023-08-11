from flask import Flask
import joblib


# Initialize App
app = Flask(__name__, template_folder='templates')

# Load models
model = joblib.load('model/model_binary.dat.gz')
