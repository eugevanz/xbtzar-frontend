import plotly.graph_objs as go
import pandas as pd


# Define the update_graph function to update the dcc.Graph component with the ticker data
def figure(data):
    df = pd.DataFrame(data)

    fig = go.Figure(
        data=[
            go.Candlestick(
                x=df['Time'],
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close']
            ),
            # go.Scatter(
            #     x=[item['timestamp'] for item in data_list],
            #     y=[float(item['last_trade']) for item in data_list],
            #     text='Price', line=dict(color='#d97706', width=12, shape='spline')
            # )
        ]
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
