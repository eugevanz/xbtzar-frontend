from dash import Dash, html, dcc
from requests import get

from fig_generator import figure

app = Dash(
    __name__,
    external_scripts=["https://tailwindcss.com/", {"src": "https://cdn.tailwindcss.com"}]
)
server = app.server


def luno(api):
    try:
        return get(
            f'https://model-server-api.onrender.com{api}'
        ).json() if 'candles' in api else get(
            f'https://model-server-api.onrender.com{api}'
        ).text
    except Exception as error:
        return error


app.layout = html.Div(
    html.Section(
        children=[
            dcc.Store(id='local', storage_type='session'),
            html.Div(
                [
                    html.Img(
                        className='w-10 h-10 rounded-full',
                        src='https://drive.google.com/uc?export=view&id=1ZVaRMalXlrw1SLKNYkM0Rn5sf46C89L6',
                        alt="Rounded avatar"
                    ),
                    html.Div(f"R {luno('/bal/zar/')}"),
                    html.Div(f"B {luno('/bal/xbt/')}"),
                    html.Div(f"E {luno('/bal/eth/')}"),
                    html.Div(
                        children=[
                            html.Span('PROFIT ', className='text-[#d97706]'),
                            html.Span('32345.99', className='font-extrabold')
                        ]
                    )
                ],
                className='px-6 flex gap-x-4 italic w-full mb-6',
                style={'fontSize': '11px'}
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=[
                                    html.H1(
                                        'XBTZAR', className='text-6xl font-extrabold leading-none tracking-tight'
                                    ),
                                    html.P(
                                        luno('/transaction/'),
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
                                            figure=figure(luno('/candles/ETHZAR/')),
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
                                                        f"R {luno('/derives/ETHZAR/late_close/')}",
                                                        className='text-[#0891b2]'
                                                    )
                                                ]
                                            )
                                        ],
                                        className='flex flex-row gap-4 justify-items-start sm:gap-0 sm:flex-col'
                                    )
                                ],
                                className='p-3 border border-slate-800 rounded-lg items-center flex flex-row gap-8 '
                                          'w-fit'
                            )
                        ],
                        className='flex md:flex-row flex-col justify-between items-end pt-6'
                    ),
                    html.Div(
                        dcc.Graph(
                            figure=figure(luno('/candles/XBTZAR/')),
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
                        html.Div(
                            children=[
                                html.P('Close', className='text-slate-600'),
                                html.P(
                                    f"R {luno('/derives/XBTZAR/late_close/')}",
                                    className='text-[#0891b2]'
                                )
                            ]
                        ),
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
    # data = luno('/candles/XBTZAR/')
    # Convert the dictionary to a NumPy array
    # df = pd.DataFrame(data)

    # call directional_change function
    # tops, bottoms = directional_change(df['close'].values, df['high'].values, df['low'].values, sigma=0.03)

    # print results
    # print("Tops:", tops)
    # print("Bottoms:", bottoms)

    app.run_server(threaded=True, debug=True)
