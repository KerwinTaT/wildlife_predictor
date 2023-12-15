from flask import Flask, render_template, request
from api_handler import ApiHandler
from data_processor import DataProcessor

app = Flask(__name__)

# Instantiate ApiHandler with API keys
api_handler = ApiHandler(openweathermap_api_key="ee9e8dc99954f000e07a583dfd152412", opencage_api_key="b8cd8b7ad6cd4435b414a0dc4d742d09")

def extract_lat_lon_from_location(project_location):
    lat, lon = project_location.split(', ')
    return float(lat), float(lon)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Retrieve user input from the form (you'll need to adjust this based on your form fields)
    project_location = request.form.get('project_location')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    project_description = request.form.get('project_description')

    latitude, longitude = extract_lat_lon_from_location(project_location)
    # Use ApiHandler to get data from APIs
    openweathermap_data = api_handler.get_openweathermap_data(latitude, longitude, start_time, end_time)
    geocoding_data = api_handler.get_geocoding_data(project_location)

    # Process the data using DataProcessor
    processor = DataProcessor(openweathermap_data, geocoding_data)
    processed_data = processor.process_all_data()

    # Render the result page with processed data
    return render_template('result.html', processed_data=processed_data)

if __name__ == '__main__':
    app.run(debug=True)
