"""
Dashboard interactivo — Valoración de jugadores
Primera División de Chile 2026 (primera rueda)

Métrica principal: rating de Sofascore de cada jugador RELATIVO al promedio
de su propio equipo. Permite identificar quién rinde por sobre (o por bajo)
el nivel medio de su plantel.

Para ejecutar:  streamlit run app.py
"""

from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# Carpeta donde vive este archivo: así las rutas no dependen de dónde se lance la app
BASE_DIR = Path(__file__).parent

# --------------------------------------------------------------------------
# 1) CONFIGURACIÓN DE LA PÁGINA
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Valoración de jugadores — Chile 2026",
    page_icon="⚽",
    layout="wide",
)


# --------------------------------------------------------------------------
# 2) CARGA DE DATOS
#    @st.cache_data guarda el resultado en memoria: el CSV se lee una sola
#    vez y no en cada interacción, así el dashboard va rápido.
# --------------------------------------------------------------------------
@st.cache_data
def cargar_datos():
    df = pd.read_csv(BASE_DIR / "data" / "processed" / "ranking_jugadores_2026.csv")
    return df


df = cargar_datos()

# Nombres "bonitos" para mostrar en la interfaz, mapeados a las columnas reales
METRICAS = {
    "Rating relativo (jugador / promedio equipo)": "rating_relativo",
    "Diferencia sobre su equipo (en puntos)": "diferencia",
    "Rating crudo de Sofascore": "rating",
}


# --------------------------------------------------------------------------
# 3) BARRA LATERAL: FILTROS
# --------------------------------------------------------------------------
st.sidebar.header("Filtros")

equipos = ["Todos los equipos"] + sorted(df["team"].unique().tolist())
equipo_sel = st.sidebar.selectbox("Equipo", equipos)

nombre_metrica = st.sidebar.selectbox("Ordenar / medir por", list(METRICAS.keys()))
col_metrica = METRICAS[nombre_metrica]

top_n = st.sidebar.slider("¿Cuántos jugadores mostrar en el gráfico?", 5, 30, 15)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Datos: Sofascore vía LanusStats. Solo jugadores con ≥ 675 minutos "
    "(la mitad de los minutos posibles de la primera rueda)."
)

# Aplicamos el filtro de equipo
if equipo_sel == "Todos los equipos":
    df_vista = df.copy()
else:
    df_vista = df[df["team"] == equipo_sel].copy()

df_vista = df_vista.sort_values(col_metrica, ascending=False)


# --------------------------------------------------------------------------
# 4) ENCABEZADO Y MÉTRICAS RESUMEN (KPIs)
# --------------------------------------------------------------------------
st.title("⚽ Valoración de jugadores — Primera División de Chile 2026")
st.markdown(
    "Ranking de jugadores según su **rating de Sofascore relativo al promedio "
    "de su equipo** durante la primera rueda del Campeonato Nacional 2026."
)

col1, col2, col3 = st.columns(3)
col1.metric("Jugadores analizados", len(df_vista))
mejor = df_vista.iloc[0]
col2.metric("Mejor por la métrica elegida", mejor["player"], f'{mejor[col_metrica]:.3f}')
col3.metric("Rating promedio de la vista", f'{df_vista["rating"].mean():.2f}')

st.markdown("---")


# --------------------------------------------------------------------------
# 5) GRÁFICO DE BARRAS: TOP N JUGADORES
# --------------------------------------------------------------------------
st.subheader(f"Top {top_n} — {nombre_metrica}")

df_top = df_vista.head(top_n)

fig = px.bar(
    df_top,
    x=col_metrica,
    y="player",
    color="team",
    orientation="h",
    hover_data=["team", "rating", "rating_promedio_equipo", "minutesPlayed"],
    labels={col_metrica: nombre_metrica, "player": ""},
)
# El de mayor valor arriba
fig.update_layout(yaxis=dict(autorange="reversed"), height=500)
st.plotly_chart(fig, use_container_width=True)


# --------------------------------------------------------------------------
# 6) GRÁFICO DE DISPERSIÓN: RATING vs PROMEDIO DEL EQUIPO
#    La línea diagonal marca "rinde igual que su equipo". Por encima =
#    destaca; por debajo = queda corto.
# --------------------------------------------------------------------------
st.subheader("Jugador vs. nivel de su equipo")

fig2 = px.scatter(
    df_vista,
    x="rating_promedio_equipo",
    y="rating",
    color="team",
    size="minutesPlayed",
    hover_name="player",
    labels={
        "rating_promedio_equipo": "Rating promedio del equipo",
        "rating": "Rating del jugador",
    },
)
# Línea de referencia y = x (jugador rinde igual que su equipo)
lo = df_vista["rating_promedio_equipo"].min() - 0.1
hi = df_vista["rating"].max() + 0.1
fig2.add_shape(type="line", x0=lo, y0=lo, x1=hi, y1=hi,
               line=dict(dash="dash", color="gray"))
st.plotly_chart(fig2, use_container_width=True)


# --------------------------------------------------------------------------
# 7) TABLA COMPLETA
# --------------------------------------------------------------------------
st.subheader("Tabla completa")
st.dataframe(
    df_vista[
        ["player", "team", "appearances", "minutesPlayed",
         "rating", "rating_promedio_equipo", "rating_relativo", "diferencia"]
    ].reset_index(drop=True),
    use_container_width=True,
)
