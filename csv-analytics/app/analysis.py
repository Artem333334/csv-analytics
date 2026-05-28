import plotly.express as px

def build_chart(df):

    numeric = df.select_dtypes(include='number')

    if len(numeric.columns) >= 2:

        fig = px.scatter(
            numeric,
            x=numeric.columns[0],
            y=numeric.columns[1],
            title='График данных'
        )

        return fig.to_html(full_html=False)

    return '<p>Недостаточно числовых данных</p>'