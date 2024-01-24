import pandas as pd
import json

# Load the CSV files into dataframes
categories_df = pd.read_csv('categories.csv')
metadata_df = pd.read_csv('metadata.csv')

# Extract the required columns using iloc
extracted_info = metadata_df[['split','category_id', 'image_id', 'datetime','location']].copy()
# Mapping name to extracted_info using category_id
extracted_info['name'] = extracted_info['category_id'].map(categories_df.set_index('category_id')['name'])
# Removing rows where 'name' is NaN
extracted_info = extracted_info[~(extracted_info['name'].isna())]

# Read the JSON file
with open('gps_locations.json') as file:
    gps_data = json.load(file)

# Convert JSON data to DataFrame and rename its columns
gps_df = pd.DataFrame.from_dict(gps_data, orient='index').reset_index()
gps_df.columns = ['location', 'latitude', 'longitude']
print(gps_df)

# Convert location to the same data type as in metadata_df for consistent mapping
gps_df['location'] = gps_df['location'].astype(metadata_df['location'].dtype)

# Mapping latitude and longitude to extracted_info using location
# Simultaneously map latitude and longitude
extracted_info = extracted_info.assign(
    latitude_longitude=lambda df: df['location'].
    map(lambda loc: f"[{gps_df.at[loc, 'latitude']}, {gps_df.at[loc, 'longitude']}]"
        if loc in gps_df.index else "no_axis")
)
# extracted_info = extracted_info.assign(
#     latitude=lambda df: df['location'].map(gps_df['latitude']),
#     longitude=lambda df: df['location'].map(gps_df['longitude'])
# )

# Filter out rows where either latitude or longitude are NaN or 'no_axis'
extracted_info = extracted_info[~((extracted_info['latitude_longitude'].isna() | (extracted_info['latitude_longitude'] == 'no_axis')))]

extracted_info.to_csv('extracted_info',index=True)

# Iterate over each unique value in the 'split' column
# for value in extracted_info['split'].unique():
#     # Create a new DataFrame for each unique value
#     subset_df = extracted_info[extracted_info['split'] == value]
#
#     # Define a file name based on the unique value
#     file_name = f'extracted_info_{value}.csv'
#
#     # Save each subset DataFrame to a separate CSV file
#     subset_df.to_csv(file_name, index=False)
