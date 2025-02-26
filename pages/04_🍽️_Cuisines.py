#Caminho da pasta para mudar no terminal: cd C:/Users/Bruno/repos/matricula_2024/3_FTC/projeto_aluno

#Importando as bibliotecas
import pandas as pd
import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
#-----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Cities', page_icon = '🍽️' , layout = 'wide')

#Função para carregar arquivos de dados transformados
@st.cache_data
def load_data(path):
    
    #Carregando arquivo csv - dataframe processado
    df = pd.read_csv(path)

    return df
#-----------------------------------------------------------------------------------------------------------------------
def analysis_pais(df, pais):

    df1 = df.loc[df['country'] == pais[0], :]

    return df1
#-----------------------------------------------------------------------------------------------------------------------
def analysis_cidade(df, cidade):

    df2 = df.loc[df['city'] == cidade[0], :]

    df3 = df2[['cuisines', 'aggregate_rating']].groupby('cuisines').mean().round(decimals = 2).reset_index()
    df3.columns = ['cuisines', 'mean_aggregate_rating']

    return df2, df3
#-----------------------------------------------------------------------------------------------------------------------
def analysis_tipo_culinario(df, tipo_culinario):

    df4 = df.loc[df['cuisines'] == tipo_culinario[0], ['restaurant_name', 'address', 'locality', 'locality_verbose', 'average_cost_for_two', 'currency', 
                                                      'has_table_booking', 'has_online_delivery', 'is_delivering_now', 'switch_to_order_menu', 'price_range', 
                                                      'aggregate_rating', 'longitude', 'latitude', 'color', 'country']].reset_index(drop=True)
    df4['reserva_mesa'] = df4['has_table_booking'].apply(lambda x: 'Sim' if x == 1 else 'Não')
    df4['entrega_online'] = df4['has_online_delivery'].apply(lambda x: 'Sim' if x == 1 else 'Não')
    df4['entrega_hoje'] = df4['is_delivering_now'].apply(lambda x: 'Sim' if x == 1 else 'Não')
    
    return df4
#-----------------------------------------------------------------------------------------------------------------------
def create_map(df):
    
    map = folium.Map(location = [df['longitude'].median(), df['latitude'].median()], 
                     tiles = 'OpenStreetMap', zoom_start = 1.5,  width = 1000, height = 600 
                     )
    
    marker_cluster = MarkerCluster().add_to(map)

    for row, value in df.iterrows():
         
        folium.Marker(location = (df.loc[row, 'latitude'], df.loc[row, 'longitude']), 
                      popup = df.loc[row, 'country'],
                      icon = folium.Icon(color = df.loc[row, 'color'])
                     ).add_to(marker_cluster)
    return map
#-----------------------------------------------------------------------------------------------------------------------
path = './dataset/processed/dataset.csv'
df = load_data(path)
#-----------------------------------------------------------------------------------------------------------------------
# CONFIGURANDO BARRA LATERAL
#-----------------------------------------------------------------------------------------------------------------------
with st.sidebar:

    pais = st.multiselect('Escolha o país', 
                  options = df['country'].unique(),
                  default = 'Brazil',
                  max_selections = 1)
#-----------------------------------------------------------------------------------------------------------------------
df1 = analysis_pais(df, pais)
#-----------------------------------------------------------------------------------------------------------------------
# CONFIGURANDO BARRA LATERAL
#-----------------------------------------------------------------------------------------------------------------------
with st.sidebar:

    cidade = st.multiselect('Escolha a cidade', 
                  options = df1['city'].unique(),
                  default = df1['city'].unique()[0],
                  max_selections = 1)
#-----------------------------------------------------------------------------------------------------------------------
df2 = analysis_cidade(df1, cidade)[0]
df3 = analysis_cidade(df1, cidade)[1]
#-----------------------------------------------------------------------------------------------------------------------
# CONFIGURANDO BARRA LATERAL
#-----------------------------------------------------------------------------------------------------------------------
with st.sidebar:

    tipo_culinario = st.multiselect('Escolha o tipo culinário', 
                  options = sorted(df2['cuisines'].unique()),
                  default = sorted(df2['cuisines'].unique())[0],
                  max_selections = 1)
#-----------------------------------------------------------------------------------------------------------------------
df3 = df3.loc[df3['cuisines'] == tipo_culinario[0], :]
df4 = analysis_tipo_culinario(df2, tipo_culinario)
#-----------------------------------------------------------------------------------------------------------------------
# CONFIGURANDO BARRA LATERAL
#-----------------------------------------------------------------------------------------------------------------------
with st.sidebar:

    restaurante = st.multiselect('Escolha o restaurante', 
                  options = sorted(df4['restaurant_name'].unique()),
                  default = sorted(df4['restaurant_name'].unique())[0],
                  max_selections = 1)
#-----------------------------------------------------------------------------------------------------------------------
st.markdown("<h1 style='text-align: center; color: black;'>Visualização do Restaurante Desejado</h1>", unsafe_allow_html=True)

df4 = df4.loc[df4['restaurant_name'] == restaurante[0], :]

col1, col2, col3 = st.columns([0.5, 0.2, 0.3], vertical_alignment = 'center', )

with col1:
    
    st.metric('Restaurante', value = restaurante[0], border = True)

with col2:

    
    st.metric('Lojas', value = df4['restaurant_name'].count(), border = True)

with col3:

    st.metric('Nota Restaurate / Avaliação Média', value = f'{df4.iloc[0,11]} / {df3.iloc[0,1]}', border = True)

col4, col5, col6 = st.columns([0.5, 0.2, 0.3], vertical_alignment = 'center', )

with col4:

    st.metric('Reserva de Mesa',
             value = df4.iloc[0,-3],
             border = True)

with col5:

    st.metric('Pedido por aplicativo',
             value = df4.iloc[0,-2],
             border = True)

with col6:

    st.metric('Está entregando',
             value = df4.iloc[0,-1],
             border = True)
#-----------------------------------------------------------------------------------------------------------------------
map = create_map(df4)
#-----------------------------------------------------------------------------------------------------------------------

with st.container():

    st.markdown("<h4 style='text-align: center; color: black;'>Mapa com visualização do restaurante desejado</h4>",
                unsafe_allow_html=True)

    st_folium(map, width = 1024, height = 800)


    












