from datetime import datetime
from meteostat import Point
from meteostat import Hourly 
from meteostat import Daily
from meteostat import Monthly
import pandas as pd


def get_meteostat_data(id, type, latitude, longitude, start_date, end_date) -> pd.DataFrame:
    '''
    Function pulls weather data from meteostat. Data can be hourly, daily, or monthly.
    '''
    start = start_date
    end = end_date
    place = Point(latitude, longitude)

    if type == 'hourly':
        # Get hourly data
        final_weather_data = Hourly(place, start, end)
        final_weather_data = final_weather_data.fetch()
        data_col = ['time', 'temp', 'dwpt', 'rhum', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun', 'coco']
    elif type == 'daily':
        # Get daily data
        final_weather_data = Daily(place, start, end)
        final_weather_data = final_weather_data.fetch()
        data_col = ['time', 'tavg', 'tmin', 'tmax', 'prcp', 'snow', 'wdir', 'wspd', 'wpgt', 'pres', 'tsun']
    elif type == 'monthly':
        # Get daily data
        final_weather_data = Monthly(place, start, end)
        final_weather_data = final_weather_data.fetch()
        data_col = ['time', 'tavg', 'tmin', 'tmax', 'prcp', 'wspd', 'pres', 'tsun']
    else:
        print('Invalid type, please use hourly, daily, or monthly for input')
        
    final_weather_data = pd.DataFrame(final_weather_data).reset_index()

    # add the data id, lat, and long to the data
    final_weather_data['id'] = id
    final_weather_data['latitude'] = latitude
    final_weather_data['longitude'] = longitude

    final_weather_data = final_weather_data[['id', 'latitude', 'longitude'] + data_col]
    
    return final_weather_data
    