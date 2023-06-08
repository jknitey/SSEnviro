import requests
import json
import pandas as pd


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
        

def get_soil_data(id, latitude, longitude):
    """
    Function that returns the 0-100cm soil properties from isric soilgrids

    Inputs = location identifier, latitude, longitude
    """
    # isric api
    isric_url = f"https://rest.isric.org/soilgrids/v2.0/properties/query?lon={longitude}&lat={latitude}&property=bdod&property=cec&property=clay&property=phh2o&property=sand&property=silt&depth=0-5cm&depth=0-30cm&depth=5-15cm&depth=15-30cm&depth=30-60cm&depth=60-100cm&depth=100-200cm&value=mean&value=uncertainty"
    response = requests.get(url=isric_url, verify=True)
    
    content = json.loads(response.content.decode('utf-8'))
    
    df1 = pd.DataFrame.from_dict(content, orient='index')
    
    df2 = pd.DataFrame.from_dict(df1[0]['properties'],orient='index').transpose()
    
    final_soil = pd.DataFrame({'depth': ['0-5-cm', '5-15cm', '15-30cm', '30-60cm', '60-100cm', '100-200cm']})
    
    for i in range(0, len(df2)):
        one_col = pd.DataFrame({df2.layers[i]['name']: [df2.layers[i]['depths'][0]['values']['mean'],
                                                        df2.layers[i]['depths'][1]['values']['mean'],
                                                        df2.layers[i]['depths'][2]['values']['mean'],
                                                        df2.layers[i]['depths'][3]['values']['mean'],
                                                        df2.layers[i]['depths'][4]['values']['mean'],
                                                        df2.layers[i]['depths'][5]['values']['mean']]})
    
        final_soil = pd.concat([final_soil, one_col], axis=1)
    
    final_soil.columns = ['depth', 'bulk_density', 'cec', 'clay', 'ph', 'sand', 'silt']

    # convert data to 'normal' units
    final_soil['bulk_density'] = final_soil['bulk_density'] * 0.01
    final_soil['cec'] = final_soil['cec'] * 0.1
    final_soil['clay'] = final_soil['clay'] * 0.1
    final_soil['ph'] = final_soil['ph'] * 0.1
    final_soil['sand'] = final_soil['sand'] * 0.1
    final_soil['silt'] = final_soil['silt'] * 0.1

    # add the data id, lat, and long to the data
    final_soil['id'] = id
    final_soil['latitude'] = latitude
    final_soil['longitude'] = longitude

    # only keep the top 5 soil layers 0 - 100cm. This is mainly the root zone.
    final_soil = final_soil.groupby(['id', 'latitude', 'longitude']).head(5)
    final_soil.drop('depth', axis=1, inplace=True)
    
    # take the average of the top 5 soil layers 0 - 100cm
    final_soil = final_soil.groupby(['id', 'latitude','longitude']).mean().reset_index()

    sand = final_soil['sand'][0]
    clay = final_soil['clay'][0]
    
    final_soil['soil_texture'] = classify_soil_texture(sand, clay)

    return final_soil
