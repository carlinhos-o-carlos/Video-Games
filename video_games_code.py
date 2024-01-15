import pandas as pd
import datetime as dt
import plotly.graph_objects as go

df =pd.read_csv("vgsales.csv")

#Funçao para obter o top 10 jogos que venderam no ano (determinado pelo usuario, ano padrão 2020)
def top_10_year(df=df,year=2020,padrao=True):
    result = df[df['Year'] == year].reset_index()
    if padrao:
        result = result.iloc[:,2:7]
        return result.head(10)
    else:
        result = result[['Name','Year','Genre','Publisher']]
        return result.head(10)

top_10_year(year=2000)

#Genero que mais vendeu ao longo dos anos em um grafico
df_graph = df.groupby(by=['Genre']).sum()['Global_Sales'].reset_index().sort_values(by='Global_Sales',ascending=False)

fig = go.Figure()
fig.add_trace(go.Bar(x=df_graph['Global_Sales'], y= df_graph['Genre'],
                marker_color='rgb(26, 118, 255)',
                text=df_graph['Global_Sales'],
                hoverinfo='none',
                orientation='h'))
fig.update_layout({"paper_bgcolor": "rgba(0, 0, 0, 0)",
        "plot_bgcolor": "rgba(0, 0, 0, 0)"})
fig.update_layout(yaxis=dict(type='category',autorange="reversed"))
fig.update_xaxes(visible=False, showticklabels=False)
fig.show()

#Quais são os rankings de jogos mais vendidos quando não consideramos a plataforma 
df_games = df.copy()
df_games= df_games.drop(columns=['Platform','Rank'])
df_games_sales = df_games.groupby(by=['Name','Year','Genre','Publisher']).sum().reset_index().sort_values(by='Global_Sales',ascending=False)
#df_games_sales['rank'] = df_games_sales['Global_Sales'].rank(ascending=False)
df_games_sales.head(10)

#Top 10 jogos que venderam no ano de 2000 sem considerar a plataforma.
top_10_year(df=df_games_sales,year=2000,padrao=False)
