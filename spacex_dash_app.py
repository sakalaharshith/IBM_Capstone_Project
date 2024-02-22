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
launch_sites=spacex_df['Launch Site'].unique()
print(spacex_df.columns)

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(options=[{'label': 'All Sites', 'value': 'All Sites'},
                    {'label': launch_sites[0], 'value': launch_sites[0]},{'label': launch_sites[1], 'value': launch_sites[1]},{'label': launch_sites[2], 'value': launch_sites[2]},{'label': launch_sites[3], 'value': launch_sites[3]}],value='All Sites',id='site-dropdown'),

                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=min_payload,max=max_payload,step=1000, value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

@app.callback(Output(component_id='success-pie-chart',component_property='figure'), Input(component_id='site-dropdown',component_property='value'))
def get_pie_chart(entered_site):
    
    if entered_site=='All Sites':
        local_df=spacex_df
        fig=px.pie(local_df,values='class',names='Launch Site',title='Launch Success for all sites')
        return fig
    else:
        
        local_df=spacex_df.loc[spacex_df['Launch Site']==entered_site]
        print(local_df['class'].value_counts())
        fig=px.pie(local_df,names='class',title='Launch Success for {launch}'.format(launch=entered_site))
        return fig
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart',component_property='figure'),[Input(component_id='site-dropdown',component_property='value'),Input(component_id='payload-slider',component_property='value')])
def get_scatter_plot(dropdown_value,slider_value):
    if dropdown_value=='All Sites':
        print(slider_value[0])
        local_df=spacex_df.loc[(spacex_df['Payload Mass (kg)']>=slider_value[0]) & (spacex_df['Payload Mass (kg)']<=slider_value[1])]
        fig=px.scatter(local_df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig
    else:
        print(dropdown_value)
        local_df=spacex_df.loc[(spacex_df['Payload Mass (kg)']>=slider_value[0]) & (spacex_df['Payload Mass (kg)']<=slider_value[1]) & (spacex_df['Launch Site']==dropdown_value)]
        fig=px.scatter(local_df,x='Payload Mass (kg)',y='class',color='Booster Version Category')
        return fig
    




# Run the app
if __name__ == '__main__':
    app.run_server()
