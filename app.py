from flask import Flask, render_template
from dotenv import load_dotenv
from config import Config
import os
# Local development convenience ONLY. Loads personal values from
# .env.local if that file exists on your machine (it's gitignored).
# Cloud instances (Dev service / Prod service) never use this file -
# their env vars are injected directly by the platform dashboard,
# independent of which branch/commit is deployed.
load_dotenv(dotenv_path='.env.local')

app = Flask(__name__)

# Single config class - reads current environment values via os.getenv()
# at the moment this line runs, whatever those happen to be.
app.config.from_object(Config)

@app.route('/')
def hello():
    # Get environment-specific data from config
    app_name = app.config.get("APP_NAME")
    app_version = app.config.get("APP_VERSION")
    sample_data = app.config.get("SAMPLE_DATA")
    features = app.config.get("FEATURES")
    
    return render_template('index.html', 
                          app_name=app_name,
                          app_version=app_version,
                          sample_data=sample_data,
                          features=features)

@app.route('/user/<name>')
def greet_user(name):
    return f'Hello, {name}!'

@app.route('/api/data')
def get_data():
    """API endpoint that returns environment-specific data"""
    return {
        "environment": app.config.get("ENVIRONMENT"),
        "app_name": app.config.get("APP_NAME"),
        "users": app.config.get("SAMPLE_DATA")["users"],
        "stats": app.config.get("SAMPLE_DATA")["stats"],
        "features": app.config.get("FEATURES")
    }

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(debug=app.config.get("DEBUG"), host='0.0.0.0', port=port)