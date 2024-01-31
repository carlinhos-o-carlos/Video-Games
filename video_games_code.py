import pandas as pd
import datetime as dt
import plotly.graph_objects as go

df =pd.read_csv("vgsales.csv")

#Funçao para obter o top 10 jogos que venderam no ano (determinado pelo usuario, ano padrão 2020)
def top_10_year(df=df,year=2020):
    result = df[df['Year'] == year].reset_index()
    result = result.iloc[:,2:7]
    return result.head(10)

top_10_year(year=2000)

#Gênero que mais vendeu ao longo dos anos, acumulados, em um grafico
df_graph = df.groupby(by=['Genre']).sum()['Global_Sales'].reset_index().sort_values(by='Global_Sales',ascending=False)

fig = go.Figure()
fig.add_trace(go.Bar(x=df_graph['Global_Sales'], y= df_graph['Genre'],
                marker_color='rgb(26, 118, 255)',
                text=df_graph['Global_Sales'],
                hoverinfo='none',
                orientation='h'))
fig.update_layout({"paper_bgcolor": "rgba(0, 0, 0, 0)",
        "plot_bgcolor": "rgba(0, 0, 0, 0)"})
fig.update_layout(title="Gênero de jogo que mais vendeu mundialmente",yaxis=dict(type='category',autorange="reversed"))
fig.update_xaxes(visible=False, showticklabels=False)
fig.show()

#Qual é o ranking dos top 10 jogos mais vendidos, quando não consideramos a plataforma ?
df_games = df.copy()
df_games= df_games.drop(columns=['Platform','Rank'])
df_games_sales = df_games.groupby(by=['Name','Year','Genre','Publisher']).sum().reset_index().sort_values(by='Global_Sales',ascending=False)
df_games_sales.head(10)

#Qual foi o genero mais famoso durante um período de tempo ?
def tend_jogos(min_year:int=1980,max_year:int=2020):
    if min_year > max_year:
        return "O valor de max_year deve ser maior que o valor de min_year"
    else:
        result = df[(df['Year'] >= min_year) & (df['Year'] <= max_year)]
        result = result.groupby(by=['Genre','Year']).sum()['Global_Sales'].reset_index().sort_values(by='Global_Sales',ascending=False)
        lista = list(result.Genre.unique())
        fig = go.Figure()
        n=0
        for x in lista:
            fig.add_trace(go.Bar(y=result[result['Genre']==x]['Global_Sales'], x= result[result['Genre']==x]['Year'],
                            offsetgroup=n,
                            name=x,
                            text=result[result['Genre']==x]['Global_Sales'].round(2),
                            ))
            n+=1
        fig.update_layout({"paper_bgcolor": "rgba(0, 0, 0, 0)",
                "plot_bgcolor": "rgba(0, 0, 0, 0)"})
        fig.update_layout(title=f"Os gêneros de jogos e quanto estes venderam mundialmente, entre {min_year} e {max_year}")
        fig.update_layout(barmode='group')
        fig.update_yaxes(title="Quantidade de cópias vendidas em milhões")
        fig.show()

tend_jogos(min_year=2007,max_year=2010)

