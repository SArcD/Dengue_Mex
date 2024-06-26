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


    # Permitir al usuario seleccionar las columnas para el histograma
    columnas_seleccionadas = st.multiselect('Seleccione las columnas para el histograma:', df.columns)

    # Deslizador para definir el tamaño de los bins
    num_bins = st.slider('Seleccione el número de bins para el histograma:', min_value=1, max_value=50, value=10)

    # Botón para generar el histograma
    if st.button('Generar Histograma'):
        fig, ax = plt.subplots()
        for col in columnas_seleccionadas:
            ax.hist(df[col].dropna(), bins=num_bins, alpha=0.5, label=col)
        ax.set_title('Histograma')
        ax.set_xlabel('Valor')
        ax.set_ylabel('Frecuencia')
        ax.legend()
        st.pyplot(fig)
