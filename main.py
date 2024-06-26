import streamlit as st
import pandas as pd

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

# Crear un selector en la barra lateral para elegir el año
año_seleccionado = st.sidebar.selectbox('Seleccione el año:', list(archivos.keys()))

# Función para cargar los datos desde GitHub
def cargar_datos(url):
    df = pd.read_excel(url, engine='openpyxl')
    return df

# Botón para cargar los datos
if st.sidebar.button('Cargar Datos'):
    df = cargar_datos(archivos[año_seleccionado])
    st.write(f"Datos para el año {año_seleccionado}:")
    st.dataframe(df)

    # Mostrar las dimensiones del DataFrame
    filas, columnas = df.shape
    st.text(f"El DataFrame tiene {filas} filas y {columnas} columnas.")
