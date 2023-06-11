from geopy.distance import distance, geodesic
from geopy.point import Point
import pandas as pd


def get_weighted_sample(latitude, longitude):
    '''
    function is to get approximately a 50 meter box around the center point for weighted sampling.
    '''
    # Center latitude and longitude
    center_latitude = latitude
    center_longitude = longitude
        
    # Converter to get degrees to meters
    distance_converter = 2800
    
    # Calculate distance in degrees using geopy
    distance_degrees = distance(meters=distance_converter).kilometers / 111.0
    
    # Create center point
    center_point = Point(center_latitude, center_longitude)
    
    # Calculate latitude and longitude boundaries
    north_point = geodesic(kilometers=distance_degrees).destination(center_point, 0)
    south_point = geodesic(kilometers=distance_degrees).destination(center_point, 180)
    east_point = geodesic(kilometers=distance_degrees).destination(center_point, 90)
    west_point = geodesic(kilometers=distance_degrees).destination(center_point, 270)
    
    # Retrieve latitude and longitude coordinates
    north_latitude, north_longitude = north_point.latitude, north_point.longitude
    south_latitude, south_longitude = south_point.latitude, south_point.longitude
    east_latitude, east_longitude = east_point.latitude, east_point.longitude
    west_latitude, west_longitude = west_point.latitude, west_point.longitude
    
    weighted_df = pd.DataFrame({'latitude': [center_latitude, north_latitude, north_latitude, south_latitude, south_latitude],
                                'longitude': [center_longitude, west_longitude, east_longitude, west_longitude, east_longitude]})


    return weighted_df
