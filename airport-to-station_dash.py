import dash
import dash_core_components as dcc
import dash_html_components as html
import folium
import pandas as pd
from dash.dependencies import Input, Output
from folium import plugins

app = dash.Dash()
distances = pd.read_pickle('data_noaa/distances.pkl')
df_stations = pd.read_pickle('data_noaa/df_stations.pkl')
airports = pd.read_pickle('data_noaa/airports.pkl')

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Styling using html components', style={'textAlign': 'center',
                                                                      'marginTop': 40, 'marginBottom': 40}),

    dcc.Input(id='textinput',
              placeholder='Enter 3-letter IATA code',
              type='text',
              value='ORD'
              ),
        dcc.Graph(id = 'foliummap')
    ])


@app.callback(Output(component_id='foliummap', component_property='graph'),
              [Input(component_id='textinput', component_property='value')])

def draw_top5_map(input_iata):
  top5stations = distances[[input_iata]]\
    .sort_values(by = input_iata)\
    .head(5)\
    .reset_index()\
    .merge(df_stations,
          left_on='index',
          right_on = 'id',
          how = 'left')\
    .rename(columns={input_iata:'distance'})

  input_lat = float(airports[airports.iata == input_iata].lat)
  input_lon = float(airports[airports.iata == input_iata].lon)

  # Init folium map
  m5 = folium.Map(location=[input_lat,input_lon], 
                  zoom_start=10, 
                  control_scale=True,
                  tiles="Stamen Terrain")

  # Add root marker for airport
  folium.Marker(
      [input_lat,input_lon],
      popup = input_iata,
      icon = folium.Icon(color='blue',
                        icon='plane',
                        prefix='fa')
  ).add_to(m5)

  # Add NOAA station markers
  for i in range(0,len(top5stations)):
    folium.Marker(
        [top5stations.iloc[i]['lat'],top5stations.iloc[i]['lon']],
        popup=top5stations.iloc[i]['id'] + "\n" + top5stations.iloc[i]['name'] + "\n" + str(
            top5stations.iloc[i]['distance']),
        icon=folium.Icon(color='green',
                         icon='cloud',
                         prefix='fa')
    ).add_to(m5)

  # Init + add minimap
  minimap = plugins.MiniMap()
  m5.add_child(minimap)

  return m5


if __name__ == '__main__':
    app.run_server()
