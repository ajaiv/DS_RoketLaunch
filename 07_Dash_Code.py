import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the spacex dataset into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")

# Find the minimum and maximum payload values from the dataframe
min_payload = spacex_df['Payload Mass (kg)'].min()
max_payload = spacex_df['Payload Mass (kg)'].max()

# Get the unique launch sites from the dataset
launch_sites = spacex_df['Launch Site'].unique()

# Create a dash application
app = dash.Dash(__name__)

# Create the layout for the app
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard', style={'textAlign': 'center', 'color': '#503D36', 'font-size': 40}),
    
    # Task 1: Launch Site Dropdown
    html.Br(),
    dcc.Dropdown(
        id='site-dropdown',
        options=[{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in launch_sites],
        value='ALL',
        placeholder="Select a Launch Site here",
        searchable=True
    ),
    html.Br(),
    
    # Task 2: Pie Chart for Success/Failure
    html.Div(dcc.Graph(id='success-pie-chart')),
    html.Br(),
    
    # Task 3: Payload Range Slider
    html.P("Payload range (Kg):"),
    dcc.RangeSlider(
        id='payload-slider',
        min=0,
        max=10000,
        step=1000,
        marks={i: str(i) for i in range(0, 10001, 1000)},
        value=[min_payload, max_payload]
    ),
    html.Br(),
    
    # Task 4: Scatter Chart for Payload vs. Launch Success
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])


# Task 2: Callback for Success/Failure Pie Chart
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def get_pie_chart(entered_site):
    if entered_site == 'ALL':
        # If 'ALL' sites are selected, show overall success/failure
        fig = px.pie(spacex_df, names='class', 
                     title='Total Success/Failure for All Sites', 
                     labels={'class': 'Launch Success/Failure', '0': 'Failure', '1': 'Success'})
    else:
        # If a specific site is selected, filter by site and show success/failure
        filtered_df = spacex_df[spacex_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, names='class', 
                     title=f'Success/Failure for {entered_site}', 
                     labels={'class': 'Launch Success/Failure', '0': 'Failure', '1': 'Success'})

    return fig


# Task 4: Callback for Payload Range and Scatter Plot
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def get_scatter_chart(entered_site, selected_payload_range):
    min_payload, max_payload = selected_payload_range
    
    # Filter data based on the selected site and payload range
    if entered_site == 'ALL':
        filtered_df = spacex_df[
            (spacex_df['Payload Mass (kg)'] >= min_payload) & 
            (spacex_df['Payload Mass (kg)'] <= max_payload)
        ]
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category', 
            title='Payload Mass vs. Launch Outcome for All Sites',
            labels={'class': 'Launch Outcome (Success=1, Failure=0)', 'Payload Mass (kg)': 'Payload Mass (kg)'}
        )
    else:
        filtered_df = spacex_df[
            (spacex_df['Launch Site'] == entered_site) & 
            (spacex_df['Payload Mass (kg)'] >= min_payload) & 
            (spacex_df['Payload Mass (kg)'] <= max_payload)
        ]
        fig = px.scatter(
            filtered_df, 
            x='Payload Mass (kg)', 
            y='class', 
            color='Booster Version Category', 
            title=f'Payload Mass vs. Launch Outcome for {entered_site}',
            labels={'class': 'Launch Outcome (Success=1, Failure=0)', 'Payload Mass (kg)': 'Payload Mass (kg)'}
        )
    
    return fig


# Run the app
if __name__ == '__main__':
    app.run_server()
