
# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

app = dash.Dash(__name__) 

# Create an app layout
#Task 1, Create dropdown layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Dashboard', 
                                        style={'textAlign':'center', 'color':'#503D36', 'font-size': 40}),
                                dcc.Dropdown(id='site-dropdown',
                                             options=[
                                            {'label': 'All Sites', 'value': 'ALL'},
                                            {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                            {'label': 'VAFB SLC-4E LC-40', 'value': 'CVAFB SLC-4E LC-40'},
                                            {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                            {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                                     ],
                                             value='ALL',
                                             placeholder='Select a Launch Site here',
                                             searchable=True
                                             # style={'width':'80%','padding':'3px','font-size':'20px','text-align-last':'center'}
                                             ),
                                html.Br(),

                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),

                                # Tast 3, Add Range Slider
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0',
                                                    100: '100'},
                                                value=[min_payload, max_payload]
                                                ),

                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# Task 2, add callback function to render pie chart
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Successful Landings for All Sites')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df = spacex_df[spacex_df['Launch Site']== entered_site] 
        filtered_df=filtered_df.groupby(['Launch Site','class']).size().reset_index(name='class count')
        fig = px.pie(filtered_df, values='class count', names= 'class',  title='Total Successful Landings for ' + entered_site)
        return fig

# Task 4, add callback to render scatterplot
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),
                [Input(component_id='site-dropdown',component_property='value'),
                Input(component_id='payload-slider',component_property='value')])
def scatter(entered_site,payload):
    filtered_df = spacex_df[spacex_df['Payload Mass (kg)'].between(payload[0],payload[1])]
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df,
        x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Launch Success Rate For All Sites by Payload Mass')
        return fig
    else:
    # return the outcomes piechart for a selected site
        fig=px.scatter(filtered_df[filtered_df['Launch Site']==entered_site],
        x='Payload Mass (kg)', y='class',
        color='Booster Version Category',    
        title='Launch Success Rate For All Sites by Payload Mass')
        return fig
# Run the app
if __name__ == '__main__':
 app.run_server()
