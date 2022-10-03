# Dashboard

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
import numpy as np

df = px.data.gapminder().query("country=='Brazil' | country =='Mexico' | country == 'Chile' | country == 'Canada' | country == 'United States'")

# Charts

# Bar chart

def barchart(df):
  colors = [px.colors.sequential.Blues_r[0],] * 3
  colors.insert(0,'silver')
  colors.insert(0,'silver')

  fig_bar = px.bar(df[df['year'] == 2007].sort_values('gdpPercap', ascending = False), x = 'country', y = 'gdpPercap', 
              #color_discrete_sequence = colors,
              title = 'GDP Per Capita in 2007',
              opacity= 0.8,
              labels = {"gdpPercap": "GDP Per Capita (USD)", "country": "Country"}
              )
  fig_bar.update_layout(title_x=0.5, font=dict(size=13))
  fig_bar.update_traces(marker_color=colors, #marker_line_color='rgb(0,0,0)',
                    marker_line_width=1.5, )
  fig_bar.add_annotation(x=3, y=18000,
              text='Latin America is still <br> far behind the first world <br> in terms of GDP Per Capita.',
              showarrow=False,
              yshift=0,
              font=dict(
          #family="serif",
          size=12,
          color="Black"
      ))
  
  return fig_bar

# Scatter plot

def scatter(df):
  fig_scatter = px.scatter(df, x = 'gdpPercap', y = 'lifeExp', 
              color = 'country',
              #color_discrete_sequence = px.colors.sequential.Blues_r,
              title = 'Life Expectancy vs. GDP Per Capita',
              opacity= 0.8,
              labels = {"gdpPercap": "GDP Per Capita (USD)", "lifeExp": "Life Expectancy", "country": "Country"}
              )
  fig_scatter.update_layout(title_x=0.5, font=dict(size=13))
  fig_scatter.add_annotation(x=10000, y=82,
              text='The relationship between Life Expectancy <br> and GDP Per Capita is stronger <br> for the Latin American countries.',
              showarrow=False,
              yshift=0,
              font=dict(
          #family="serif",
          size=12,
          color="Black"
      ))
  
  return fig_scatter

# Line chart

def linechart(df):
  fig_line = px.line(df, x = 'year', y = 'gdpPercap',
              color = 'country',
              #color_discrete_sequence = px.colors.sequential.Blues_r,
              title = 'GDP Per Capita Over Time',             
              labels = {"gdpPercap": "GDP Per Capita (USD)", "year": "Year", "country": "Country"}
              )
  fig_line.update_layout(title_x=0.5, font=dict(size=13))
  fig_line.add_annotation(x=1994, y=19000,
              text='Economic growth in Latin America has been <br> very slow over time. In 2007, no country in the region <br>had even surpassed the US GDP Per Capita of 1952,\
              <br>and the gap is growing bigger.',
              showarrow=False,
              yshift=0,
              font=dict(
          #family="serif",
          size=12,
          color="Black"
      ))
  
  return fig_line


# Layout

app = dash.Dash(
                  __name__, 
                 # server_url=server_url,
                  
                  )


app.layout = html.Div(children=[
                      html.Div([
                      html.H1(
                          children='Economic Lag in Latin America',
                          style={
                              'textAlign': 'center',
                              'color': 'white',
                              'fontFamily': 'Helvetica'
                          })
                      ], style={'margin-top': '0',
                                'width': '100%', 
                                'height': '40px', 
                                'background-color': 'navy', 
                                'float': 'center', 
                                'margin': '0'}),
                      #html.Br(),

                      html.P(children='By Daniel Eduardo López', style={
                          'textAlign': 'center',
                          'color': 'navy',
                          'fontFamily': 'Tahoma',
                          'fontSize': 15
                          }),
                      
                      dcc.Link(html.A('GitHub'), href="https://github.com/DanielEduardoLopez",
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 12, 'font-family': 'Tahoma',
                                               'margin': 'auto',
                                               'display': 'block'}),
                      #html.Br(),
                      dcc.Link(html.A('LinkedIn'), href="https://www.linkedin.com/in/daniel-eduardo-lopez",
                                        style={'textAlign': 'center', 'color': 'navy',
                                               'font-size': 12, 'font-family': 'Tahoma',
                                               'margin': 'auto',
                                               'display': 'block'}),
                      
                      #html.Br(),

                      html.P(children='Economic growth in Latin American has been consistently low over the years,\
                           \ncreating a widening gap between the countries in the region and the advanced economies.', style={
                          'textAlign': 'center',
                          'color': 'black',
                          'fontFamily': 'Helvetica',
                          'fontSize': '15'
                          }),

                      html.Div(children=[
                              html.Label('Select countries:'),
                              html.Br(),
                              dcc.Checklist(['Canada', 'United States', 'Chile', 'Mexico', 'Brazil'],
                                            ['Canada', 'United States', 'Chile', 'Mexico', 'Brazil'],
                                            id='selector'
                                            ),
                      ], style={
                          'textAlign': 'center',
                          'color': 'dimgray',
                          'fontFamily': 'Helvetica',
                          'fontSize': '15',
                          'background-color': '#92CCFF'
                          }),

                      html.Div([
                          html.Div([
                            dcc.Graph(
                              id='barchart',
                              #figure=barchart(df)
                            )], 
                             style={'margin-top': '20px',
                                        'margin-left': '10px',
                                        'width': '48.5%', 
                                        'height': '30%', 
                                        'float': 'center', 
                                       }
                            ),

                          html.Div([
                            dcc.Graph(
                              id='scatterplot',
                              #figure=scatter(df)
                            )], 
                            style={'margin-top': '-450px',
                                        'margin-left': '50%',
                                        'margin-right': '10px',
                                        'width': '48.5%', 
                                        'height': '30%', 
                                        'float': 'center', 
                                       }
                            ),

                      ],
                      style={
                            'width': '100%', 
                             }
                       ),

                      html.Div([
                          dcc.Graph(
                          id='linechart',
                          #figure=linechart(df)
                          ),
                      ],
                      style={'margin-top': '20px',
                             'margin-left': '10px',
                             'margin-right': '10px',
                             'margin-bottom': '10px',
                             'width': '98%', 
                             'height': '450px', 
                             'float': 'center', 
                            }
                      ),


                    ], style={'width': '100%', 
                              'overflow': 'hidden',
                              'background-color': 'aliceblue', 
                              })         
                            
@app.callback(
    [Output(component_id="barchart", component_property="figure"), 
    Output(component_id="scatterplot", component_property="figure"), 
    Output(component_id="linechart", component_property="figure")], 
    [Input(component_id="selector", component_property="value")]
    )
def update_charts(selector):
    dff = df.copy()
    dff = dff[dff['country'].isin(selector)]
    
    fig_bar = barchart(dff)
    fig_scatter = scatter(dff)
    fig_line = linechart(dff)
    
    return fig_bar, fig_scatter, fig_line

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)