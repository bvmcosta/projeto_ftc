#Importando as bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
#-----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Countries', page_icon = '🌍' , layout = 'wide')

#Função para carregar arquivos de dados transformados
@st.cache_data
def load_data(path):
    
    #Carregando arquivo csv - dataframe processado
    df = pd.read_csv(path)

    return df
#-----------------------------------------------------------------------------------------------------------------------
def analysis(df):

    paises_classificacao = df[['country', 'country_classification']].groupby('country').first().reset_index()

    grupos_paises_cidades = df[['country', 'city']].groupby('country')['city'].nunique().reset_index()

    grupos_paises_restaurantes = df[['country', 'restaurant_id']].groupby('country').count().sort_values('restaurant_id', ascending=False).reset_index()

    avaliacoes_pais = df[['country', 'votes']].groupby('country').sum().reset_index()
    
    df1 = paises_classificacao.merge(grupos_paises_cidades, on = 'country', how = 'inner')

    df1 = df1.merge(grupos_paises_restaurantes, on = 'country', how = 'inner')

    df1 = df1.merge(avaliacoes_pais, on = 'country', how = 'inner')

    df1.columns = ['País', 'Classificação Econômica', 'Cidades', 'Restaurantes', 'Avaliações']

    df_aux = df.loc[(df['average_cost_for_two'] > 0)&(df['average_cost_for_two'] != 15565010.5842), ['country', 
                                                                                                     'country_classification', 
                                                                                                     'average_cost_for_two']]

    categories = list(df_aux['country_classification'].unique())
    df_aux['country_classification'] = pd.Categorical(df_aux['country_classification'], categories = categories, ordered = True)
    df_aux = df_aux.sort_values('country_classification')

    return df1, df_aux
#-----------------------------------------------------------------------------------------------------------------------
def plotly_barchart(df):
    
    df = df.sort_values('Restaurantes', ascending=False)
    fig1 = px.bar(df, 
                  x = 'País', 
                  y = 'Restaurantes', 
                  color = 'Classificação Econômica', 
                  hover_data = ['País', 'Restaurantes'], 
                  width = 1000, 
                  height = 400, 
                  title = 'Quantidade de restaurantes por país')

    fig1.update_layout(
        font_family="Times New Roman",
        font_color="black",
        title_font_family="Times New Roman",
        title_font_color="black",
        legend_title_font_color="black"
    )
    
    fig1.update_layout(
        xaxis=dict(
            title=dict(
                text="País"
            )
        ),
        yaxis=dict(
            title=dict(
                text= 'Quantidade de Restaurantes'
            )
        ),
        legend=dict(
            title=dict(
                text="Classificação Econômica"
            )
        ),
        font=dict(
            family="Times New Roman, monospace",
            size=14,
            color="black"
        )
    )
    
    df = df.sort_values('Cidades', ascending=False)
    fig2 = px.bar(df, 
                  x = 'País', 
                  y = 'Cidades', 
                  color = 'Classificação Econômica', 
                  hover_data = ['País', 'Cidades'], 
                  width = 1000, 
                  height = 400, 
                  title = 'Quantidade de cidades')

    fig2.update_layout(
        xaxis=dict(
            title=dict(
                text="País"
            )
        ),
        yaxis=dict(
            title=dict(
                text= 'Quantidade de cidades'
            )
        ),
        legend=dict(
            title=dict(
                text="Classificação Econômica"
            )
        ),
        font=dict(
            family="Times New Roman, monospace",
            size=14,
            color="black"
        )
    )

    fig3 = px.bar(df, 
                  x = 'País', 
                  y = 'Avaliações', 
                  color = 'Classificação Econômica', 
                  hover_data = ['País', 'Avaliações'], 
                  width = 1000, 
                  height = 400, 
                  title = 'Quantidade de Avaliações')

    fig3.update_layout(
            xaxis=dict(
                title=dict(
                    text="País"
                )
            ),
            yaxis=dict(
                title=dict(
                    text= 'Quantidade de Avaliações'
                )
            ),
            legend=dict(
                title=dict(
                    text="Classificação Econômica"
                )
            ),
            font=dict(
                family="Times New Roman, monospace",
                size=14,
                color="black"
            )
        )
    
    return fig1, fig2, fig3
