# SSEnviro

Single Service Enviromental data (SSEnviro) is a one stop shop for all your soil and weather environmental data. The goal of this package is to have one place to access environmental data. The package utilizes the ISRIC soil grids for soil data, and meteostats for weather data.

## Installation

```bash
get package from GitHub
git clone https://github.com/jknitey/SSEnviro.git

navigate to package
cd SSEnviro

run pip to install package
pip install -e .
```

## Dependencies

meteostat
pandas
json
requests
datetime

## Available data

| Variable |   Name   |   Unit   |
| -------- | -------- | -------- |
| bulk_density | bulk density   | kg/m3   |
| cec   | cation-exchange capacity   | --------   |
| clay | -------- | percent |
| ph | -------- | -------- |
| sand | -------- | percent |
| silt | -------- | percent |
| soil_texture | soil texture | USDA soil textural class |
| temp | air temp. | C |
| dwpt | dew point | C |
| rhum | relative humidity | percent |
| snow | snow depth | mm |
| wdir | average wind direction | degrees |
| wspd | average wind speed | km/h |
| wpgt | peak wind gust | km/h |
| pres | average sea level air pressure | hPa |
| coco | weather condition code | -------- |
| tavg | average air temp. | C |
| tmin | min air temp. | C |
| tmax | max air temp. | C |
| prcp | precipitation | mm |
| tsun | sunshine total | minutes |

## Usage

Data pulls return a pandas dataframe.

```python
# soil data pull
from SSEnviro import get_soil_data


test = 'test1'
latitude = 43.61
longitude = -111.09

get_soil_data(id=test, latitude=latitude, longitude=longitude)

# weather data pull
from SSEnviro import get_weather_data
from datetime import datetime


latitude = 43.61
longitude = -111.09
start = datetime(2023, 1, 1)
end = datetime(2023, 1, 15)

get_weather_data(id='test1', type='daily', latitude=latitude, longitude=longitude, start_date=start, end_date=end)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
