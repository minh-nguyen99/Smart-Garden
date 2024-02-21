import pandas as pd
import MQTT_Gateway

feed_data = pd.read_json('https://io.adafruit.com/api/v2/YncognitoMei/feeds/aio_Bifl808YcND5NZnZKC3ZSLTPEC6N/data')
feed_data['humid-sensor'] =  pd.to_datetime(feed_data['humid-sensor'], infer_datetime_format=True)
feed_data = feed_data.set_index('humid-sensor')

values = pd.Series(feed_data['value'])
values.plot()

daily = values.resample('1d').mean()
daily.plot(kind='barh')