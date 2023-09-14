import colorsys
import copy
import numpy as np
import re
import plotly.graph_objects as go

def generate_distinct_colors(n):
    color_list = [
        "rgb(220,0,0)",         # Toned down Red
        "rgb(0,220,0)",         # Green            
        "rgb(255,255,0)",       # Yellow
        "rgb(255,0,255)",       # Magenta
        "rgb(0,255,255)",       # Cyan
        "rgb(255,165,0)",       # Orange
        "rgb(127,255,212)",     # Aquamarine
        "rgb(218,112,214)",     # Orchid
        "rgb(255,99,71)",       # Tomato
        "rgb(240,230,140)",     # Khaki
        "rgb(152,251,152)",     # PaleGreen
        "rgb(255,192,203)",     # Pink
      "rgb(0,0,180)",         # Further toned down Blue
        "rgb(72,209,204)"       # MediumTurquoise
    ]
    
    if n <= len(color_list):
        return color_list[:n]
    else:
        print(f"Requested {n} colors, but I only have a list of {len(color_list)} distinct colors. You might want to expand the list or use another method.")
        return color_list

def zoom_in(fig, *vectors):
    fig_zoom = copy.deepcopy(fig)

    all_x = np.concatenate([v[:, 0] for v in vectors])
    all_y = np.concatenate([v[:, 1] for v in vectors])

    x_min, x_max = all_x.min(), all_x.max()
    y_min, y_max = all_y.min(), all_y.max()

    x_margin = (x_max - x_min) 
    y_margin = (y_max - y_min) 

    fig_zoom.update_layout(
        xaxis=dict(range=[x_min - x_margin, x_max + x_margin]),
        yaxis=dict(range=[y_min - y_margin, y_max + y_margin])
    )
    
    return fig_zoom

def create_plot():
  new_fig = go.Figure()
  new_fig.update_layout(template="plotly_white", margin=dict(t=50, b=50, l=50, r=50))
  return new_fig

def plot_points(fig, points, color, label=None, symbol="circle", size=4, showlegend=True):
  fig.add_trace(go.Scatter(x=points[:, 0], y=points[:, 1], mode='markers', 
                           marker=dict(size=size, color=color, symbol=symbol), name=label, 
                           showlegend=showlegend))
  return fig