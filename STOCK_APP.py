# -*- coding: utf-8 -*-
"""
Created on Wed Sep 13 17:55:09 2023

@author: user
"""
import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash_bootstrap_templates import load_figure_template
import plotly.graph_objects as go
from datetime import datetime

df = pd.read_excel("StockData.xlsx")
df['Date'] = pd.to_datetime(df['Date'])

pivoted_df = df.pivot(index='Date', columns='Company', values='High')
pivoted_df = pivoted_df.dropna()
pivoted_df = pivoted_df.loc['2021-01-01':'2021-12-31']

app = dash.Dash(title="Stocks App", external_stylesheets=[dbc.themes.BOOTSTRAP])  
server = app.server
app.title = "Stock Prices"
load_figure_template('BOOTSTRAP')  

title = html.Div(
    children=[
        html.H1(
            "STOCK MARKET ANALYSIS",
            style={'font-size': '30px', 'text-align': 'center', 'font-weight': 'bold', 'color': '#060233',
                   'backgroundColor': '#a2b8eb', 'margin': '8px', 'padding': '5px'}
        )
    ]
)

footer = html.Div(
    children=[
        html.Div(
            [
                html.P('CREATED BY:', style={'font-size': '12px', 'text-align': 'center', 'font-weight': 'bold',
                                              'color': 'black'}),
                html.P('THEEKSHITHA VARATHARAJSARMA', style={'font-size': '12px', 'text-align': 'center',
                                                            'font-weight': 'bold', 'color': 'black'}),
            ],
            style={'background-color': '#d5e6f5', 'padding': '3px', 'border-radius': '5px', 'margin-bottom': '0px',
                   'position': 'fixed', 'bottom': '0', 'left': '85%', 'width': '15%'}
        )
    ]
)

style = {'text-align': 'center',
         'padding': '0px 15px 0px 15px',
         'background-color': 'white',
         'font-weight': 'bold',
         'color': '#06314f'}

app.layout = html.Div([
    title,
    dcc.Tabs(
        id="tabs-with-classes",
        value='tab-1',
        parent_className='custom-tabs',
        className='custom-tabs-container',
        children=[
            dcc.Tab(
                label='Overview',
                value='tab-1',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#d5e6f5', 'color': 'black'}
            ),
            dcc.Tab(
                label='Stock Pattern Analysis',
                value='tab-2',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#d5e6f5', 'color': 'black'}
            ),
            dcc.Tab(
                label='Correlation Analysis of Variables',
                value='tab-3',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#d5e6f5', 'color': 'black'}
            ),
            dcc.Tab(
                label='Overall Analysis',
                value='tab-4',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#d5e6f5', 'color': 'black'}
            ),
            dcc.Tab(
                label='Correlation Analysis of Companies',
                value='tab-5',
                className='custom-tab',
                selected_className='custom-tab--selected',
                style={'backgroundColor': '#d5e6f5', 'color': 'black'}
            ),
        ]
    ),
    html.Div(id='tabs-content-classes'),
    footer
])

