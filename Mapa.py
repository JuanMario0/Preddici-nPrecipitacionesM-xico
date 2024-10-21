import streamlit as st
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt


df_predicciones = pd.read_csv("C:\\Users\\PC\\Desktop\\PP Agua\\MapaPrediccionsPIIA\\df_predicciones.csv")
# Cargar el shapefile de México
mexico = gpd.read_file("C:\\Users\\PC\\Desktop\\PP Agua\\MapaPrediccionsPIIA\\mexicoHigh.json")  # Cambia esto a la ruta de tu shapefile


# Interfaz de usuario en Streamlit
st.title("Predicciones de Precipitación en México")

# Slider para seleccionar el año
año_seleccionado = st.selectbox("Selecciona el año de predicción:", options=[2025, 2026, 2027, 2030])

# Filtrar el DataFrame por el año seleccionado
df_filtrado = df_predicciones[df_predicciones['Año'] == año_seleccionado]

# Merge entre el GeoDataFrame y el DataFrame filtrado
merged = mexico.set_index('name').join(df_filtrado.set_index('Estado'))

# Crear el mapa
fig, ax = plt.subplots(1, 1, figsize=(12, 12))
merged.boundary.plot(ax=ax, linewidth=1)
merged.plot(column='Precipitación', ax=ax, legend=True,
            legend_kwds={'label': "Precipitación (mm)",
                         'orientation': "horizontal"},
            cmap='Blues', missing_kwds={"color": "lightgrey", "label": "No predicción"})

# Agregar nombres de los estados
for x, y, label in zip(merged.geometry.centroid.x, merged.geometry.centroid.y, merged.index):
    ax.annotate(label, xy=(x, y), horizontalalignment='center', fontsize=8, color='black')

plt.title(f'Mapa de Precipitaciones Predichas por Estado para el Año {año_seleccionado}')
st.pyplot(fig)
