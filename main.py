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
}

# Crear un selector en la barra lateral para elegir el año
año_seleccionado = st.sidebar.selectbox('Seleccione el año:', list(archivos.keys()))

# Función para cargar los datos desde GitHub
def cargar_datos(url):
    response = requests.get(url)
    if response.status_code == 200:
        excel_data = BytesIO(response.content)
        df = pd.read_excel(excel_data, engine='openpyxl')
        return df
    else:
        st.error("Error al cargar el archivo: HTTP Status " + str(response.status_code))
        return None

# Verificar si el DataFrame ya está cargado en el estado de la sesión
if 'df' not in st.session_state or st.sidebar.button('Cargar Datos'):
    st.session_state.df = cargar_datos(archivos[año_seleccionado])

if st.session_state.df is not None:
    st.write(f"Datos para el año {año_seleccionado}:")
    st.dataframe(st.session_state.df)

    # Mostrar las dimensiones del DataFrame
    filas, columnas = st.session_state.df.shape
    st.text(f"El DataFrame tiene {filas} filas y {columnas} columnas.")

    # Mostrar un resumen estadístico del DataFrame
    if st.button('Mostrar resumen estadístico'):
        st.write('Resumen Estadístico:')
        st.dataframe(st.session_state.df.describe())
    
    # Permitir al usuario seleccionar las columnas para el histograma
    columnas_seleccionadas = st.multiselect('Seleccione las columnas para el histograma:', st.session_state.df.columns)

    # Deslizador para definir el tamaño de los bins
    num_bins = st.slider('Seleccione el número de bins para el histograma:', min_value=1, max_value=50, value=10)

    # Generar histograma si hay columnas seleccionadas
    if columnas_seleccionadas:
        fig, axs = plt.subplots(len(columnas_seleccionadas), figsize=(10, 5 * len(columnas_seleccionadas)))
        if len(columnas_seleccionadas) == 1:  # Cuando solo hay una columna seleccionada, axs no es una lista
            axs = [axs]
        for ax, col in zip(axs, columnas_seleccionadas):
            ax.hist(st.session_state.df[col].dropna(), bins=num_bins, alpha=0.7, label=f'Histograma de {col}')
            ax.set_title(f'Histograma de {col}')
            ax.set_xlabel('Valores')
            ax.set_ylabel('Frecuencia')
            ax.legend()
        st.pyplot(fig)
