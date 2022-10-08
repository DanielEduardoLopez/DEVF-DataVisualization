### DASHBOARD DE SERVICIOS PROFESIONALES, CIENTÍFICOS y TÉCNICOS EN MÉXICO EN 2022

"""
By Daniel Eduardo López
Date: 2022-10-05
GitHub: https://github.com/DanielEduardoLopez
LinkedIn: https://www.linkedin.com/in/daniel-eduardo-lopez
"""

#!pip install dash

# Run this app with 'python 4-Dashboard.py' and
# visit http://127.0.0.1:8050/ in your web browser.

import numpy as np
import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px

# Data Source
# Categoría de "Servicios profesionales, científicos y técnicos" (2022) del DENUE del INEGI
df = pd.read_csv('https://raw.githubusercontent.com/DanielEduardoLopez/DEVF-DataVisualization/main/denue_inegi_54_.csv', encoding = 'ISO-8859-1') 

# Options for dropdown
options = sorted(list(set(df['nombre_act'].values)))

# Configuration parameters for the Graphs style
gwidth = '30%' # Graphs width
gheight = '30%'  # Graphs height

# Función para convertir los rangos de personas empleadas en números enteros
def cleaner(x):
  r = list()
  if x == '251 y más':
    r.append(251)
  else:
    x = x.split('-')
    for i in x:
      r.append(int(i))
  
  return r

# Data wrangling
df['fecha_alta'] = pd.to_datetime(df['fecha_alta'], errors = 'coerce', yearfirst=True, infer_datetime_format = True)
df['per_ocu'] = df['per_ocu'].map(lambda x: x.replace(' a ', '-').replace(' personas', ''))
df['per_ocu_int'] = df['per_ocu'].apply(lambda x: np.mean(cleaner(x)))


# Charts

# Bar chart

