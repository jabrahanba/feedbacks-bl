#Librerias y frameworks
import pandas as pd
import streamlit as st
import etl_function as etl
from datetime import date, timedelta

st.set_page_config(
     page_title="Feedback 💻",
     page_icon= "icon.png",
     layout="wide")


st.title('Baselang')
st.markdown('## Transformación de datos para feedback')

st.markdown('***')

df_transformed = pd.DataFrame()

# Agregar un control para cargar el archivo CSV
uploaded_file = st.file_uploader('# 🅰️ - Cargar el archivo descargado del back end', type=['csv'])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        st.write("Archivo subido con éxito ✅")
    except Exception as e:
        st.warning("""
            ⚠️Archivo no válido.⚠️
            Elimine el archivo cargado dando clic ❌ al lado del nombre del archivo que acaba de subir
            (Esto lo encontrará encima de este mensaje). Luego,
            cargue el archivo original extraído del back end
            """)
            #st.error(str(e))

date_option = st.radio("## 🅱️ - Seleccione la fecha:", ("Ayer", "Seleccionar fecha diferente" ))
if date_option == "Seleccionar fecha":
    selected_date = st.date_input("Seleccione una fecha en formato AAAA-MM-DD")
else:
    # Obtener la fecha de ayer
    selected_date = date.today() - timedelta(days=1)

process_button = st.button("Procesar >>")

if process_button:
    if uploaded_file:
        try:
            df_transformed = etl.etl(df, selected_date)
            st.write("Archivo procesado con éxito ✅")
            st.markdown("Visualización previa, proceda a descargar:")
            st.dataframe(df_transformed)
            csv_file = df_transformed.to_csv(sep=';',encoding='utf-8', index=False)
            st.download_button(
                label='Descargar archivo transformado',
                data=csv_file,
                file_name= f'data_{selected_date}.csv',
                mime='text/csv')
        except Exception as e:
            st.warning("""
                        ⚠️Archivo no válido.⚠️
                        Elimine el archivo cargado dando clic en la equis al lado del nombre del archivo que acaba de subir
                        (Esto lo encontrará encima de este mensaje). Luego,
                        cargue el archivo original extraído del back end
                        """)
            #st.error(str(e))
        
    elif uploaded_file is None:
        st.warning("Por favor debe insertar el archivo con los datos")


## SIDEBAR:
st.sidebar.markdown('''
#### Instrucciones:

Descargue el archivo en el backend de Baselang:
1. Ingrese en la opción "Reponses for teacher".
2. Luego, vaya a la sección "Export feedback for teacher".
3. Cargue el archivo como se pide a continuación. 👉
''')


