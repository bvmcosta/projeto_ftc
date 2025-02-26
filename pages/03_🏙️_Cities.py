#Importando as bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Cities', page_icon = '🌍' , layout = 'wide')

#Função para carregar arquivos de dados transformados
@st.cache_data
def load_data(path):
    
    #Carregando arquivo csv - dataframe processado
    df = pd.read_csv(path)

    return df
#-----------------------------------------------------------------------------------------------------------------------
def analysis(df):
    
    cidades_pais = df[['city', 'country']].groupby('city').first().reset_index()
    cidades_pais.columns = ['Cidade', 'País']
    grupos_cidades_restaurantes = df[['city', 'restaurant_id']].groupby('city').count().sort_values('restaurant_id', ascending=False).reset_index()
    grupos_cidades_restaurantes.columns = ['Cidade', 'Restaurantes']

    df1 = cidades_pais.merge(grupos_cidades_restaurantes, on = 'Cidade', how = 'inner')
    df1 = df1.sort_values('Restaurantes', ascending=False).reset_index(drop=True)
    df1.columns = ['Cidade', 'País', 'Restaurantes']
    df2 = df1.loc[df1['Restaurantes'] == 80, :].groupby('País').first().reset_index(drop=True)
    df2 = df2.merge(df1, how = 'inner', on = 'Cidade')
    df2 = df2.drop('Restaurantes_y', axis = 1)
    df2.columns = ['Cidade', 'Restaurantes', 'País']

    cidade_avaliacao = df.loc[df['aggregate_rating'] > 4, ['city', 'restaurant_id', 'country']].reset_index(drop=True)
    grupos_cidades = cidade_avaliacao[['city', 'restaurant_id']].groupby(['city']).count().sort_values('restaurant_id', ascending=False).reset_index()
    grupos_cidades.columns = ['Cidade', 'Restaurantes']
    df3 = grupos_cidades.merge(cidades_pais, how = 'inner', on = 'Cidade')

    grupos_cidade_restaurantes_nota_4 = df.loc[df['aggregate_rating'] > 4, ['city', 'restaurant_id']].\
                    groupby(['city']).\
                    count().\
                    sort_values('restaurant_id',ascending=False).\
                    reset_index()

    grupos_cidade_restaurantes_nota_4.columns = ['Cidade', 'Restaurantes']

    df4 = grupos_cidade_restaurantes_nota_4.merge(cidades_pais, how = 'inner', on = 'Cidade')
    df4 = df4.groupby('País').first().sort_values('Restaurantes', ascending=False).reset_index()

    df5 = df[['city', 'cuisines']].groupby(['city'])[['cuisines']].nunique().sort_values('cuisines', ascending=False).reset_index()
    df5.columns = ['Cidade', 'Cozinha']
    df5 = df5.merge(cidades_pais, how = 'inner', on = 'Cidade')

    

    return df1, df2, df3, df4, df5
#-----------------------------------------------------------------------------------------------------------------------
def plotly_barchart(df, df2, df5):

    df = df.head(10)
    df2 = df2.head(10)
    fig1 = px.bar(df, 
                  x = 'Cidade', 
                  y = 'Restaurantes', 
                  color = 'País', 
                  hover_data = ['País', 'Restaurantes'], 
                  width = 1000, 
                  height = 500, 
                  title = 'Top 10 cidades com mais restaurantes (80) em cada país')
    
    fig1.update_layout(
        font=dict(
            family="Times New Roman, monospace",
            size=20,
            color="black"
        )
    )

    fig2 = px.bar(df2, 
                  x = 'Cidade', 
                  y = 'Restaurantes', 
                  color = 'País', 
                  hover_data = ['País', 'Restaurantes'], 
                  width = 1000, 
                  height = 500 
                  )
    
    fig2.update_layout(
        font=dict(
            family="Times New Roman, monospace",
            size=20,
            color="black"
        )
    )

    fig3 = px.bar(df5, 
                  x = 'Cidade', 
                  y = 'Cozinha', 
                  color = 'País', 
                  hover_data = ['Cidade', 'Cozinha'], 
                  width = 1200, 
                  height = 500 
                  )
    
    fig3.update_layout(
        font=dict(
            family="Times New Roman, monospace",
            size=20,
            color="black"
        )
    )

    return fig1, fig2, fig3
#-----------------------------------------------------------------------------------------------------------------------
path = './dataset/processed/dataset.csv'
df = load_data(path)
df1 = analysis(df)[0]
df2 = analysis(df)[1]
df3 = analysis(df)[2]
df4 = analysis(df)[3]
df5 = analysis(df)[4]

fig1 = plotly_barchart(df2, df4, df5)[0]
fig2 = plotly_barchart(df2, df4, df5)[1]
fig3 = plotly_barchart(df2, df4, df5)[2]

#-----------------------------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Visão Cidades</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([0.7, 0.3], vertical_alignment="center")
with col1:
    
    st.plotly_chart(fig1, user_container_width=True)

with col2:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Cidades Cadastradas</h5>", unsafe_allow_html=True)
    st.write(df1)
#-----------------------------------------------------------------------------------------------------------------------
col1, col2 = st.columns([0.7, 0.3], vertical_alignment="center")

with col1:
    
    st.markdown("<h5 style='text-align: center; color: black;'>Top 10 cidades com restaurantes bem avaliados (nota > 4)</h5>", unsafe_allow_html=True)
    st.plotly_chart(fig2)
    
with col2:

    st.markdown("<h5 style='text-align: center; color: black;'>Quantidade de restaurantes mais bem avaliados (nota > 4)</h5>", unsafe_allow_html=True)
    st.dataframe(df4)
#-----------------------------------------------------------------------------------------------------------------------
with st.container():

    st.markdown("<h3 style='text-align: center; color: black;'>Tipos distintos de culinária por cidade e país</h3>", unsafe_allow_html=True)
    st.plotly_chart(fig3, user_container_width = True)

 
   


    









