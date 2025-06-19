import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
import requests
import pandas as pd
from dash.dependencies import Input, Output
import plotly.express as px

# IP address of your FLARE VM
FLARE_VM_IP_ADDRESS = '192.168.56.1'
API_URL = f'http://{FLARE_VM_IP_ADDRESS}:5000/api/data'

# Fetch data from the Flask backend
def fetch_data():
    response = requests.get(API_URL)
    data = response.json()
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("Sentinel: Malware Analyzer Visualization", className='text-center mb-4'), width=12)
    ]),
    dbc.Row([
        dbc.Col(dcc.Graph(id='timeline-graph'), width=12),
        dbc.Col(dcc.Graph(id='activity-bar-chart'), width=12),
        dbc.Col(dcc.Graph(id='activity-pie-chart'), width=12)
    ])
])

@app.callback(
    Output('timeline-graph', 'figure'),
    [Input('timeline-graph', 'id')]
)
def update_timeline_graph(_):
    df = fetch_data()
    print("DataFrame Columns:", df.columns)  # Debug line
    print("DataFrame Sample:", df.head())    # Debug line

    fig = px.scatter(df, x='timestamp', y='activity', color='severity', hover_data=['details', 'process_name', 'network_ip'])
    fig.update_layout(title='Malware Activity Timeline', xaxis_title='Time', yaxis_title='Activity')
    return fig

@app.callback(
    Output('activity-bar-chart', 'figure'),
    [Input('activity-bar-chart', 'id')]
)
def update_bar_chart(_):
    df = fetch_data()
    activity_count = df['activity'].value_counts().reset_index()
    activity_count.columns = ['activity', 'count']
    fig = px.bar(activity_count, x='activity', y='count', title='Activity Count')
    return fig

@app.callback(
    Output('activity-pie-chart', 'figure'),
    [Input('activity-pie-chart', 'id')]
)
def update_pie_chart(_):
    df = fetch_data()
    activity_count = df['activity'].value_counts().reset_index()
    activity_count.columns = ['activity', 'count']
    fig = px.pie(activity_count, names='activity', values='count', title='Activity Distribution')
    return fig

if __name__ == '__main__':
    app.run_server(debug=True, host='127.0.0.1')