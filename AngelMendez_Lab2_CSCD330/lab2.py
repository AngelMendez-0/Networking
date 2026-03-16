#! /usr/bin/env python3
# author: Angel Mendez

from json import loads  # steps 3, 4
from requests import get  # steps 3, 4
from socket import gethostbyname  # step 1
from subprocess import getstatusoutput  # step 2
from sys import argv  # command line arguments
import matplotlib.pyplot as plt  # for plotting
import numpy as np  # for plotting

# Takes an array of temps and plots them.
def plot_temps(temps):
    xs = [x for x in range(len(temps))]
    plt.plot(xs, temps, label="Hourly temperatures")

    # Label axes
    plt.xlabel("Hour")
    plt.ylabel("Temperature F.")
    plt.legend()
    plt.show()


def main():
    if len(argv) < 2:
        print("Usage: python3 lab2.py <domain>")
        return
        
    domain = argv[1]
    ip = gethostbyname(domain)
    print(f"IP address of {domain}: {ip}")

    status, whois_output = getstatusoutput(f"whois {ip}")
    if status != 0:
        print("Error fetching WHOIS info")
        return

    print("\nWHOIS info:")
    print(whois_output[:500])  # just first 500 chars to avoid huge output

    lines = whois_output.splitlines()
    address_lines = [line for line in lines if "City" in line or "State" in line or "Address" in line]
    if not address_lines:
        print("Could not extract address from WHOIS info")
        return
    physical_address = " ".join([line.split(":")[1].strip() for line in address_lines])
    print(f"\nPhysical address: {physical_address}")

    census_api = "https://geocoding.geo.census.gov/geocoder/locations/onelineaddress"
    params = {
        "address": physical_address,
        "benchmark": "Public_AR_Current",
        "format": "json"
    }
    response = get(census_api, params=params)
    js = loads(response.text)

    try:
        coords = js['result']['addressMatches'][0]['coordinates']
        lat = coords['y']
        lon = coords['x']
        print(f"Latitude: {lat}, Longitude: {lon}")
    except IndexError:
        print("Could not find coordinates for address")
        return

    weather_api = f"https://api.weather.gov/points/{lat},{lon}"
    response = get(weather_api)
    js = loads(response.text)

    try:
        forecast_hourly_URL = js['properties']['forecastHourly']
    except KeyError:
        print("Could not get hourly forecast URL")
        return

    response = get(forecast_hourly_URL)
    js = loads(response.text)

    temps = [period['temperature'] for period in js['properties']['periods']] 
    print(f"\nHourly temperatures: {temps}")

    plot_temps(temps)


if __name__ == "__main__":
    main()

