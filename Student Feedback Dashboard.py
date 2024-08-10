# Import necessary libraries
import pandas as pd
from dash import Dash, html, dcc
import plotly.graph_objs as go

# Path to your CSV file (update this to your file's actual path)
file_path = '/Users/mihirshekhar/Documents/feedback_table.csv'

# Read the CSV file into a DataFrame
feedback_df = pd.read_csv(file_path)

# Aggregate feedback counts
feedback_summary = feedback_df['feedback'].value_counts()

# Creating Plotly visualizations
# Bar Chart for Feedback Counts
feedback_bar = go.Figure(data=[
    go.Bar(
        x=feedback_summary.index,
        y=feedback_summary.values,
        marker=dict(color=['green', 'yellow', 'red'])
    )
])
feedback_bar.update_layout(title='Feedback Counts', xaxis_title='Feedback Type', yaxis_title='Count')

# Pie Chart for Feedback Proportions
feedback_pie = go.Figure(data=[
    go.Pie(
        labels=feedback_summary.index,
        values=feedback_summary.values,
        marker=dict(colors=['green', 'yellow', 'red']),
        hole=.3  # Creating a donut chart
    )
])
feedback_pie.update_layout(title='Feedback Proportions')

# Initialize the Dash app
app = Dash(__name__)

# Define the app layout
app.layout = html.Div(children=[
    html.H1(children='Student Feedback Dashboard', style={'textAlign': 'center'}),
    
    html.Div(children=[
        dcc.Graph(
            id='feedback-bar-chart',
            figure=feedback_bar
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
    
    html.Div(children=[
        dcc.Graph(
            id='feedback-pie-chart',
            figure=feedback_pie
        ),
    ], style={'width': '48%', 'display': 'inline-block'}),
])

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
