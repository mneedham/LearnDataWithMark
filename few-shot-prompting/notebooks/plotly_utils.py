import plotly.graph_objs as go


def render_confusion_matrix(matrix):
  # create the heatmap
  heatmap = go.Heatmap(z=matrix, x=['Negative', 'Positive'], y=['Negative', 'Positive'], colorscale='Greens')
  
  # create the figure
  fig = go.Figure(data=[heatmap])
  
  # add custom xaxis title
  fig.add_annotation(dict(font=dict(color="black",size=18),
                          x=0.5,
                          y=-0.15,
                          showarrow=False,
                          text="LLM Prediction",
                          xref="paper",
                          yref="paper"))
  
  # add custom yaxis title
  fig.add_annotation(dict(font=dict(color="black", size=18),
                          x=-0.13,  # Adjusted x position                          
                          y=0.5,  # Adjusted y position
                          showarrow=False,
                          text="Data (Truth)",
                          textangle=-90,
                          xref="paper",
                          yref="paper"))
  
  # Add annotations for each value in the matrix
  labels = ['TN', 'FP', 'FN', 'TP']
  label_index = 0
  for i, row in enumerate(matrix):
      for j, value in enumerate(row):
          # Add numerical value
          fig.add_annotation(dict(font=dict(color="black", size=30),
                                  x=j,
                                  y=i,
                                  showarrow=False,
                                  text=f"{value}",
                                  xref="x",
                                  yref="y",
                                  yanchor="bottom"))
          
          # Add label
          fig.add_annotation(dict(font=dict(color="black", size=25),
                                  x=j,
                                  y=i,
                                  showarrow=False,
                                  text=f"{labels[label_index]}",
                                  xref="x",
                                  yref="y",
                                  yanchor="top"))
          label_index += 1
  
  fig.update_layout(margin=dict(t=20, l=150, b=70))
  return fig
  