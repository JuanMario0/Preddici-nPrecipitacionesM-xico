import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px

# Configuración básica
st.set_page_config(layout="wide")

# Cargar datos
try:
    df_predicciones = pd.read_csv("predicciones_precipitacionV2.csv")
    mexico = gpd.read_file("mexicoHigh.json")
    
    # Verificar que los datos se cargaron correctamente
    st.write("Datos cargados correctamente")
    st.write(f"Número de registros en predicciones: {len(df_predicciones)}")
    st.write(f"Número de estados en el mapa: {len(mexico)}")
except Exception as e:
    st.error(f"Error al cargar los datos: {str(e)}")
    st.stop()

# Preparación de datos
df_predicciones['Estado'] = df_predicciones['Estado'].str.lower().str.strip()
mexico['name'] = mexico['name'].str.lower().str.strip()

# Título
st.title("Predicciones de Precipitación en México")

# Crear dos columnas
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Mapa de Precipitaciones")
    
    # Selector de año
    año_seleccionado = st.selectbox(
        "Selecciona el año de predicción:",
        options=sorted(df_predicciones['Año'].unique())
    )
    
    try:
        # Filtrar datos
        df_filtrado = df_predicciones[df_predicciones['Año'] == año_seleccionado]
        merged = mexico.set_index('name').join(df_filtrado.set_index('Estado'))
        
        # Crear mapa
        fig, ax = plt.subplots(figsize=(10, 10))
        merged.boundary.plot(ax=ax, linewidth=1)
        merged.plot(column='Precipitación', 
                   ax=ax, 
                   legend=True,
                   legend_kwds={'label': 'Precipitación (mm)'},
                   cmap='Blues')

         # Agregar nombres de los estados
        for idx, row in merged.iterrows():
            # Obtener el centroide de cada estado
            centroid = row.geometry.centroid
            # Añadir el texto del nombre del estado
            ax.annotate(text=idx.title(),  # Convertir a título para mejor presentación
                       xy=(centroid.x, centroid.y),
                       horizontalalignment='center',
                       verticalalignment='center',
                       fontsize=8,
                       color='black')
            
        plt.title(f'Precipitaciones {año_seleccionado}')
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error al crear el mapa: {str(e)}")

with col2:
    st.subheader("Serie Temporal")
    
    # Selector de estado
    estado_seleccionado = st.selectbox(
        "Selecciona un estado:",
        options=sorted(df_predicciones['Estado'].unique())
    )
    
    try:
        # Filtrar datos para el estado
        df_estado = df_predicciones[df_predicciones['Estado'] == estado_seleccionado]
        
        # Crear gráfica de línea
        fig_line = px.line(df_estado,
                          x='Año',
                          y='Precipitación',
                          title=f'Predicciones para {estado_seleccionado.title()}')
        st.plotly_chart(fig_line)
        
        # Mostrar estadísticas básicas
        st.write("Estadísticas:")
        st.write(df_estado['Precipitación'].describe())
    except Exception as e:
        st.error(f"Error al crear la serie temporal: {str(e)}")

# Mostrar datos crudos si se desea
if st.checkbox("Mostrar datos crudos"):
    st.write(df_predicciones)
