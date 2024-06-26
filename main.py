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


    # Cargar todos los DataFrames una vez y almacenarlos en el estado de sesión
    if 'data' not in st.session_state:
        st.session_state.data = {year: cargar_datos(url) for year, url in archivos.items()}

    # Selección de un valor específico de la columna 'Estado'
    if 'Estado' in st.session_state.df.columns:
        estados_disponibles = st.session_state.df['Estado'].unique()
        estado_seleccionado = st.selectbox('Seleccione un Estado:', estados_disponibles)
        
        # Mostrar la fila correspondiente al Estado seleccionado
        fila_seleccionada = st.session_state.df[st.session_state.df['Estado'] == estado_seleccionado]
        st.write('Fila seleccionada:')
        st.dataframe(fila_seleccionada)
        
    # Mostrar los datos de cada año para el estado seleccionado
    for year, df in st.session_state.data.items():
        if not df.empty:
            st.write(f"Datos para el año {year}:")
            fila_seleccionada = df[df['Estado'] == estado_seleccionado]
            if not fila_seleccionada.empty:
                st.dataframe(fila_seleccionada)
            else:
                st.write(f"No hay datos para {estado_seleccionado} en {year}.")
    
    variables_disponibles = list(st.session_state.data[next(iter(st.session_state.data))].columns)
    variable_seleccionada = st.sidebar.selectbox('Seleccione la variable de interés:', variables_disponibles)

    # Crear un DataFrame para almacenar los datos de la variable seleccionada a través de los años
    valores_por_año = []

    for year, df in st.session_state.data.items():
        if not df.empty and variable_seleccionada in df.columns:
            valor = df.loc[df['Estado'] == estado_seleccionado, variable_seleccionada]
            if not valor.empty:
                valores_por_año.append((year, valor.values[0]))
            else:
                valores_por_año.append((year, None))

    valores_df = pd.DataFrame(valores_por_año, columns=['Año', variable_seleccionada])
    st.write(f"Valores de '{variable_seleccionada}' para {estado_seleccionado} a lo largo de los años:")
    st.dataframe(valores_df.set_index('Año'))

    # Histograma de la variable a lo largo de los años
    fig, ax = plt.subplots()
    ax.hist(valores_df[variable_seleccionada].dropna(), bins=10, alpha=0.75)
    ax.set_title(f'Histograma de {variable_seleccionada}')
    ax.set_xlabel('Valores')
    ax.set_ylabel('Frecuencia')
    st.pyplot(fig)

    # Verificar si hay datos para mostrar
    if any(len(data) > 0 for data in valores_por_año.values()):
        # Crear el gráfico de cajas
        fig, ax = plt.subplots()
        ax.boxplot([data for data in valores_por_año.values() if len(data) > 0], labels=[year for year, data in valores_por_año.items() if len(data) > 0])
        ax.set_title(f'Gráfico de caja de {variable_seleccionada} por año para {estado_seleccionado}')
        ax.set_ylabel(variable_seleccionada)
        ax.set_xlabel('Año')
        st.pyplot(fig)
    else:
        st.write("No hay datos suficientes para mostrar el gráfico de cajas.")



