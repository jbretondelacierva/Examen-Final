# Importar librerías
import dash
from dash import Dash, html, dcc, dash_table
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
from dash import Dash, html, dcc, dash_table, callback
import plotly.graph_objs as go
from datetime import datetime, timedelta
from dash.dependencies import Input, Output
import plotly.express as px
import requests
import pandas as pd
import dash
import plotly.figure_factory as ff

# Lectura de datos
data=pd.read_csv('datos_examen.csv')

# Definicion de variables
list_vars=list(data.columns)[1:10]

# Definicion de funciones
def graf_dispersion_color_mean(data, var1, var2, var3):
    fig = px.scatter(data, 
                     x=var1, 
                     y=var2,
                     color=var3,
                     color_continuous_scale=px.colors.sequential.Blugrn,
                     hover_data=["country"])
    
    fig.add_vline(x=np.mean(data[[var1]])[0], opacity=1, line_width=0.75, line_dash='dash', line_color='skyblue')
    fig.add_hline(y=np.mean(data[[var2]])[0], opacity=1, line_width=0.75, line_dash='dash', line_color='skyblue')
    
    fig.update_layout(template='plotly_white')
    
    return fig



# Build of the app
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SPACELAB], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)

# Definir el layout de la página inicial
app.layout = html.Div([
    html.Div([
        dbc.NavbarSimple(
            brand="Descriptivo y clustering de paises con variables socio-económicas y de salud",
            color="#3F556A",
            dark=True
        ), 
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H6("Comparativa triple de variables",style={'margin-top':'40px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                html.Hr(style={'border': '1px solid gray','border-radius': '10px'}),
                dcc.Dropdown(
                    list_vars,
                    placeholder="Select a variable", id='dropdown1',value='child_mort',
                    style={'margin-top':'40px','margin-bottom':'60px','border-width':'2px','border-color':'#a0a3a2',
                           'font-family': "Times New Roman",'border-radius': '5px','width':'50%'}
                    ),
                dcc.Dropdown(
                    list_vars,
                    placeholder="Select a variable", id='dropdown2', value='exports',
                    style={'margin-top':'60px','margin-bottom':'60px','border-width':'2px','border-color':'#a0a3a2',
                           'font-family': "Times New Roman",'border-radius': '5px','width':'50%'}
                    ),
                dcc.Dropdown(
                    list_vars,
                    placeholder="Select a variable", id='dropdown3', value='health',
                    style={'margin-top':'60px','margin-bottom':'50px','border-width':'2px','border-color':'#a0a3a2',
                           'font-family': "Times New Roman",'border-radius': '5px','width':'50%'}
                    ),
                dcc.Graph(id='figura_1')
            ]),
            dbc.Col([
                html.H6("Diagrama caja de variables seleccionadas",style={'margin-top':'40px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                html.Hr(style={'border': '1px solid gray','border-radius': '10px'}),
                html.Div([
                    html.H6('First Select Value',style={'margin-top':'25px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                    dcc.RangeSlider(min=0, max=500, value=[0, 200],id='range_slider1',className='slider_range',tooltip={"placement": "bottom", "always_visible": True})
                ],style={'margin-top':'40px','margin-bottom':'5px','width':'50%'}),
                html.Div([
                    html.H6('Second Select Value',style={'margin-top':'25px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                    dcc.RangeSlider(min=0, max=500, value=[0, 200],id='range_slider2',className='slider_range',tooltip={"placement": "bottom", "always_visible": True})
                ],style={'margin-top':'5px','margin-bottom':'30px','width':'50%'}),
                html.Div([
                    html.H6('Third Select Value',style={'margin-top':'25px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                    dcc.RangeSlider(min=0, max=500, value=[0, 200],id='range_slider3',className='slider_range',tooltip={"placement": "bottom", "always_visible": True})
                ],style={'margin-top':'5px','margin-bottom':'30px','width':'50%'}),
                dcc.Graph(id='figura_2')
            ])
        ]),
        dbc.Row([
            dbc.Col([
                html.H6("Clustering en función de variables",style={'margin-top':'20px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                html.Hr(style={'border': '1px solid gray','border-radius': '10px'}),
                dcc.Dropdown(
                    list_vars,
                    placeholder="Select a variable", id='dropdown_clust1',value='health',
                    style={'margin-top':'40px','margin-bottom':'10px','border-width':'2px','border-color':'#a0a3a2',
                           'font-family': "Times New Roman",'border-radius': '5px','width':'50%'}
                    ),
                dcc.Dropdown(
                    list_vars,
                    placeholder="Select a variable", id='dropdown_clust2',value='gdpp',
                    style={'margin-top':'10px','margin-bottom':'5px','border-width':'2px','border-color':'#a0a3a2',
                           'font-family': "Times New Roman",'border-radius': '5px','width':'50%'}
                    ),
                dcc.Graph(id='figura_3'),
                dcc.Textarea(
                    value='Cluster0: High GDPP with high life expentancy and lower child mort.\nCluster1: Low GDPP with low life expentancy and medium high child mort.\nCluster2: Medium high GDPP with medium high life expentancy and low child mort.\nCluster3: Lowest GDPP with lowest life expentancy and highest child mort.\nCluster4: Low GDPP with medium low life expentancy and higher child mort.\nCluster5: Highest GDPP with highest life expentancy and lowest child mort.\nCluster6: Medium low GDPP with medium low life expentancy and medium low child mort.',
                    style={'margin-top':'30px','width': '100%', 'height': '175px'},
                ),
            ]),
            dbc.Col([
                html.H6("PCA clustering de los datos",style={'margin-top':'20px','font-family': 'Arial Black', 'color':'#6C6C6C'}),
                html.Hr(style={'border': '1px solid gray','border-radius': '10px','margin-bottom':'110px'}),
                dcc.Graph(figure=graph_pca())
            ])
        ])
    ])
])

# Definir callbacks
@app.callback(Output('figura_1', 'figure'), 
              [Input('dropdown1','value'),
               Input('dropdown2','value'),
               Input('dropdown3','value')]
)
def draw_figure_1(dropdown1,dropdown2,dropdown3):
   fig=graf_dispersion_color_mean(data,dropdown1,dropdown2,dropdown3)
   return fig

@app.callback(Output('figura_2', 'figure'), 
              [Input('range_slider1','value'),
               Input('range_slider2','value'),
               Input('range_slider3','value'),
               Input('dropdown1','value'),
               Input('dropdown2','value'),
               Input('dropdown3','value')]
)
def draw_figure_2(range_slider1,range_slider2,range_slider3,dropdown1,dropdown2,dropdown3): 
    data_aux=data.loc[(data[dropdown1]>=range_slider1[0])&(data[dropdown1]<=range_slider1[1])&
                      (data[dropdown2]>=range_slider2[0])&(data[dropdown2]<=range_slider2[1])&
                      (data[dropdown3]>=range_slider3[0])&(data[dropdown3]<=range_slider3[1])]
    fig=cajas_graph(data_aux,dropdown1,dropdown2,dropdown3)
    return fig

@app.callback(Output('figura_3', 'figure'), 
              [Input('dropdown_clust1','value'),
               Input('dropdown_clust2','value')]
)
def draw_figure_3(dropdown_clust1,dropdown_clust2):
    fig=graph_clust(dropdown_clust1,dropdown_clust2)
    return fig

# Run de la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)