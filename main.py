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
    # Añadir más años según sea necesario
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

# Selector de variable de interés
if st.session_state.data:
    # Asumiendo que todas las tablas tienen las mismas columnas, puedes usar las de cualquier año
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
