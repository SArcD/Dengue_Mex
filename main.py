import pandas as pd

# Definir los años disponibles para los archivos
años = ['2017', '2018', '2019']

# URL base donde están alojados los archivos en GitHub
# Asegúrate de reemplazar los segmentos necesarios para adaptarlo a los diferentes años.
url_base = 'https://github.com/SArcD/Dengue_Mex/blob/9f745cc171fc6ba519c276a129b60c51028b482e/Dengue_{}.xlsx?raw=true'

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
