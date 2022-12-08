#                   ---GRAPH script---

import plotly.graph_objects as go

class Graph(object):
    # init method, where is generated figure and set background
    def __init__(self):
        self.fig = go.Figure()
        self.fig.update_layout(template="plotly_white",)
    
    # method which plot original defined function, it might be
    # aproximated or original function
    def plot_function(self, x1, x2 , z, func):
        if func == "approximated function":
            colorscale = "Viridis"
        else:
            colorscale = "Bluered"

        self.fig.add_trace(
            go.Surface(
                x = x1,
                y = x2,
                z = z,
                name = func,
                colorscale = colorscale,
                showlegend = True,
                showscale = False,
                contours_z = dict(
                    highlightcolor="limegreen", 
                    project_z=True
                )
            )
        )

    # method which plot finded min. extreme on approximated
    # graph
    def add_minim(self, x1, x2, z, lab):
        self.fig.add_trace(
            go.Scatter3d(
                x = x1, 
                y = x2, 
                z = z,
                name = lab,
                showlegend=True
            )
        )