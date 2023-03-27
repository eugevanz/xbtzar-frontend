from dash import Dash, html, dcc
from requests import get
import plotly.graph_objs as go
import pandas as pd

app = Dash(
    __name__,
    external_scripts=["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
)

server = app.server


def figure(df, max_high=None, min_low=None, max_close=None, min_close=None, avg_close=None):
    df = pd.DataFrame(df)
    df.index = df.index.astype(int)
    df.open = df.open.astype(int)
    df.high = df.high.astype(int)
    df.low = df.low.astype(int)
    df.close = df.close.astype(int)
    df.EMA12 = df.EMA12.astype(int)

    try:
        fig = go.Figure(
            data=[
                go.Candlestick(
                    x=df.index,
                    open=df.open,
                    high=df.high,
                    low=df.low,
                    close=df.close,
                    increasing={
                        'fillcolor': '#fefae0', 'line': {'color': '#fefae0'}
                    },
                    decreasing={'fillcolor': 'gray', 'line': {'color': 'gray'}}
                ),
                go.Scatter(
                    x=df.index.values, y=df.EMA12, text='EMA12', line=dict(color='#d97706', width=4, shape='spline')
                ),
                # go.Scatter(x=df.timestamp, y=df.close, line=dict(color='#0891b2', width=4, shape='spline'))
            ]
        )
        # print(df.prediction.values)

        for i in range(len(df)):
            if (i + 1) != len(df):
                fig.add_vrect(
                    x0=df.index.values[i],
                    x1=df.index.values[i + 1],
                    fillcolor='#1e293b' if df.prediction.values[i] else '#0f172a',
                    line_width=0,
                    opacity=1,
                    layer='below'
                )

        if avg_close is not None:
            fig.add_hline(y=avg_close, line_width=4, line_dash='dash', line_color='green')
            fig.add_annotation(
                x=df.index.values[0], y=avg_close,
                text='Average price',
                showarrow=True,
                arrowhead=0,
                arrowcolor='green',
                arrowwidth=2,
                font=dict(color='green')
            )

        if max_high is not None:
            fig.add_annotation(
                x=max_high, y=df.loc[max_high].high,
                text='Highest high',
                showarrow=True,
                arrowhead=0,
                arrowcolor='gray',
                arrowwidth=2,
                font=dict(color='gray')
            )

        if min_low is not None:
            fig.add_annotation(
                x=min_low, y=df.loc[min_low].low,
                text='Lowest low',
                showarrow=True,
                arrowhead=0,
                arrowcolor='gray',
                arrowwidth=2,
                font=dict(color='gray')
            )

        if max_close is not None:
            fig.add_annotation(
                x=max_close, y=df.loc[max_close].close,
                text='Highest close',
                showarrow=True,
                arrowhead=0,
                arrowcolor='gray',
                arrowwidth=2,
                font=dict(color='gray')
            )

        if max_high is not None:
            fig.add_annotation(
                x=min_close, y=df.loc[min_close].close,
                text='Lowest close',
                showarrow=True,
                arrowhead=0,
                arrowcolor='gray',
                arrowwidth=2,
                font=dict(color='gray')
            )

        fig.update_layout(
            showlegend=False,
            plot_bgcolor='#0f172a',
            paper_bgcolor='#0f172a',
            margin=dict(
                l=0,
                r=0,
                b=0,
                t=0
            )
        )

        fig.update_xaxes(visible=False)
        fig.update_yaxes(visible=False)

        return fig

    except Exception as er:
        print(er)


def handle_str_request(query):
    return get(query).text if 'http' in query else get(f'https://model-server-api.onrender.com{query}').text


def handle_dict_request(query):
    return get(query).json() if 'http' in query else get(f'https://model-server-api.onrender.com{query}').json()


app.layout = html.Div(
    html.Section(
        children=[
            html.Div(
                [
                    html.Img(
                        className='w-10 h-10 rounded-full',
                        src='https://drive.google.com/uc?export=view&id=1ZVaRMalXlrw1SLKNYkM0Rn5sf46C89L6',
                        alt="Rounded avatar"
                    ),
                    html.Div('ZAR 34567.01'),
                    html.Div('XBT 0.48'),
                    html.Div('ETH 12.04'),
                    html.Div(
                        children=[
                            html.Span('PROFIT ', className='text-[#d97706]'),
                            html.Span('32345.99', className='font-extrabold')
                        ]
                    )

                ],
                className='px-6 flex gap-x-4 italic w-full',
                style={'fontSize': '11px'}
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.Div(
                                        f'{"BUY" if bool(handle_str_request("/derives/late_signal/xbtzar_deriv/")) else "SELL"}',
                                        className='text-3xl font-extrabold text-[#d97706]'
                                    ),
                                    html.H1(
                                        'XBTZAR',
                                        className='text-6xl font-extrabold leading-none tracking-tight',
                                        id='xbt-pair'
                                    ),
                                    html.P(
                                        handle_str_request('/transaction/'), className='italic',
                                        style={'fontSize': '11px'}
                                    )
                                ],
                                className='p-4'
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        dcc.Graph(
                                            figure=figure(handle_dict_request('/candles/ethzar_df/')),
                                            config={'displayModeBar': False},
                                            style={'height': '120px'}
                                        ),
                                        className='max-w-xs hidden sm:block'
                                    ),
                                    html.Div(
                                        [
                                            html.H1(
                                                'ETHZAR',
                                                className='text-2xl font-extrabold leading-none tracking-tight '
                                                          'mb-0 sm:mb-3',
                                                id='eth-pair'
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P('Close', className='text-slate-600'),
                                                    html.P(
                                                        f'R {handle_str_request("/derives/late_close/ethzar_deriv/")}',
                                                        className='text-[#0891b2]'
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P('EMA12', className='text-slate-600'),
                                                    html.P(
                                                        f'R {handle_str_request("/derives/late_ema/ethzar_deriv/")}',
                                                        className='font-bold text-[#d97706]'
                                                    )
                                                ]
                                            )
                                        ],
                                        className='flex flex-row gap-4 items-center sm:gap-0 sm:flex-col'
                                    )
                                ],
                                className='p-3 border border-slate-800 rounded-lg flex flex-row gap-8 w-fit'
                            )
                        ],
                        className='flex md:flex-row flex-col justify-between pt-6'
                    ),
                    html.Div(
                        dcc.Graph(
                            figure=figure(
                                df=handle_dict_request('/candles/xbtzar_df/'),
                                max_high=int(handle_str_request('/derives/max_high/xbtzar_deriv/')),
                                min_low=int(handle_str_request('/derives/min_low/xbtzar_deriv/')),
                                max_close=int(handle_str_request('/derives/max_close/xbtzar_deriv/')),
                                min_close=int(handle_str_request('/derives/min_close/xbtzar_deriv/')),
                                avg_close=float(handle_str_request('/derives/avg_close/xbtzar_deriv/'))
                            ),
                            config={'displayModeBar': False},
                            style={'height': '70vh'}
                        ),
                        className='pt-6 w-full'
                    ),
                    html.Div(
                        '**Predicted Long positions indicated by vertical bars',
                        className='italic px-6',
                        style={'fontSize': '11px'}
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.P('Close', className='text-slate-600'),
                                    html.P(
                                        f'R {handle_str_request("/derives/late_close/xbtzar_deriv/")}',
                                        className='text-[#0891b2]'
                                    )
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.P('EMA12', className='text-slate-600'),
                                    html.P(
                                        f'R {handle_str_request("/derives/late_ema/xbtzar_deriv/")}',
                                        className='font-bold text-[#d97706]'
                                    )
                                ]
                            )
                        ],
                        className='p-6 flex gap-8'
                    )
                ]
            )
        ],
        className='p-3 body-font container mx-auto flex flex-col content-between'
    ),
    className='bg-slate-900 text-slate-400 text-sm h-full pb-24 font-mono'
)

if __name__ == '__main__':
    app.run_server()

    # See PyCharm help at https://www.jetbrains.com/help/pycharm/
