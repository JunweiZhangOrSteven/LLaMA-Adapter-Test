import plotly.express as px
import pandas as pd

# Load the DataFrame from the CSV file
extracted_info = pd.read_csv('extracted_info')

# Split 'latitude_longitude' into two columns 'latitude' and 'longitude'
location_info = extracted_info['latitude_longitude'].str.strip('[]').str.split(',', expand=True).astype(float)
print(location_info)
location_info.columns = ['latitude', 'longitude']

# Create a scatter plot of latitude and longitude
fig = px.scatter_geo(location_info,
                     lat='latitude',
                     lon='longitude',
                     title='Coordinate Distribution')
fig.show();