@app.callback(Output('tabs-content-classes', 'children'),
              Input('tabs-with-classes', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return html.Div(
            children=[
                html.H1(
                    dcc.Markdown(
                        '''
                        This dashboard analyzes the stock prices for some of the biggest companies  
                        during a six-year period of 2015 - 2021
                        '''
                    ),
                    style={'fontSize': '30px', 'textAlign': 'center', 'color': '#3c3896', 'marginTop': '42px'}
                ),
                html.H5(
                    dcc.Markdown(
                        '''
                        The Companies are: 
                        Apple,
                        Amazon,
                        Netflix, 
                        Microsoft, 
                        Google,
                        Facebook,
                        Tesla,
                        Walmart,
                        Zoom
                        '''
                    ),
                    style={'fontSize': '18px', 'textAlign': 'center', 'color': '#040636'}
                ),
                html.H6(
                    dcc.Markdown(
                        '''
                        The following are values recorded each day for each company:  
                            
                        Low : The lowest price per share  
                        
                        High : The highest price per share  
                        
                        Open : The opening price per share  
                        
                        Closed : The closing price per share  
                        
                        Adj Close : Closing price amended with any corporate actions occurred before the next day  
                        
                        &  
                        
                        Volume : The amount of stocks traded
                        '''
                    ),
                    style={'fontSize': '13.5px', 'textAlign': 'center', 'marginBottom': '0px', 'marginTop': '65px'}
                ),
                html.Img(
                    src="https://camo.githubusercontent.com/af9dec3649e8fbb13ea37855b9df15809ae6bb40d1902e86a898d11278d3b75d/68747470733a2f2f7777772e7063722d6f6e6c696e652e62697a2f77702d636f6e74656e742f75706c6f6164732f6661616e672d6f776e2d6c6f676f2d363630783333302e6a7067",
                    style={'max-width': '80%', 'height': 'auto', 'display': 'block', 'margin': '0 auto', 'max-height': '140px'}
                    ),
            ],
            style={'text-align': 'center',
                   'height': 'calc(100vh - 175px)',  
                   })
    elif tab == 'tab-2':
        filtered_df = df[df['Date'].dt.year >= 2015]
        date_range_min = filtered_df['Date'].min().timestamp()
        date_range_max = filtered_df['Date'].max().timestamp()
        years = range(2015, 2022)
        marks = {pd.Timestamp(f'{year}-01-01').timestamp(): {'label': str(year)} for year in years}

        return html.Div([
            html.H6('Number of Shares Traded by Time'),
            html.P("Select the company of interest",
                   style={'font-weight': 'normal', 'fontSize': '13px', 'color': '#5580e6'}),
            dcc.Dropdown(
                id="Company",
                value=['Amazon'],
                multi=True,
                options=[{'label': x, 'value': x} for x in filtered_df.Company.unique()],
                style={'font-weight': 'normal'},
            ),
            dcc.Graph(id="line1"),

            html.Div([
                dcc.RangeSlider(
                    id='date-range-slider',
                    min=date_range_min,
                    max=date_range_max,
                    marks=marks,
                    value=[date_range_min, date_range_max],
                    allowCross=False,
                    pushable=1
                ),
            ]),
            html.P("Select the date range preferred", style={'font-weight': 'normal', 'fontSize': '13px', 'color': '#5580e6'}),
        ],
            style=style)
    elif tab == 'tab-3':
        return html.Div(
            children=[
                html.H6('Scatter Plot of Stock Prices'),
                html.P("Select the y axis preferred", style={'font-weight': 'normal', 'fontSize': '13px', 'color': '#5580e6'}),
                dcc.RadioItems(
                    id="y_axis",
                    options=[
                        {'label': 'Low', 'value': 'Low'},
                        {'label': 'High', 'value': 'High'},
                        {'label': 'Open', 'value': 'Open'},
                        {'label': 'Close', 'value': 'Close'},
                        {'label': 'Adj Close', 'value': 'Adj Close'}
                    ],
                    style={'font-weight': 'normal', 'fontSize': '12px'},
                    value='Close'
                ),
                dcc.Graph(
                    id="graph6",
                ),
            ],
            style=style
        )
    elif tab == 'tab-4':
        company_volume = df.groupby('Company')['Volume'].sum().reset_index()

        fig = px.bar(
            company_volume,
            x='Company',
            y='Volume'
        )
        fig.update_layout(
            title="Total Shares Traded in Each Company",
            xaxis_title="Company",
            yaxis_title="Total Share Volume",
            title_x=0.5,
            height=520
        )

        return html.Div([html.H6("Overall Values for the 6 Year Period"),
                         html.P("Click on the bars to select the company.", style={'font-weight': 'normal', 'fontSize': '13px', 'color': '#5580e6'}),
            html.Div([
                dcc.Graph(id="bar-chart", figure=fig),
            ], style={'width': '100%', 'display': 'inline-block'}),  
            html.Div([
                dcc.Graph(id="box-plots")
            ], style={'width': '100%', 'display': 'inline-block'})  
        ],
            style=style)

    elif tab == 'tab-5':
        return html.Div([
            html.H6('Highest Price Reached in 2021'),
            html.P("Select the companies below", style={'font-weight': 'normal', 'fontSize': '13px', 'color': '#5580e6'}),
            dcc.Dropdown(
                id="x-axis-dropdown",
                options=[{'label': company, 'value': company} for company in pivoted_df.columns],
                style={'font-weight': 'normal'},
                value=pivoted_df.columns[0],
                multi=False
            ),
            dcc.Dropdown(
                id="y-axis-dropdown",
                options=[{'label': company, 'value': company} for company in pivoted_df.columns],
                style={'font-weight': 'normal'},
                value=pivoted_df.columns[1],
                multi=False
            ),
            dcc.Graph(id="scatter-plot"),
            html.P("Click on the desired point on the chart above to see more details",
                   style={'font-weight': 'normal', 'fontSize': '13px', 'color': '#5580e6'}),
            html.Div(id="grouped-bar-chart")
        ],
            style=style)
###############################3
@app.callback(
    Output("line1", "figure"),
    Output("date-range-slider", "marks"),  
    Input("Company", "value"),
    Input('date-range-slider', 'value')
)
def update_line_chart(company, dates):
    filtered_df = df[df['Company'].isin(company) & df['Date'].between(pd.to_datetime(dates[0], unit='s'),
                                                                    pd.to_datetime(dates[1], unit='s'))]

    # Generate the marks based on the filtered data
    years = filtered_df['Date'].dt.year.unique()
    marks = {pd.Timestamp(f'{year}-01-01').timestamp(): {'label': str(year)} for year in years}

    fig = px.line(
        filtered_df,
        x="Date",
        y="Volume",
        color='Company'
    ).update_layout(
        title="Date vs Volume",
        xaxis_title="Date",
        yaxis_title="Volume",
        title_x=0.5,
        height=420
    )
    return fig, marks  

@app.callback(
    Output("graph6", "figure"),
    Input("y_axis", "value")
)
def update_scatter_chart(value):
    filtered_df = df.copy()

    correlation = filtered_df['Volume'].corr(filtered_df[value])

    fig = go.Figure()
    for company in filtered_df['Company'].unique():
        company_df = filtered_df[filtered_df['Company'] == company]
        fig.add_trace(go.Scatter(
            x=company_df['Volume'],
            y=company_df[value],
            mode='markers',
            marker=dict(size=3.5),
            name=company,
            hovertemplate='Volume: %{x}<br>' + value + ': %{y}<extra></extra>'
        ))

    fig.update_layout(
        title=f"Number of Shares Traded vs {value} - Correlation: {correlation:.4f}",
        xaxis_title="Number of shares traded",
        yaxis_title=value,
        title_x=0.5,
        height=440
    )

    return fig

@app.callback(
    Output("box-plots", "figure"),
    Input("bar-chart", "clickData")
)
def update_box_plots(click_data):
    if click_data is not None:
        selected_company = click_data['points'][0]['x']
    else:
        selected_company = 'Microsoft'  

    company_data = df[df['Company'] == selected_company]
    colors = ['#75fa97', '#75faed', '#75c3fa', '#a175fa', '#dd75fa']
    fig = go.Figure()
    for i, column in enumerate(['Open', 'Close', 'Adj Close', 'High', 'Low']):
        fig.add_trace(go.Box(
            y=company_data[column],
            name=column,
            marker_color=colors[i]
        ))

    fig.update_layout(
        title=f"Distribution of Stock Prices for {selected_company}",
        xaxis_title="Column",
        yaxis_title="Stock Price",
        title_x=0.5,
        height=520
    )

    return fig

@app.callback(
    Output("scatter-plot", "figure"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value")
)
def update_scatter_plot(x_axis, y_axis):
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=pivoted_df[x_axis],
        y=pivoted_df[y_axis],
        mode='markers',
        text=pivoted_df.index.strftime('%Y-%m-%d'),
        hovertemplate='Date: %{text}<br>' + x_axis + ': %{x}<br>' + y_axis + ': %{y}<extra></extra>'
    ))
    fig.update_layout(
        title=f"{x_axis} vs {y_axis}",
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        title_x=0.5
    )
    return fig

@app.callback(
    Output("grouped-bar-chart", "children"),
    Input("scatter-plot", "clickData"),
    Input("x-axis-dropdown", "value"),
    Input("y-axis-dropdown", "value")
)
def update_grouped_bar_chart(click_data, company1, company2):
    if click_data is None:
    
        default_click_data = {"points": [{"text": pivoted_df.index[0].strftime("%Y-%m-d")}]}
        click_data = default_click_data

    selected_date_str = click_data["points"][0]["text"]
    selected_date = datetime.strptime(selected_date_str, "%Y-%m-%d").date()
    selected_companies = [company1, company2]

    filtered_df = df[
        (df["Company"].isin(selected_companies)) & (df["Date"].dt.date == selected_date)
    ]

    colors = ['#75fa97', '#75faed', '#75c3fa', '#a175fa', '#dd75fa']

    fig = go.Figure()

    bar_width = 0.7 

    for i, column in enumerate(["Open", "High", "Close", "Adj Close", "Low"]):
        fig.add_trace(
            go.Bar(
                x=filtered_df["Company"],
                y=filtered_df[column],
                name=column,
                offsetgroup=i,
                width=bar_width / len(["Open", "High", "Close", "Adj Close", "Low"]),
                marker_color=colors[i]
            )
        )

    fig.update_layout(
        barmode="group",
        bargap=0.1, 
        title=f"Stock Prices on {selected_date_str}",
        xaxis_title="Company",
        yaxis_title="Price",
    )

    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run_server(port=9221)
