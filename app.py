import dash
import pandas as pd
import plotly.express as px
from dash import dcc, html, callback, dependencies

df = pd.read_csv('sicCd_name.csv')
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

available_indicators = df['sickNm'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Dropdown(
                id='crossfilter-xaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='콜레라'
            ),
            dcc.RadioItems(
                id='crossfilter-xaxis-type',
                options=[{'label': i, 'value': i} for i in ['양방', '한방']],
                value='양방',
                labelStyle={'display': 'inline-block'}
            )
        ],
        style={'width': '49%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown(
                id='crossfilter-yaxis-column',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='콜레라'
            ),
            dcc.RadioItems(
                id='crossfilter-yaxis-type',
                options=[{'label': i, 'value': i} for i in ['양방', '한방']],
                value='양방',
                labelStyle={'display': 'inline-block'}
            )
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
             id='crossfilter-indicator-scatter',
           
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

     html.Div([
        dcc.Graph(
             id='crossfilter-test-scatter',
           
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),

])

@callback(
    dash.dependencies.Output('crossfilter-indicator-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-xaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-xaxis-type', 'value')]

    )
def update_graph_scatter(xaxis_column_name, xaxis_type):
    Cd = df.loc[df['sickNm'] == xaxis_column_name, 'sickCd'].iloc[0]
    dff = pd.read_csv(f'성별나이/{xaxis_type}/sickCd_{Cd}.csv')
    yearly_sum = dff.groupby('year')['specCnt'].sum().reset_index()
    
    fig = px.scatter(x=yearly_sum['year'],
            y=yearly_sum['specCnt'])
    fig.update_traces(mode='lines+markers', line_shape='linear')
    fig.update_xaxes(title=xaxis_column_name)
    fig.update_yaxes(title='환자 수')
    fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0})
    return fig

@callback(
    dash.dependencies.Output('crossfilter-test-scatter', 'figure'),
    [dash.dependencies.Input('crossfilter-yaxis-column', 'value'),
     dash.dependencies.Input('crossfilter-yaxis-type', 'value')]

    )
def update_graph_bar(yaxis_column_name, yaxis_type):
    Cd = df.loc[df['sickNm'] == yaxis_column_name, 'sickCd'].iloc[0]
    dff = pd.read_csv(f'성별나이/{yaxis_type}/sickCd_{Cd}.csv')
    year_age_sum = dff.groupby(['year', 'age'])['specCnt'].sum().reset_index()
    fig = px.bar(
    year_age_sum, 
    x='year', 
    y='specCnt', 
    color='age', 
    barmode='group',  # 같은 x값에 대해 그룹화된 막대
    labels={'specCnt': 'SpecCnt Sum', 'year': 'Year', 'age': 'Age'}
    )




    # yearly_sum = dff.groupby('age')['specCnt'].sum().reset_index()
    
    # fig = px.scatter(x=yearly_sum['age'],
    #         y=yearly_sum['specCnt'])
    # fig.update_traces(mode='lines+markers', line_shape='linear')
    # fig.update_xaxes(title=yaxis_column_name)
    # fig.update_yaxes(title='환자 수')
    # fig.update_layout(margin={'l': 40, 'b': 40, 't': 10, 'r': 0})
    return fig


if __name__ == '__main__':
    app.run(debug=True)