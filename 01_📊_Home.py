#Importando as bibliotecas
import pandas as pd
import folium
from folium.plugins import MarkerCluster
import json
from PIL import Image
import streamlit as st
from streamlit_folium import st_folium
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
#-----------------------------------------------------------------------------------------------------------------------
st.set_page_config(page_title = 'Home', page_icon = '📊' , layout = 'wide')

#Função para carregar arquivos de dados transformados
@st.cache_data
def load_data(path):
    
    #Carregando arquivo csv - dataframe processado
    df = pd.read_csv(path)

    paises = df[['country', 'color', 'country_classification']].groupby('country').first().reset_index()
    qtd_restaurantes = df[['country', 'restaurant_id']].groupby('country').count().reset_index() #.sort_values('restaurant_id', ascending = False).reset_index()
    
    paises = paises.merge(qtd_restaurantes, on = 'country', how = 'inner')
    
    df1 = pd.DataFrame({'country': list(paises['country']),
                        'latitude': [-25.274398, -14.235004, 56.130366, 55.378051, 20.593684, -0.789275, 
                                     -40.900557, 12.879721, 25.354826, 1.352083, -30.559482, 7.873054, 
                                     38.963745, 23.424076, 37.09024],
                        'longitude': [133.775136,-51.925285, -106.346771, -3.435973, 78.96288, 113.921327, 
                                      174.885971, 121.774017, 51.183884, 103.819836, 22.937506, 80.771797, 
                                      35.243322, 53.847818, -95.712891], 
                        }, 
                      )
    
    df1 = paises.merge(df1, on = 'country')
    df1.columns = ['country', 'color', 'classificação', 'restaurantes', 'latitude', 'longitude']
    
    return df, df1
#-----------------------------------------------------------------------------------------------------------------------
def analysis(df):

    qtd_restaurantes_unicos = df['restaurant_id'].nunique()
    qtd_paises_unicos = df['country'].nunique()
    qtd_cidades_unicas = df['city'].nunique()
    total_avaliacoes = df['votes'].sum()
    total_culinarias = df['cuisines'].nunique()  
    
    return qtd_restaurantes_unicos, qtd_paises_unicos, qtd_cidades_unicas, total_avaliacoes, total_culinarias
#-----------------------------------------------------------------------------------------------------------------------
def load_json(json_files):

    lista_json = []

    for file in json_files:
    
        with open(file, 'r') as f:
    
            country = json.load(f)
            lista_json.append(country)

    return lista_json
