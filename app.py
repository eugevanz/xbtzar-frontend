from os import getenv

from dash import Dash, html, dcc
from requests import get
from sqlalchemy import create_engine, text
import pandas as pd
from fig_generator import figure

app = Dash(
    __name__,
    external_scripts=["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
)

server = app.server


def handle_str_request(query):
    return get(query).text if 'http' in query else get(f'https://model-server-api.onrender.com{query}').text


def handle_dict_request(query):
    return get(query).json() if 'http' in query else get(f'https://model-server-api.onrender.com{query}').json()


def candles(tbl_name):
    result = []
    query = text('SELECT * FROM :tbl_name')
    try:
        # Create the SQLAlchemy engine
        engine = create_engine(getenv('RENDER_SQL_EXT'), echo=True, future=True)
        # Define the query to select data from the table
        with engine.connect() as connection:
            result = connection.execute(query, {'tbl_name': tbl_name})
            result = pd.DataFrame(result.fetchall())
    except Exception as error:
        print(error)

    return result.to_dict()


def fetchones(col_name, tbl_name):
    result = f'derives {col_name}, {tbl_name} FAILED'
    query = text('SELECT :col_name FROM :tbl_name')
    try:
        # Create the SQLAlchemy engine
        engine = create_engine(getenv('RENDER_SQL_EXT'), echo=True, future=True)
        # Define the query to select data from the table
        with engine.connect() as connection:
            result = connection.execute(query, {'col_name': col_name, 'tbl_name': tbl_name})
            result = result.fetchone()[0]
    except Exception as error:
        print(error)

    return result


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
                    html.Div(fetchones('ZAR', 'accounts')),
                    html.Div(fetchones('XBT', 'accounts')),
                    html.Div(fetchones('ETH', 'accounts')),
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
                                        'BUY' if bool(fetchones('late_signal', 'xbtzar_deriv')) else 'SELL',
                                        className='text-3xl font-extrabold text-[#d97706]'
                                    ),
                                    html.H1(
                                        'XBTZAR',
                                        className='text-6xl font-extrabold leading-none tracking-tight',
                                        id='xbt-pair'
                                    ),
                                    html.P(
                                        fetchones('description', 'accounts'), className='italic',
                                        style={'fontSize': '11px'}
                                    )
                                ],
                                className='p-4'
                            ),
                            html.Div(
                                children=[
                                    html.Div(
                                        dcc.Graph(
                                            figure=figure(candles('ethzar_df')),
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
                                                        f'R {fetchones("late_close", "ethzar_deriv")}',
                                                        className='text-[#0891b2]'
                                                    )
                                                ]
                                            ),
                                            html.Div(
                                                children=[
                                                    html.P('EMA12', className='text-slate-600'),
                                                    html.P(
                                                        f'R {fetchones("late_ema", "ethzar_deriv")}',
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
                                df=candles('xbtzar_df'),
                                max_high=int(fetchones('max_high', 'xbtzar_deriv')),
                                min_low=int(fetchones('min_low', 'xbtzar_deriv')),
                                max_close=int(fetchones('max_close', 'xbtzar_deriv')),
                                min_close=int(fetchones('min_close', 'xbtzar_deriv')),
                                avg_close=float(fetchones('avg_close', 'xbtzar_deriv'))
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
                                        f'R {fetchones("late_close", "xbtzar_deriv")}',
                                        className='text-[#0891b2]'
                                    )
                                ]
                            ),
                            html.Div(
                                children=[
                                    html.P('EMA12', className='text-slate-600'),
                                    html.P(
                                        f'R {fetchones("late_ema", "xbtzar_deriv")}',
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
