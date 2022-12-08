#                   ---GRAPH script---

import plotly.graph_objects as go

class Graph(object):
    # init method which generate figure and set colours
    def __init__(self):
        self.fig = go.Figure()
        self.set_color = "generated"
        self.fig.update_layout(template="plotly_white",)
    
    # method which plot defined elipse by equation
    # for this operatin was choosed countour graph 
    def set_equation(self, x1, x2 , z):
        self.fig.add_trace(
            go.Contour(
                x = x1,
                y = x2,
                z = z,
                contours_coloring='fill',
                line_width=4,
                line=dict(color='black'),
                name='elipse',
                contours=dict(
                    type = 'constraint'
                ),
                hoverinfo='none'
            )
        )

    # method which plot aproximate bounderies and areas from 
    # classificator
    def aprox_equation(self, x1, x2 , z):
        colorscale = [[0, 'lime'], [1, 'lightcoral']]
        self.fig.add_trace(
            go.Contour(
                x = x1,
                y = x2,
                z = z,
                contours_coloring='fill',
                colorscale=colorscale,
                line_width=4,
                line=dict(
                    color='black'
                ),
                # this is becouse plotly.countour dont support
                # countour levels as pyplot
                contours=dict(
                    start=0.8,
                    end=1.1,
                    size=1,
                ),
                hoverinfo='none',
                showscale=False
            )
        )

    # method which show classifed generated points
    # in init or after training 
    def gen_points(self,p,clas):
        if self.set_color == "generated":
            if clas == 'inside':
                color = 'darkgreen'
            else:
                color = 'darkred'
        
        else:
            if clas == 'inside':
                color = 'darkblue'
            else:
                color = 'orange'

        self.fig.add_trace(
            go.Scatter(
                x=p[:,0], 
                y=p[:,1],
                mode='markers',
                name=clas,
                marker=dict(
                    color=color
                )
            )
        )