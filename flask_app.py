#!/usr/bin/env python3
from flask import Flask, render_template, request
import geoip2.database

app = Flask(__name__)
reader = geoip2.database.Reader('GeoLite2-City.mmdb')

def log(message):
    with open('request_logs.log', 'a') as f:
        f.write(message + '\n')


@app.route('/')
def hello():
     # Get the IP address of the client
    ip_address = request.remote_addr

    # Get approximate location based on IP address
    try:
        response = reader.city(ip_address)
        country = response.country.name
        city = response.city.name
        latitude = response.location.latitude
        longitude = response.location.longitude

        # Log IP address and location information
        log_message = f"IP Address: {ip_address}, Country: {country}, City: {city}, Latitude: {latitude}, Longitude: {longitude}"

    except geoip2.errors.AddressNotFoundError:
        log_message = f"IP Address: {ip_address}, Location not found"
    log(log_message)
    return 'V1'

@app.route('/flan')
def flan():
    return 'flan de pate'

@app.route('/index')
def index():
    return render_template('3.html')

if __name__ == '__main__':
    app.run(port=8080)
