#!/usr/bin/env python

import plotly.graph_objects as go
import numpy as np

# main classmethod, which show graph in default web broswer
# inputs: way points
class Graph(object):
    @classmethod
    def show(self, x, y, z, title):
        fig = go.Figure()
        fig.add_trace(go.Scatter3d(
            x=x,
            y=y,
            z=z,
            marker_color='darkred',
            name="way points"
        ))

        fig.add_trace(go.Scatter3d(
            x=np.array(x[0]),
            y=np.array(y[0]),
            z=np.array(z[0]),
            marker_color='darkgreen',
            name="goal"
        ))

        fig.add_trace(go.Scatter3d(
            x=np.array(x[-1]),
            y=np.array(y[-1]),
            z=np.array(z[-1]),
            marker_color='darkblue',
            name="start"
        ))

        # defined scenes in gtaph to workaspace of UR3 cobot
        fig.update_layout(
            scene_aspectmode='cube',
            scene = dict(
                xaxis = dict(nticks=4, range=[-0.5,0.5]),
                yaxis = dict(nticks=4, range=[-0.5,0.5]),
                zaxis = dict(nticks=4, range=[0,0.6]),
            ),

            showlegend=False,
            autosize=True,
        )

        fig.update_layout(template="plotly_white",title=title)
        fig.show()
