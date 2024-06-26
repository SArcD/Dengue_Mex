import streamlit as st
import pandas as pd

# Definir los años disponibles para los archivos
años = ['2017', '2018', '2019']

# URL base donde están alojados los archivos en GitHub
url_base = 'https://github.com/username/repo/blob/main/path/to/your/Dengue_{}.xlsx?raw=true'

# Crear un selector en la barra lateral para elegir el año
año_seleccionado = st.sidebar.selectbox('Seleccione el año:', años)

# Función para cargar los datos desde GitHub
def cargar_datos(año):
    url = url_base.format(año)
    df = pd.read_excel(url, engine='openpyxl')
    return df

# Botón para cargar los datos
if st.sidebar.button('Cargar Datos'):
    df = cargar_datos(año_seleccionado)
    st.write(f"Datos para el año {año_seleccionado}:")
    st.dataframe(df)

# Puedes también mostrar los datos directamente sin necesidad de un botón
# df = cargar_datos(año_seleccionado)
# st.write(f"Datos para el año {año_seleccionado}:")
# st.dataframe(df)

