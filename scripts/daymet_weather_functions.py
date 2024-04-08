import pandas as pd
import requests
from datetime import datetime, timedelta
import math
import io


def calculate_pet(tmax, tmin, srad, vp, dayl, tavg):
    # Constants
    lambda_ = 2.45  # Latent heat of vaporization (MJ/kg)
    gamma = 0.067  # Psychrometric constant (kPa/°C)
    delta = 4098.0  # Slope of the vapor pressure curve (kPa/°C)
    Cn = 37.0  # Numerator constant
    Cd = 0.34  # Denominator constant

    # Calculate the saturation vapor pressure
    es = 0.6108 * math.exp((17.27 * tmax) / (tmax + 237.3))

    # Calculate the actual vapor pressure
    ea = vp / 1000.0

    # Calculate the slope of the vapor pressure curve
    delta_s = delta * (es / (tavg + 273.3) ** 2)

    # Calculate the net radiation
    Rn = (1 - 0.23) * srad

    # Calculate the PET using the Penman-Monteith equation
    pet = ((delta_s * Rn) + (Cn * (vp / 1000.0 - ea) / dayl) * gamma) / (delta_s + gamma * (1 + Cd * (vp / 1000.0 - ea) / dayl))

    return pet



def get_weather_data(id, latitude, longitude, start_date, end_date):
    # Specify the API endpoint URL
    url = f"https://daymet.ornl.gov/single-pixel/api/data?lat={latitude}&lon={longitude}&vars=dayl,prcp,srad,tmax,tmin,vp&start={start_date}&end={end_date}&format=csv"
    
    # Send a GET request to the API endpoint
    response = requests.get(url=url, verify=True)
    df = pd.read_csv(io.BytesIO(response.content), skiprows=6)
    # Add meta data
    df['id'] = id
    df['latitude'] = latitude
    df['longitude'] = longitude
    df['tavg (deg c)'] = df[['tmax (deg c)', 'tmin (deg c)']].mean(axis=1)

    # Get date, potential evapotranspiration 
    for index, row in df.iterrows():
        date = datetime(year=int(row['year']), month=1, day=1) + timedelta(days=int(row['yday']) - 1)
        df.at[index, 'date'] = date
        pet = calculate_pet(row['tmax (deg c)'], row['tmin (deg c)'], row['srad (W/m^2)'], row['vp (Pa)'], row['dayl (s)'], row['tavg (deg c)'])
        df.at[index, 'pet'] = pet

    df = df[['id', 'latitude', 'longitude', 'year', 'yday', 'date', 'dayl (s)', 'prcp (mm/day)', 'tmin (deg c)', 'tmax (deg c)', 'tavg (deg c)', 'srad (W/m^2)', 'vp (Pa)', 'pet (mm/day)']]
    
    return df