#-----------------------------------------------------------------------------------------------------------------------
def boxplot(df):
    
    fig4, axs = plt.subplots(1, 2, figsize = (12, 4), gridspec_kw = dict(width_ratios = [6, 4]))
    sns.boxplot(data = df, x = df['country'], y = df['average_cost_for_two'], hue = 'country_classification', log_scale = True, orient = 'v', ax = axs[0])
    axs[0].set_xticklabels(labels = ['Philippines', 'India', 'Indonesia', 'South Africa', 'Brazil', 'Turkey', 'Sri Lanka', 'Singapure', 'England',
                                     'United States of America', 'New Zeland', 'United Arab Emirates', 'Qatar', 'Canada', 'Australia'], 
                           rotation=90)
    sns.boxplot(data = df, x = df['country_classification'], y = df['average_cost_for_two'], 
                hue = 'country_classification', 
                log_scale = True, orient = 'v', 
                ax = axs[1])
    axs[1].set_xticklabels(labels = ['lower_middle', 'upper_middle', 'high'], rotation = 90)
    axs[0].set_ylabel('Preço médio (US$) de prato para 2', fontsize = 11)
    axs[0].set_xlabel('País', fontsize = 11)
    axs[0].legend(title = 'Classificação Econômica', fontsize = 11)
    
    axs[1].set_ylabel('Preço médio (US$) de prato para 2', fontsize = 11)
    

    return fig4
#-----------------------------------------------------------------------------------------------------------------------
def filtrar_pais(df, pais):

    df4 = df.loc[df['country'] == pais[0], :]

    qtd_cidades_restaurantes = df4[['city', 'restaurant_id']].groupby('city').count().sort_values('city', ascending=False).reset_index()
    qtd_cidades_restaurantes.columns = ['Cidades', 'Restaurantes']

    fig5 = px.bar(qtd_cidades_restaurantes, 
                  x = 'Cidades', 
                  y = 'Restaurantes', 
                  hover_data = ['Cidades', 'Restaurantes'], 
                  width = 1000, 
                  height = 400, 
                  title = 'Quantidade de restaurantes por cidade')

   
    fig6, ax = plt.subplots(figsize = (6, 4))
    ax.set_title('Variação no preço de prato para 2 em cada cidade', fontsize = 10)
    sns.boxplot(data = df4, x = df4['city'], y = df4['average_cost_for_two'],
                log_scale = True, orient = 'v', 
                ax = ax)

    ax.set_xticklabels(labels = df4['city'].unique(), rotation = 90)
    ax.set_ylabel('Preço médio (US$) de prato para 2', fontsize = 11)
    ax.set_xlabel('Cidades', fontsize = 11)
    
    
    
    return fig5, fig6
#-----------------------------------------------------------------------------------------------------------------------
path = './dataset/processed/dataset.csv'

df = load_data(path)
df1 = analysis(df)[0]
df2 = analysis(df)[1]

fig1 = plotly_barchart(df1)[0]
fig2 = plotly_barchart(df1)[1]
fig3 = plotly_barchart(df1)[2]
fig4 = boxplot(df2)
#-----------------------------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Visão Países</h1>", unsafe_allow_html=True)

with st.container():
    
    st.plotly_chart(fig1, use_container_width = True)

with st.container():
    
    st.plotly_chart(fig2, use_container_width = True)

with st.container():

    st.plotly_chart(fig3, use_container_width = True)

with st.container():
    
    st.markdown("<h4 style='text-align: center; color: black;'>Variação do preço médio (US$) dos pratos por país segundo classificação econômica</h4>",
                unsafe_allow_html=True)
    
    st.markdown("<h6 style='text-align: center; color: black;'>(Foram excluídos valores iguais a 0 e o outlier muito alto [US$ 15565010.58 (cidade de Adelaide - Austrália)])</h6>",
                unsafe_allow_html=True)
    
    st.pyplot(fig4, use_container_width=True)

#-----------------------------------------------------------------------------------------------------------------------
# CONFIGURANDO BARRA LATERAL
#-----------------------------------------------------------------------------------------------------------------------
with st.sidebar:

    st.markdown('# Filtros')
    st.text("Filtro para selecionar o país e, posteriormente, avaliar a distribuição na quantidade de restaurantes e no preço médio do prato para 2 entre as cidades")
    pais = st.multiselect('Selecione o país', 
                   options = df2['country'].unique(), 
                   default = 'Brazil',
                   max_selections = 1)
#-----------------------------------------------------------------------------------------------------------------------
#Filtrando as linhas por país selecionado
fig5 = filtrar_pais(df, pais)[0]
fig6 = filtrar_pais(df, pais)[1]
#-----------------------------------------------------------------------------------------------------------------------
st.markdown("<h4 style='text-align: center; color: black;'>Variação entre as cidades do país selecionado</h4>",
                unsafe_allow_html=True)

st.plotly_chart(fig5)
st.pyplot(fig6)



            