def barchart(df):

  df_act = df.groupby(by = 'nombre_act', as_index = False).agg(count = ('nombre_act', 'size')).\
          sort_values(by = 'count', ascending = False)
  df_act_top = df_act.head(10)
  df_act_top['nombre_act'] = df_act_top['nombre_act'].map(lambda x: x[:30])
    
  palette = ['silver',]*9
  palette.insert(9, px.colors.sequential.Blues_r[0])

  fig = px.bar(df_act_top.sort_values(by='count'), y = 'nombre_act', x = 'count',              
              title = 'Organizaciones de servicios profesionales y técnicos <br>más comunes en México (2022)',
              opacity= 0.8,
              labels = {"nombre_act": "Actividad profesional y/o técnica", "count": "Número de organizaciones"}
              )
  fig.update_layout(title_x=0.5, font=dict(size=10), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  fig.update_traces(marker_color=palette, marker_line_color='white', marker_line_width=1)
  """
  fig.add_annotation(x=40000, y=7.5,
              text='Los bufetes jurídicos <br>son las organizaciones de <br>servicios profesionales y técnicos <br>más comunes en el país.',
              showarrow=False,
              yshift=0,
              font=dict(
              #family="sans-serif",
              size=10,
              color="Black"
              ))
  """
  return fig

# Treemap
def treemap(df):
  df = df[df['nombre_act'] == act]
  df_org = df.groupby(by = 'raz_social', as_index = False).\
          agg(count = ('raz_social', 'size')).sort_values(by = 'count', ascending = False)
  df_org['raz_social'] = df_org['raz_social'].map(lambda x: x[:30].title().replace('Sa De Cv', 'SA de CV').\
                                                  replace('S De Rl', 'S de RL').replace('Cv', 'CV').replace('Sc', 'SC'))
  df_org_top = df_org.head(15)

  palette = ['silver',]*15
  palette.insert(15, px.colors.sequential.Blues_r[0])

  fig = px.treemap(df_org_top, path = [px.Constant("."), 'raz_social'], values='count', color = 'count', 
                  color_continuous_scale=px.colors.sequential.Blues,
                  title= 'Principales organizaciones en México',
                  )
  fig.update_traces(root_color="aliceblue")
  fig.update_layout(title_x=0.5, 
                    coloraxis_colorbar=dict(title="Número de <br>Establecimientos"), 
                    font=dict(size=11),
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  return fig

# Scatterplot
def scatter(df):
  
  df_org = df.groupby(by = 'raz_social', as_index = False).\
          agg(count = ('raz_social', 'size')).sort_values(by = 'count', ascending = False)
  df_org['raz_social'] = df_org['raz_social'].map(lambda x: x[:30].title().replace('Sa De Cv', 'SA de CV').\
                                                  replace('S De Rl', 'S de RL').replace('Cv', 'CV').replace('Sc', 'SC'))
  df_org_top = df_org.head(15).sort_values(by = 'count', ascending = False)

  palette = ['silver',]*12
  for i in range(0,3):
    palette.insert(0, px.colors.sequential.Blues_r[0])

  fig = px.scatter(df_org_top, y='raz_social', x = 'count', size = 'count', 
                  color = 'raz_social',
                  color_discrete_sequence = palette,
                  #color = 'count',
                  #color_continuous_scale = px.colors.sequential.Blues,
                  title= 'Principales organizaciones en México',
                  labels = {"raz_social": "Organización", "count": "Número de establecimientos en el país"},
                  opacity= 0.8,
                  )
  fig.update_layout(title_x=0.5, 
                    font=dict(size=10), 
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)"
                    )

  for index, value in df_org_top.sort_values(by = 'count', ascending = True)['count'].reset_index().iterrows():
    if index in [12,13,14]:
      fig.add_shape(type='line', y0=index, y1= index, x0=np.min(df_org_top['count']), x1= value[1], xref='x',
                  yref='y', line=dict(color= px.colors.sequential.Blues_r[0]), opacity= 0.7)
    else:
      fig.add_shape(type='line', y0=index, y1= index, x0=np.min(df_org_top['count']), x1= value[1], xref='x',
                  yref='y', line=dict(color= 'silver'), opacity= 0.7)
  """
  top = df_org_top.iloc[0:1]['raz_social'].values[0]
  
  fig.add_annotation(x=value[1], y=10,
              text=f'La organización con más <br> establecimientos en el país es <br> {top}.',
              showarrow=False,
              yshift=0,
              font=dict(
              #family="sans-serif",
              size=10,
              color="Black"
               ))
   """
  return fig

# Donut chart

def donutchart(df, act):
  df_percen = df.groupby(by = 'nombre_act', as_index = False).agg(count = ('nombre_act', 'size')).sort_values(by = 'count', ascending = False)
  df_percen.loc[~(df_percen['nombre_act'] == act), 'nombre_act'] = 'Otros'
  df_percen = df_percen.groupby('nombre_act').agg(total = ('count','sum')).sort_values(by = 'total').reset_index()
  percentage = (df_percen.loc[0,'total'] / df_percen.loc[1,'total']) *100

  colors =  [px.colors.sequential.Blues_r[0], 'silver']

  fig = px.pie(df_percen, values='total', names='nombre_act', color = 'total', hole = 0.7,  
              title='Porcentaje del total de establecimientos')
  fig.update_layout(title_x=0.5, font=dict(size=11), showlegend=False, paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  fig.update_traces(hoverinfo='label+percent+name', textinfo='percent', textfont_size=14,
                      marker=dict(colors=colors, line=dict(color="rgba(0,0,0,0)", width=4)))
  """
  fig.add_annotation(x=1.35, y=0.5,
              text=f'Las organizaciones de <br> {act} <br> representaron el {percentage:.0f}% de las organizaciones <br>oferentes de servicios profesionales y <br>técnicos en México.',
              showarrow=False,
              yshift=0,
              font=dict(
              #family="sans-serif",
              size=10,
              color="Black"
              ))
  """
  return fig

# Choropleth Map
def mapa(df):
  
  df_map = df.\
            groupby(by = 'entidad', as_index = False).agg(count = ('nombre_act','size')).\
            sort_values(by = 'count', ascending = False)
  df_map['percentage'] = (df_map['count'] / np.sum(df_map['count'])) *100
  df_map['entidad'] = df_map['entidad'].map(lambda x: x.title().replace('De','de').strip())

  states_dict = {'Aguascalientes': 'AS', 
              'Baja California': 'BC', 
              'Baja California Sur': 'BS', 
              'Campeche': 'CC',
              'Ciudad de México':'DF',
              'Chiapas': 'CS',
              'Chihuahua':'CH',
              'Coahuila de Zaragoza':'CL',
              'Colima':'CM',
              'Durango':'DG',
              'México':'MC',
              'Guanajuato':'GT',
              'Guerrero':'GR',
              'Hidalgo':'HG',
              'Jalisco':'JC',
              'Michoacán de Ocampo':'MN',
              'Morelos':'MS',
              'Nayarit':'NT',
              'Nuevo León':'NL',
              'Oaxaca':'OC',
              'Puebla':'PL',
              'Querétaro':'QT',
              'Quintana Roo':'QR',
              'San Luis Potosí':'SP',
              'Sinaloa':'SL',
              'Sonora':'SR',
              'Tabasco':'TC',
              'Tamaulipas':'TS',
              'Tlaxcala':'TL',
              'Veracruz de Ignacio de La Llave':'VZ',
              'Yucatán':'YN',
              'Zacatecas':'ZS'}

  states_df = pd.DataFrame.from_dict(states_dict, orient='index').reset_index().\
              rename(columns={"index": "State", 0: "ID"}).set_index('State')

  df_map = df_map.set_index('entidad').join(states_df, how = 'left').fillna(value=0)

  fig = px.choropleth(df_map, 
                              geojson = 'https://raw.githubusercontent.com/isaacarroyov/data_visualization_practice/master/Python/visualizing_mexican_wildfires_tds/data/states_mx.json', 
                              locations='ID', 
                              color='percentage',
                              color_continuous_scale="Blues",
                              scope="north america",
                              title='% total de establecimientos <br> por entidad',
                              labels={'percentage':'% del total'},           
                              )
  fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, title_x=0.5, title_y=0.85, font=dict(size=11), 
                  paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", geo_bgcolor = "rgba(0,0,0,0)")
  fig.update_geos(fitbounds="locations", visible=False)
  fig.update(layout_coloraxis_showscale=False)
 
  """
  fig.add_annotation(x=0.5, y=0.1,
            text=f'La mayor parte de las <br> organizaciones en México se <br> concentran en la capital del país.',
            showarrow=False,
            yshift=0,
            font=dict(
            #family="sans-serif",
            size=10,
            color="Black"
            ))
    """
  return fig

# Histogram
def histogram(df):
  
  df_hist = df

  palette = ['silver',]*100
  palette.insert(0, px.colors.sequential.Blues_r[0])

  fig = px.histogram(df_hist, x = 'per_ocu_int', 
                            labels={
                                    "per_ocu_int": "Número de empleados",
                                    "count": "Frecuencia"
                                    },
                            title='Distribución del número de empleados',
                            )
  fig.update_layout(title_x=0.5, font=dict(size=11), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  fig.update_traces(marker_color=palette)
  fig.update_yaxes(title = "Frecuencia")
  """
  fig.add_annotation(x=70, y=1200,
              text=f'La mayor parte de las <br> organizaciones en México tienen <br> de 1 a 5 empleados en promedio.',
              showarrow=False,
              yshift=0,
              font=dict(
              #family="sans-serif",
              size=10,
              color="Black"
              ))
  """
  return fig

# Area chart
def areachart(df):
  
  df_date = df.groupby(by= 'fecha_alta', as_index = False).\
                agg(sum_ocu = ('per_ocu_int', 'sum'), mean_ocu = ('per_ocu_int', 'mean'), count = ('entidad','count')).\
                sort_values(by = 'fecha_alta')
  fig = px.area(df_date, x="fecha_alta", y="mean_ocu",
                labels={"fecha_alta": "Año",
                        "mean_ocu": "Promedio de empleados"
                        },
                title='Promedio de empleados a lo largo del tiempo',
                )
  fig.update_layout(title_x=0.5, font=dict(size=11), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
  fig.update_traces(line_color=px.colors.sequential.Blues_r[0])
  """
  fig.add_annotation(x='2019-11-01', y=100,
              text=f'Desde el 2017, el número promedio <br>de empleados en organizaciones de <br>servicios prof. y técnicos ha aumentado.',
              showarrow=False,
              yshift=0,
              font=dict(
              #family="sans-serif",
              size=10,
              color="Black"
              ))
  """
  return fig



# Layout

app = dash.Dash(__name__)

app.layout = html.Div(children=[
                      html.Div([
                      html.H1(
                          children='Servicios profesionales y técnicos en México en 2022',
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

                      html.P(children='La mayor parte de los servicios técnicos y profesionales en México están concentrados en servicios jurídicos\
                           \ny contables. Los servicios en tecnologías de la información apenas representan una mínima parte.', style={
                          'textAlign': 'center',
                          'color': 'black',
                          'fontFamily': 'Helvetica',
                          'fontSize': '15'
                          }),

                      html.Div(children=[
                              html.Label('Selecciona servicio profesional o técnico:'),
                              html.Br(),
                              dcc.Dropdown(options, 
                                           'Servicios de diseño de sistemas de cómputo y servicios relacionados', 
                                           id='dropdown'
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
                              figure=barchart(df)
                            )], 
                             style={'margin-top': '20px',
                                        'margin-left': '10px',
                                        'width': '32%', 
                                        'height': gheight, 
                                        'float': 'center', 
                                       }
                            ),

                          html.Div([
                            dcc.Graph(
                              id='scatter',
                              #figure=scatter(df)
                            )], 
                            style={'margin-top': '-450px',
                                        'margin-left': '33.5%',
                                        'margin-right': '32%',
                                        'width': '35%', 
                                        'height': gheight, 
                                        'float': 'center', 
                                       }
                            ),
                          
                          html.Div([
                            dcc.Graph(
                              id='donutchart',
                              #figure=donutchart(df)
                            )], 
                             style={'margin-top': '-450px',
                                        'margin-left': '69%',
                                        'margin-right': '10px',
                                        'width': gwidth, 
                                        'height': gheight, 
                                        'float': 'center', 
                                       }
                            ),

                      ],
                      style={
                            'width': '100%', 
                             }
                       ),

                      html.Div([
                          html.Div([
                              dcc.Graph(
                              id='mapa',
                              #figure=mapa(df)
                              ),
                          ],
                          style={'margin-top': '10px',
                                'margin-left': '10px',
                                'margin-right': '10px',
                                'margin-bottom': '10px',
                                'width': '32%', 
                                'height': gheight, 
                                'float': 'center', 
                                }
                          ),

                          html.Div([
                                dcc.Graph(
                                  id='histogram',
                                  #figure=histogram(df)
                                )], 
                                  style={'margin-top': '-460px',
                                        'margin-left': '33.5%',
                                        'margin-right': '32%',
                                        'width': '35%', 
                                        'margin-bottom': '10px',
                                        'height': gheight, 
                                        'float': 'center', 
                                        }
                                ),
                        
                        html.Div([
                                dcc.Graph(
                                  id='areachart',
                                  #figure=areachart(df)
                                )], 
                                  style={'margin-top': '-460px',
                                        'margin-left': '69%',
                                        'margin-right': '10px',
                                        'margin-bottom': '10px',
                                        'width': gwidth, 
                                        'height': gheight, 
                                        'float': 'center', 
                                        }
                                ),
                      ]),
                                        

                    ], style={'width': '100%', 
                              'overflow': 'hidden',
                              'background-color': 'aliceblue', 
                              })    

# Callback

@app.callback(
    [
    #Output("barchart", "figure"), 
    Output("scatter", "figure"), 
    Output("donutchart", "figure"),
    Output("mapa", "figure"),
    Output("histogram", "figure"),
    Output("areachart", "figure")], 
    [Input("dropdown", "value")]
    )
def update_charts(dropdown):
    
    dff = df.copy()
    dff2 = df.copy()

    dff = dff[dff['nombre_act'] == dropdown]

    #fig_bar = barchart(dff)
    fig_scatter = scatter(dff)
    fig_donut = donutchart(dff2, dropdown)
    fig_map = mapa(dff)
    fig_hist = histogram(dff)
    fig_area = areachart(dff)

    #fig_bar.update_layout(transition_duration=500)
    fig_scatter.update_layout(transition_duration=500)
    fig_donut.update_layout(transition_duration=500)
    fig_map.update_layout(transition_duration=500)
    fig_hist.update_layout(transition_duration=500)
    fig_area.update_layout(transition_duration=500)
    
    return fig_scatter, fig_donut, fig_map, fig_hist, fig_area

app.run_server(debug=True)