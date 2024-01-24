import plotly.graph_objects as go
import pandas as pd

# Load the DataFrame from the CSV file
extracted_info = pd.read_csv('extracted_info')

# Calculate the frequency of each name
name_counts = extracted_info['name'].value_counts()
# Creating the bar chart
fig = go.Figure(data=go.Bar(x=name_counts.index, y=name_counts.values))

# Customizing the layout
fig.update_layout(title='Name Distribution',
                  xaxis_title='Name',
                  yaxis_title='Frequency',
                  xaxis={'categoryorder':'total descending'})  # This orders the bars based on frequency
# Show the plot
fig.show()




