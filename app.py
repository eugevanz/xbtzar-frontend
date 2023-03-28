from os import getenv
from dash import Dash, html, dcc
from requests import get
from sqlalchemy import create_engine, text
import pandas as pd
from fig_generator import figure
from fetch_data import fetch

app = Dash(
    __name__,
    external_scripts=["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
)

server = app.server

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
                    html.Div(f"R {fetch('select * from accounts').ZAR[0]}"),
                    html.Div(f"B {fetch('select * from accounts').XBT[0]}"),
                    html.Div(f"E {fetch('select * from accounts').ETH[0]}"),
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
                                        'BUY' if bool(
                                            fetch('select * from xbtzar_deriv').late_signal[0]
                                        ) else 'SELL',
                                        className='text-3xl font-extrabold text-[#d97706]'
                                    ),
                                    html.H1(
                                        'XBTZAR', className='text-6xl font-extrabold leading-none tracking-tight'
                                    ),
                                    html.P(
                                        fetch('select * from accounts').description[0],
                                        className='italic',
                                        style={'fontSize': '11px'}
                                    )
                                ],
                                className='p-4'
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        dcc.Graph(
                                            figure=figure(fetch('select * from ethzar_df')),
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
                                                          'mb-0 sm:mb-3'
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P('Close', className='text-slate-600'),
                                                    html.P(
                                                        f'R {fetch("select * from ethzar_deriv").late_close[0]}',
                                                        className='text-[#0891b2]'
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P('EMA12', className='text-slate-600'),
                                                    html.P(
                                                        f'R {fetch("select * from ethzar_deriv").late_ema[0]}',
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
                                df=fetch('select * from xbtzar_df'),
                                max_high=int(fetch('select * from xbtzar_deriv').max_high[0]),
                                min_low=int(fetch('select * from xbtzar_deriv').min_low[0]),
                                max_close=int(fetch('select * from xbtzar_deriv').max_close[0]),
                                min_close=int(fetch('select * from xbtzar_deriv').min_close[0]),
                                avg_close=float(fetch('select * from xbtzar_deriv').avg_close[0])
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
                                        f'R {fetch("select * from xbtzar_deriv").late_close[0]}',
                                        className='text-[#0891b2]'
                                    )
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.P('EMA12', className='text-slate-600'),
                                    html.P(
                                        f'R {fetch("select * from xbtzar_deriv").late_ema[0]}',
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
