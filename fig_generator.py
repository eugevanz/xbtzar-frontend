import plotly.graph_objs as go
import pandas as pd


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
                )
            ]
        )

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
