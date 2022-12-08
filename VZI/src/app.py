import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.graph_objects as go

import json
from dijkstra import Dijkstra

class Run_App(object):
    def __init__(self) -> None:
        self.pom = list()

    # private method:
    #   input: 
    #   return distances
    # Notes: reading data stored in external database files describing the chart structure ​
    # determination of visited nodes
    def __load_city_data(self) -> list:
        with open('data/flights_data.json', 'r') as outfile:
            distances = json.load(outfile)
        return distances
    
    # private method:
    #   input: path nodes
    #   return city
    # Notes: eading of data about individual cities, used for plotting
    def __load_city_name(self) -> dict:
        with open('data/airports_location.json', 'r') as outfile:
            locations = json.load(outfile)
        city = list()
        for i in locations:   
            city.append(i)
        return city
    
    # private method:
    #   input: airports nodes
    #   return latitude, longitude
    # Notes: reading of data about individual cities, used for plotting
    # when the requested city is found, its coordinates are returned​
    def __load_city_location(self, airports: list) -> list:
        with open('data/airports_location.json', 'r') as outfile:
            locations = json.load(outfile)
            
        latitude,longitude = list(), list()

        for k in airports:
            for i in locations.keys():
                if i == k:
                    latitude.append(locations[i]['lat'])
                    longitude.append(locations[i]['lon'])
                    break

        return latitude, longitude
    
    # private method:
    #   input:
    #   return figure
    # Notes: initialization graph, plot all known nodes
    def show(self) -> None:
        city_ = self.__load_city_name()
        lat_, lon_ = self.__load_city_location(city_)
        self.fig = go.Figure()
        self.fig.add_trace(
            go.Scattergeo(
                lat = lat_[:],
                lon = lon_[:],
                name="City-Airport",
                text = city_[:],
                mode = 'markers',
                marker = dict(
                    size = 12,
                    color = 'darkred'
                ),
            ),        
        )
        self.fig.update_layout(
            autosize = True,
            showlegend = True,
            geo = dict(
                showland = True,
                showlakes = True,
                showcountries = True,
                showocean = True,
                showrivers=True, 
                rivercolor = 'rgb(0, 92, 149)',
                oceancolor = 'rgb(0, 159, 228)',          
                landcolor = 'rgb(196, 206, 86)',
                showsubunits = True,
                countrycolor = 'rgb(0, 0, 0)',
                resolution = 110,
                lakecolor = 'rgb(0, 92, 149)',
                projection_type = 'orthographic',
                coastlinewidth = 2,
            )
        )
    
    # public method:
    #   input: path nodes
    #   return 
    # Notes: show / init graph path
    def show_path(self, path: list) -> None:
        # setting coordinates for plotting​
        lat_, lon_ = self.__load_city_location(path)
        self.fig.add_trace(
            go.Scattergeo(
                lat = lat_[:],
                lon = lon_[:],
                text = path,
                name = "Path",
                mode = 'lines+markers',
                marker = dict(
                    size = 12,
                    color = 'black'
                ),
                line = dict(
                    width = 5,
                    color = 'black'
                ),
            ),
        )
    
    # public method:
    #   input: path nodes
    #   return 
    # Notes: show start node
    def show_s_node(self, pom: list) -> None:
        airport = [pom[0]]
        lat_, lon_ = self.__load_city_location(airport)
        self.fig.add_trace(
            go.Scattergeo(
                lat = lat_,
                lon = lon_,
                text = pom[0],
                name = pom[0],
                mode = 'markers',
                marker = dict(
                    size = 12,
                    color = 'green'
                ),
            )
        )

    # public method:
    #   input: path nodes
    #   return 
    # Notes: show end node
    def show_e_node(self, pom: list) -> None:
        airport = [pom[-1]]
        lat_, lon_ = self.__load_city_location(airport)
        self.fig.add_trace(
            go.Scattergeo(
                lat = lat_,
                lon = lon_,
                text = pom[-1],
                name = pom[-1],
                mode = 'markers',
                marker = dict(
                    size = 12,
                    color = 'orange'
                ),
            )
        )

    # public method:
    #   input:
    #   return
    # Note: Show whole app.
    def show_app(self) -> None:
        pom = self.pom

        # call a function to display the initialization graph​
        self.show()
        dash_app = dash.Dash(__name__)
        dash_app.layout = html.Div(
            children = [
                dcc.Graph(
                    id = 'geo-world',
                    figure = self.fig,
                    config = dict(
                        fillFrame = True
                    )
                )
            ]
        )

        @dash_app.callback(
            Output('geo-world', 'figure'),
            Input('geo-world', 'clickData')
        )
        def display_click_data(clickData):
            if clickData != None:
                try:
                    pom.append(clickData['points'][0]['text'])
                except:
                    pass

                if len(pom) == 1:
                    self.show()
                    self.show_s_node(pom)
                    return self.fig

                # if 2 points are checked then calculate the Dijkstra algorithm and display the result
                elif len(pom) == 2:  
                    dijktra = Dijkstra(pom[0], pom[1], self.__load_city_data())
                    self.show()
                    self.show_path(dijktra.path)
                    self.show_s_node(pom)
                    self.show_e_node(pom)
                    return self.fig

                # if point 3 is checked, reset the variable field and return the initialization geographic
                elif len(pom) > 2:
                    self.show()
                    for i in range(3):
                        del pom[0]

                    return self.fig

            else:
                return self.fig

        # Python Flask run server 
        return dash_app


if __name__ == "__main__":
    dash_app = Run_App().show_app()
    dash_app.run_server(debug=False)