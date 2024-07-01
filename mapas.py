import streamlit as st
import geopandas as gpd
import pandas as pd
import fiona
from fiona.drvsupport import supported_drivers
import folium
from folium import Map, FeatureGroup, Marker, LayerControl, Popup
from streamlit_folium import folium_static
from folium import Choropleth, GeoJson, plugins
from folium import GeoJson
from branca.element import MacroElement
from jinja2 import Template
import branca
from shapely.ops import unary_union
import os


# Leitura e processamento dos dados


path_resultados = "C:/GIT/ted_aneel/Mapas BDGD/resultados/"
#alimentadores_validados = alim_validados(path_alimentadores_validados)

@st.cache_data
def load_ucbt():
    resultados_ucbt = pd.read_pickle(path_resultados + 'ucbt.pkl')
    return resultados_ucbt

@st.cache_data
def load_ugbt():
    resultados_ugbt = pd.read_pickle(path_resultados + 'ugbt.pkl')
    return resultados_ugbt


@st.cache_data
def load_ucmt():
    resultados_ucmt = pd.read_pickle(path_resultados + 'ucMt.pkl')
    return resultados_ucmt

@st.cache_data
def load_ucmt():
    resultados_ugmt = pd.read_pickle(path_resultados + 'ugmt.pkl')
    return resultados_ugmt


# Mapas
basemaps = {
    'Google Maps': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Maps'
    ),
    'Google Satellite': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite'
    ),
    'Google Terrain': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=p&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Terrain'
    ),
    'Google Satellite Hybrid': folium.TileLayer(
        tiles='https://mt1.google.com/vt/lyrs=y&x={x}&y={y}&z={z}',
        attr='Google',
        name='Google Satellite'
    ),
    'Esri Satellite': folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri',
        name='Esri Satellite'
    ),
    'CartoDB positron': folium.TileLayer(
        tiles='CartoDB positron',
        attr='CartoDB',
        name='Light Map'
    )
}


# Setando pagina do stream lit

st.set_page_config(layout="wide")#, page_icon = "D:/2023_Light_Dash/logo.png")

# Titulo heade
#


st.header('TED ANEEL-  BDGD',divider='gray')
st.subheader('MAPAS', divider='gray')

# Carrega os dados
# resultados_ucbt = load_ucbt()
resultados_ucmt = load_ucmt()
resultados_ugbt = load_ugbt()
resultados_ucmt = load_ucmt()

# ucbt = st.selectbox(
#             'UCBT',
#             resultados_ucbt['COD_ID'].unique()
#             )
        
       
# ucbt = [ucbt] if isinstance(ucbt, str) else ucbt

# regiao_df = resultados_ucbt[resultados_ucbt['COD_ID'].isin(ucbt)]

ucmt = st.selectbox(
            'UCMT',
            resultados_ucmt['COD_ID'].unique()
            )
        
       
ucmt = [ucmt] if isinstance(ucmt, str) else ucmt

regiao_df = resultados_ucmt[resultados_ucmt['COD_ID'].isin(ucmt)]

# alim_regional = regiao_df['ALIMENTADOR'].unique()

# status = st.selectbox(
#     'Status',
#     (regiao_df['Macro-Status'].unique()),
#     index=None,
#     placeholder="Selecione Status ..."
#     )
# status = [status] if isinstance(status, str) else status
# if status != "Selecione Status ..." and isinstance(status, list):
    
#     regiao_df = regiao_df[regiao_df['Macro-Status'].isin(status)]
#     # Verifica se o DataFrame resultante está vazio

    
    
# alimentadores = st.selectbox(
#     'Linha',
#     (regiao_df['ALIMENTADOR'].unique()),
#     index=None,
#     placeholder="Selecione a linha ..."
#     )

# alimentadores = [alimentadores] if isinstance(alimentadores, str) else alimentadores
# #     # Verifica se a opção selecionada não é o placeholder antes de aplicar o filtro
# #    # Verifica se a opção selecionada não é o placeholder e se é uma lista antes de aplicar o filtro
# if alimentadores != 'Selecione a linha ...' and isinstance(alimentadores, list):
#     regiao_df = regiao_df[regiao_df['ALIMENTADOR'].isin(alimentadores)]


# Centroides Localidades
centroide = regiao_df.to_crs(22182).centroid.to_crs(4326).iloc[[0]]

# Criar o mapa folium
mapa = folium.Map(location=[centroide.y, centroide.x], zoom_start=13)

# Adicionar basemaps ao mapa usando um loop
for name, tile_layer in basemaps.items():
    tile_layer.add_to(mapa)



# Add the legend HTML to the map
    macro = branca.element.MacroElement()
    # macro._template = branca.element.Template(legend_html)
    mapa.add_child(macro)
    
        
        
    # Adicionar GeoJson ao mapa com base na nova coluna de cor
    GeoJson(regiao_df, style_function=lambda feature: {'color': 'blue', 'weight': 2}).add_to(mapa)
    #GeoJson(regiao_df_ucmt, style_function=lambda feature: {'color': 'blue', 'weight': 2}).add_to(mapa)


# Adicionar controle de camadas
    folium.LayerControl().add_to(mapa)

    # Adicionar controle de tela cheia
    plugins.Fullscreen().add_to(mapa)

    

    # Exibir mapa 
    folium_static(mapa, width=1200, height=500)

    




    if st.button("Baixar Mapa como HTML"):
        # Caixa de texto para inserir o caminho
        caminho_salvar = st.text_input("Arquivo:", value= ucmt[0] + ".html")

        if caminho_salvar:
            # Adicionar o arquivo temporário para download
            st.download_button(
                label="Clique para baixar",
                data=mapa.get_root().render(),
                file_name=os.path.join(caminho_salvar),
                key="download_mapa_html"
            )

