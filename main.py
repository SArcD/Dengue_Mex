import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
from io import BytesIO

# Definir los años disponibles para los archivos y sus URLs correspondientes
archivos = {
    '2017': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2017.xlsx?raw=true',
    '2018': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2018.xlsx?raw=true',
    '2019': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2019.xlsx?raw=true',
    '2020': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2020.xlsx?raw=true',
    '2021': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2021.xlsx?raw=true',
    '2022': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2022.xlsx?raw=true',
    '2023': 'https://github.com/SArcD/Dengue_Mex/blob/5211982d4dbea53b2d6a6e4ccee5e06fa1717d1f/Dengue_2023.xlsx?raw=true'
}

def cargar_datos(url):
    response = requests.get(url)
    if response.status_code == 200:
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, engine='openpyxl')
        return df
    else:
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

# Cargar todos los DataFrames una vez y almacenarlos en el estado de sesión
if 'data' not in st.session_state:
    st.session_state.data = {year: cargar_datos(url) for year, url in archivos.items()}

# Selector de estado
estado_seleccionado = st.sidebar.selectbox('Seleccione un Estado:', pd.concat(st.session_state.data.values())['Estado'].unique())

# Mostrar los datos de cada año para el estado seleccionado
for year, df in st.session_state.data.items():
    if not df.empty:
        st.write(f"Datos para el año {year}:")
        fila_seleccionada = df[df['Estado'] == estado_seleccionado]
        if not fila_seleccionada.empty:
            st.dataframe(fila_seleccionada)
        else:
            st.write(f"No hay datos para {estado_seleccionado} en {year}.")
