from dash import Dash, html, dcc, Input, Output, callback
import pandas as pd
import plotly.express as px
from datetime import datetime


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

df = pd.read_csv('detected_classes.csv')

# Définir la fonction de conversion de timestamp en date
def convert_to_date(timestamp):
    try:
        date = datetime.strptime(timestamp.split('.')[0], '%Y%m%d%H%M%S')
        return date
    except ValueError:
        return None

# Appliquer la fonction à la colonne 'id'
df['id'] = df['id'].apply(convert_to_date)

# Filtrer les lignes avec des valeurs de date/heure invalides (NaT)
df = df.dropna(subset=['id'])

# Ajouter une colonne pour le jour de la semaine
df['day_of_week'] = df['id'].dt.day_name()

# Afficher le DataFrame mis à jour pour vérifier la conversion
print(df.head())

app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
                options=[{'label': cls, 'value': cls} for cls in df['class_name'].unique()],
                value=df['class_name'].unique()[0],  # Première classe par défaut
                id='crossfilter-class-column',
            ),
            dcc.RadioItems(
                options=[{'label': 'Linear', 'value': 'Linear'}, {'label': 'Log', 'value': 'Log'}],
                value='Linear',
                id='crossfilter-class-type',
                labelStyle={'display': 'inline-block', 'marginTop': '5px'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
    ], style={
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='crossfilter-indicator-scatter',
            hoverData={'points': [{'customdata': df['id'].iloc[0]}]}
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

    html.Div([
        dcc.Graph(id='class-time-series')
    ], style={'display': 'inline-block', 'width': '49%'}),

    html.Div(dcc.Slider(
        min=df['id'].min().timestamp() * 1000,
        max=df['id'].max().timestamp() * 1000,
        step=None,
        id='crossfilter-id-slider',
        value=df['id'].max().timestamp() * 1000,
        marks={int(date.timestamp() * 1000): {'label': date.strftime('%Y-%m-%d %H:%M:%S'), 'style': {'writingMode': 'vertical-rl'}} for date in df['id']}
    ), style={'width': '49%', 'padding': '0px 20px 20px 20px'}),

    html.Div([
        html.H2('Jours de la semaine correspondant aux timestamps'),
        dcc.Graph(
            id='day-of-week-graph',
            figure={
                'data': [
                    {'x': df['id'], 'y': df['day_of_week'], 'type': 'bar', 'name': 'Jour de la semaine'}
                ],
                'layout': {
                    'title': 'Jours de la semaine correspondant aux timestamps',
                    'xaxis': {'title': 'Timestamp converti en jour de la semaine'},
                    'yaxis': {'title': 'Jour de la semaine'}
                }
            }
        )
    ], style={'width': '80%', 'margin': 'auto', 'marginTop': '50px'})

])


@callback(
    Output('crossfilter-indicator-scatter', 'figure'),
    [Input('crossfilter-class-column', 'value'),
     Input('crossfilter-class-type', 'value'),
     Input('crossfilter-id-slider', 'value')])
def update_graph(class_column, class_type, id_timestamp):
    id_date = datetime.fromtimestamp(id_timestamp / 1000)
    dff = df[df['id'] == id_date]

    fig = px.scatter(dff[dff['class_name'] == class_column],
                     x='id',
                     y='count',
                     hover_name='class_name',
                     labels={'id': 'Timestamp converti en jour de la semaine', 'count': 'Nombre de détections'})

    fig.update_traces(customdata=dff[dff['class_name'] == class_column]['id'])

    fig.update_xaxes(title='id', type='linear')
    fig.update_yaxes(title=class_column, type='linear' if class_type == 'Linear' else 'log')

    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0}, hovermode='closest')

    return fig


def create_time_series(dff, axis_type, title):

    fig = px.scatter(dff, x='id', y='count')

    fig.update_traces(mode='lines+markers')

    fig.update_xaxes(showgrid=False)

    fig.update_yaxes(type='linear' if axis_type == 'Linear' else 'log')

    fig.add_annotation(x=0, y=0.85, xanchor='left', yanchor='bottom',
                       xref='paper', yref='paper', showarrow=False, align='left',
                       text=title)

    fig.update_layout(height=225, margin={'l': 20, 'b': 30, 'r': 10, 't': 10})

    return fig


@callback(
    Output('class-time-series', 'figure'),
    [Input('crossfilter-indicator-scatter', 'hoverData'),
     Input('crossfilter-class-column', 'value'),
     Input('crossfilter-class-type', 'value')])
def update_class_timeseries(hoverData, class_column, axis_type):
    image_id = hoverData['points'][0]['customdata']
    dff = df[df['id'] == image_id]
    dff = dff[dff['class_name'] == class_column]
    title = f'<b>{image_id}</b><br>{class_column}'
    return create_time_series(dff, axis_type, title)


if __name__ == '__main__':
    app.run_server(debug=True)