#-----------------------------------------------------------------------------------------------------------------------
def create_map(df, df1, lista_json):
  
    #f = folium.Figure(width = 1000, height = 800)
    
    map = folium.Map(location = [df1['longitude'].median(), df1['latitude'].median()], 
                     tiles = 'OpenStreetMap', zoom_start = 1.5,  width = 1000, height = 600 
                     )
    
    for country in lista_json:
    
        folium.GeoJson(country).add_to(map)
    
    marker_cluster = MarkerCluster().add_to(map)
    
    for row, value in df1.iterrows():
        
        folium.Marker(location = (df1.loc[row, 'latitude'], df1.loc[row, 'longitude']), 
                      popup = df1.loc[row, 'country'],
                      icon = folium.Icon(color = df1.loc[row, 'color'])
                     ).add_to(marker_cluster)
    
    restaurantes = pd.concat([df.loc[(df['country'] == 'Australia')&(df['latitude'] < -10), ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                                             'average_cost_for_two', 'cuisines', 'aggregate_rating',
                                                                                             'currency']].head(80), 
                              #1 coordenada na Australia que aparece na Indonesia
                              df.loc[df['country'] == 'Brazil', ['latitude', 'longitude', 'color', 'restaurant_name', 
                                                                 'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80), 
                              #Não tem registros fora do Brasil
                              df.loc[df['country'] == 'Canada', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                 'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não tem registros fora do Canadá
                              df.loc[df['country'] == 'England', ['latitude', 'longitude', 'color', 'restaurant_name', 
                                                                  'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não tem registros fora do Reino Unido
                              df.loc[(df['country'] == 'India')&(df['longitude'] > 10), ['latitude', 'longitude', 'color', 'restaurant_name']].head(80), 
                              #Tem 1 registro fora da Índia
                              df.loc[df['country'] == 'Indonesia', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                    'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não tem registro fora da Indonesia
                              df.loc[df['country'] == 'New Zeland', ['latitude', 'longitude', 'color', 'restaurant_name', 
                                                                     'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não tem regsitros fora da Nova Zelândia
                              df.loc[df['country'] == 'Philippines', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                      'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não tem registros fora das Filipinas
                              df.loc[df['country'] == 'Qatar', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não há registros fora do Qatar
                              df.loc[df['country'] == 'Singapure', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                    'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não há registros fora de Singapure
                              df.loc[(df['country'] == 'South Africa')&(df['latitude'] < -20), ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                                                'average_cost_for_two', 'cuisines', 'aggregate_rating',
                                                                                                'currency']].head(80),
                              #Há 1 registro fora da África do Sul
                              df.loc[df['country'] == 'Sri Lanka', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                    'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não há registro fora
                              df.loc[df['country'] == 'Turkey', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                 'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não há registro fora
                              df.loc[df['country'] == 'United Arab Emirates', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                               'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80),
                              #Não há registro fora
                              df.loc[df['country'] == 'United States of America', ['latitude', 'longitude', 'color', 'restaurant_name',
                                                                                   'average_cost_for_two', 'cuisines', 'aggregate_rating', 'currency']].head(80)
                              #Não há registro fora
                             ])
    
    for row, value in restaurantes.iterrows():
        
        html = '<p><strong> {} </strong></p>'
        html += '<p> Preço médio (US$): {} (moeda local: {})</p>'
        html += '<p> Tipo de cozinha: {} </p>'
        html += '<p>Nota: {} / máximo: 5</p>'
        
        html = html.format(restaurantes.loc[row, 'restaurant_name'], 
                           restaurantes.loc[row, 'average_cost_for_two'].round(decimals = 2),
                           restaurantes.loc[row, 'currency'],
                           restaurantes.loc[row, 'cuisines'],
                           restaurantes.loc[row, 'aggregate_rating']
                          )
        
        popup = folium.Popup(folium.Html(html, script = True), max_width = 500)
        
        folium.Marker(location = (restaurantes.loc[row, 'latitude'], 
                                  restaurantes.loc[row, 'longitude']),
                                  popup = popup,
                      icon = folium.Icon(color = restaurantes.loc[row, 'color'])
                     ).add_to(marker_cluster)

    return map
#-----------------------------------------------------------------------------------------------------------------------
path = './dataset/processed/dataset.csv'
image = './img/logo.png'
foto = './img/foto.jpg'
image = Image.open(image)
foto = Image.open(foto)
json_files = ['./geojson/AUS.json', './geojson/BRA.json', './geojson/CAN.json', './geojson/GBR.json',
              './geojson/IND.json', './geojson/IDN.json', './geojson/NZL.json', './geojson/PHL.json',
              './geojson/QAT.json', './geojson/singapure.json', './geojson/south_africa.json', './geojson/sri_lanka.json',
              './geojson/TUR.json', './geojson/united_arab_emirates.json', './geojson/USA.json'
             ]

df = load_data(path)[0]
df1 = load_data(path)[1]
lista_json = load_json(json_files)
map = create_map(df, df1, lista_json)
results = analysis(df)
#-----------------------------------------------------------------------------------------------------------------------
#Configurando layout na página web com streamlit

#Configurando a página principal
st.markdown("<h1 style='text-align: center; color: black;'>Projeto de Ciência de Dados da empresa Fome Zero</h1>", unsafe_allow_html=True)
st.markdown('--------------------------------------------')
st.markdown("""Este é um projeto de visualização dos principais indicadores da empresa Fome Zero.
O projeto foi criado para que o novo ***Chief Executive Officer*** (CEO) Kleiton Guerra conheça os indicadores da empresa para direcionar as estratégias de sua gestão. 
            """)
st.markdown('--------------------------------------------')
#-----------------------------------------------------------------------------------------------------------------------
#CONFIGURANDO A BARRA LATERAL
#-----------------------------------------------------------------------------------------------------------------------
with st.sidebar:
    st.image(image, width = 120)
    st.markdown('# Fome Zero')
    st.markdown('--------------------------------')
    st.multiselect('Classificação dos países',
                  df['country_classification'].unique(),
                  default = df['country_classification'].unique()[1])
    st.markdown('--------------------------------')
    pais = st.multiselect('Países', 
                   df['country'].unique(), 
                   default = df['country'].unique()[1])
    st.markdown('--------------------------------')
    cidade = st.multiselect('Cidades',
                  df['city'].unique(),
                  default = df['city'].unique()[12])
    st.markdown('--------------------------------')
    
    st.download_button(label = 'Baixe o arquivo de dados (.csv)',
                      data = df.to_csv().encode("utf-8"),
                      file_name = 'dataset.csv',
                      )
    st.markdown('--------------------------------')
    
    with st.container(height = 500):
        
        st.image(foto, width = 100, use_container_width = True)
        st.markdown("<h4 style='text-align: center; color: black;'>Bruno Varella Motta da Costa</h4>", unsafe_allow_html=True)
        st.markdown('### Projeto de conclusão do curso FTC da Comunidade DS') ##Colocar o link

#-----------------------------------------------------------------------------------------------------------------------
#CONFIGURANDO A PÁGINA PRINCIPAL
#-----------------------------------------------------------------------------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

with col1:

    st.metric('Restaurantes Cadastrados', results[0])

with col2:

    st.metric('Países Representados', results[1])

with col3:

    st.metric('Cidades Representadas', results[2])

with col4:

    st.metric('Avaliações totais', results[3])

with col5:

    st.metric('Tipos culinários', results[4])

st.markdown('--------------------------------')

with st.container():

    st.markdown("<h4 style='text-align: center; color: black;'>Mapa com visualização dos 80 primeiros restaurantes nos países onde a Fome Zero opera</h4>",
                unsafe_allow_html=True)
    
    st_folium(map, width = 1024, height = 800)

with st.container():

    st.markdown("<h4 style = 'text-align: center; color: black:'> Dataframe com identificação, classificação e localização central dos países</h4>", 
                unsafe_allow_html=True)
    df2 = df1[['country', 'classificação',  'latitude', 'longitude']]

    st.dataframe(df2)
    

#-----------------------------------------------------------------------------------------------------------------------

