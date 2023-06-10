import requests
import json
import pandas as pd
from scripts.helper_functions import get_weighted_sample


def classify_soil_texture(sand, clay):
    """Function that returns the USDA 
    soil textural class given 
    the percent sand and clay.
    
    Inputs = percent of sand and clay
    """
    
    silt = 100 - sand - clay
    
    if sand + clay > 100 or sand < 0 or clay < 0:
        raise Exception('Inputs adds over 100% or are negative')

    elif silt + 1.5*clay < 15:
        textural_class = 'sand'

    elif silt + 1.5*clay >= 15 and silt + 2*clay < 30:
        textural_class = 'loamy sand'

    elif (clay >= 7 and clay < 20 and sand > 52 and silt + 2*clay >= 30) or (clay < 7 and silt < 50 and silt + 2*clay >= 30):
        textural_class = 'sandy loam'

    elif clay >= 7 and clay < 27 and silt >= 28 and silt < 50 and sand <= 52:
        textural_class = 'loam'

    elif (silt >= 50 and clay >= 12 and clay < 27) or (silt >= 50 and silt < 80 and clay < 12):
        textural_class = 'silt loam'

    elif silt >= 80 and clay < 12:
        textural_class = 'silt'

    elif clay >= 20 and clay < 35 and silt < 28 and sand > 45:
        textural_class = 'sandy clay loam'

    elif clay >= 27 and clay < 40 and sand > 20 and sand <= 45:
        textural_class = 'clay loam'

    elif clay >= 27 and clay < 40 and sand <= 20:
        textural_class = 'silty clay loam'

    elif clay >= 35 and sand > 45:
        textural_class = 'sandy clay'

    elif clay >= 40 and silt >= 40:
        textural_class = 'silty clay'

    elif clay >= 40 and sand <= 45 and silt < 40:
        textural_class = 'clay'

    else:
        textural_class = 'na'

    return textural_class
        

def get_soil_data(id, latitude, longitude, weighted_sampling=False):
    """
    Function that returns the 0-100cm soil properties from isric soilgrids.
    If weighted_sampling=True, 4 points making a 50 x 50 meter box around the center point will also be sampled and     all 5 points will be averaged for the final returned data.
    """
    final_latitude = latitude
    final_longitude = longitude

    if weighted_sampling == True:
        weighted_df = get_weighted_sample(latitude, longitude)
    else:
        weighted_df = pd.DataFrame({'latitude': [latitude],
                                    'longitude': [longitude]})

    final_soil_df = pd.DataFrame()
    
    for index, row in weighted_df.iterrows():
        latitude = row['latitude']
        longitude = row['longitude']
        
        # isric api
        isric_url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={longitude}&lat={latitude}&property=bdod&property=cec&property=clay&property=phh2o&property=sand&property=silt&depth=0-5cm&depth=0-30cm&depth=5-15cm&depth=15-30cm&depth=30-60cm&depth=60-100cm&depth=100-200cm&value=mean&value=uncertainty"
        response = requests.get(url=isric_url, verify=True)
        
        content = json.loads(response.content.decode('utf-8'))
        
        df1 = pd.DataFrame.from_dict(content, orient='index')
        
        df2 = pd.DataFrame.from_dict(df1[0]['properties'],orient='index').transpose()
        
        soil_df = pd.DataFrame({'depth': ['0-5-cm', '5-15cm', '15-30cm', '30-60cm', '60-100cm', '100-200cm']})
        
        for i in range(0, len(df2)):
            one_col = pd.DataFrame({df2.layers[i]['name']: [df2.layers[i]['depths'][0]['values']['mean'],
                                                            df2.layers[i]['depths'][1]['values']['mean'],
                                                            df2.layers[i]['depths'][2]['values']['mean'],
                                                            df2.layers[i]['depths'][3]['values']['mean'],
                                                            df2.layers[i]['depths'][4]['values']['mean'],
                                                            df2.layers[i]['depths'][5]['values']['mean']]})
        
            soil_df = pd.concat([soil_df, one_col], axis=1)
        
        soil_df.columns = ['depth', 'bulk_density', 'cec', 'clay', 'ph', 'sand', 'silt']

        # convert data to 'normal' units
        soil_df['bulk_density'] = soil_df['bulk_density'] * 0.01
        soil_df['cec'] = soil_df['cec'] * 0.1
        soil_df['clay'] = soil_df['clay'] * 0.1
        soil_df['ph'] = soil_df['ph'] * 0.1
        soil_df['sand'] = soil_df['sand'] * 0.1
        soil_df['silt'] = soil_df['silt'] * 0.1
    
        # only keep the top 5 soil layers 0 - 100cm. This is mainly the root zone.
        soil_df = soil_df.head(5)
        soil_df.drop('depth', axis=1, inplace=True)

        # add the data id, lat, and long to the data
        soil_df['id'] = id
        soil_df['latitude'] = latitude
        soil_df['longitude'] = longitude
    
        # take the average of the top 5 soil layers 0 - 100cm
        soil_df = soil_df.groupby(['id', 'latitude','longitude']).mean().reset_index()

        final_soil_df = pd.concat([final_soil_df, soil_df])

    final_soil_df = final_soil_df.drop(['id', 'latitude', 'longitude'], axis=1)

    # add the data id, lat, and long to the data
    final_soil_df['id'] = id
    final_soil_df['latitude'] = final_latitude
    final_soil_df['longitude'] = final_longitude
    final_soil_df = final_soil_df.groupby(['id', 'latitude','longitude']).mean().reset_index()

    sand = final_soil_df['sand'][0]
    clay = final_soil_df['clay'][0]
    
    final_soil_df['soil_texture'] = classify_soil_texture(sand, clay)

    return final_soil_df
