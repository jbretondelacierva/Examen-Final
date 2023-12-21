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
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.SPACELAB], 
                meta_tags=[{"name": "viewport", "content": "width=device-width"}],
                suppress_callback_exceptions=True)

# Lectura de datos
bank_df = pd.read_csv("bank-full.csv", delimiter=";")
bank_df.dropna(inplace=True)
bank_df['job'] = bank_df['job'].astype('category')
bank_df['marital'] = bank_df['marital'].astype('category')
bank_df['education'] = bank_df['education'].astype('category')
bank_df['default'] = bank_df['default'].astype('category')
bank_df['housing'] = bank_df['housing'].astype('category')
bank_df['loan'] = bank_df['loan'].astype('category')
bank_df['day'] = bank_df['day'].astype('category')
bank_df['month'] = bank_df['month'].astype('category')
bank_df['poutcome'] = bank_df['poutcome'].astype('category')
bank_df['y'] = bank_df['y'].astype('category')
bank_df['y_bool'] = bank_df['y'].apply(lambda x: 1 if x == 'yes' else 0)
bank_df['y_bool'] = bank_df['y_bool'].astype('int')

# Convert string columns into dummy variables
string_columns = ['job', 'marital', 'education', 'default', 'housing', 'loan', 'day', 'month', 'poutcome','contact']
bank_df = pd.get_dummies(bank_df, columns=string_columns)

bank_df.dtypes
bank_df


# Build of the app


# Definir el layout de la página inicial
app.layout = html.Div([
    html.Div([
        dbc.NavbarSimple(
            brand="Analisis de las campañas de marketing y futuras mejoras a futuro",
            color="#3F556A",
            dark=True
        ), 
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1('Exito en funcion de la edad', style={'textAlign': 'center'}),
                    
                # Componente para elegir qué predicciones mostrar
                dcc.Checklist(
                    id='selector_age',
                    options=[
                        {'label': 'Si', 'value': 'Si'},
                        {'label': 'No', 'value': 'No'}
                    ],
                    value=['Si', 'No'],
                ),
                dcc.Graph(id='grafico_predicciones', style={'height': '600px'}),  # Aumentar altura de la gráfica
            ])
        ])
])
])


# Definir callbacks
@callback(
    Output('histogramAge', 'figure'),
    [Input('selector_age', 'value')]  # Se activa con el cambio en el selector
)
def histogramAge(selector):

    fig = px.histogram(bank_df, x="age", color="y",
                    labels = {"streams": "Reproducciones"},
                    histnorm='probability density',
                    nbins = 100,
                    opacity=0.6)
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)