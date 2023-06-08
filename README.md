# SSEnviro

SSEnviro is a one stop shop for all your wanted soil and weather environmental data. The package utalizes the ISRIC soil grids for soil data, and meteostats 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install SSEnviro.

```bash
pip install SSEnviro
```

## Usage

```python
from ISRIC_soil_functions import get_soil_data


latitude = 43.61
longitude = -111.09

get_soil_data(id='test1', latitude=latitude, longitude=longitude)

from meteostat_weather_functions import get_weather_data
from datetime import datetime

latitude = 43.61
longitude = -111.09
start = datetime(2023, 1, 1)
end = datetime(2023, 1, 15)

get_weather_data(id='test', type='daily', latitude=latitude, longitude=longitude, start_date=start, end_date=end)
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)