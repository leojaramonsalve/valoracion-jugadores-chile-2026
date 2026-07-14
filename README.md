#  Valoración de jugadores — Primera División de Chile 2026

Ranking de jugadores del Campeonato Nacional chileno (primera rueda 2026) a partir de los *ratings* de [Sofascore](https://www.sofascore.com/), usando una **métrica relativa** que mide el rendimiento de cada jugador respecto al promedio de su propio equipo.

> **Pregunta que responde el proyecto:** ¿Cómo poder sacar más provecho a los rankings de páginas como Sofascore? en vez de "¿quién tiene la mejor nota?", observaremos cómo se comporta un jugador en el tiempo y en función de su equipo.

##  Motivación

El *rating* de Sofascore es útil pero sesgado: no es lo mismo destacar en un equipo que domina los partidos que en uno que lucha en el fondo de la tabla. Además algunas de sus métricas no siempre dan cuenta de lo que realmente se percibe en un encuentro(lo que se cuenta como asistencia no siempre es un pase en profundidad o una ocasión clara de gol). Para corregirlo, se construye una métrica sencilla de calcular y mucho más interesante de observar en el mediano plazo:

```
rating_relativo = rating_del_jugador / rating_promedio_de_su_equipo
```

Un valor mayor a 1 indica que el jugador rinde **por encima** de la media de su plantel; menor a 1, por debajo. Así podemos identificar los jugadores que destacan dentro de su equipo, así como aquellos cuya performance está por debajo de lo que se espera. Al construirse con promedios, siempre habrán jugadores por arriba o debajo de este.

##  Hallazgo principal

El jugador con el **rating crudo más alto** de la primera rueda (Fernando Zampedri, U. Católica, 7.56) **no lidera** el ranking relativo, porque su equipo promedia alto y "destacar ahí cuesta más". En cambio, quien encabeza la métrica relativa es un jugador que **carga a un equipo más irregular**. 

## Resultados

### Top 15 — jugadores que más destacan sobre su equipo

|  # | Jugador              | Equipo               | Rating | Prom. equipo | Rating relativo |
| -: | -------------------- | -------------------- | -----: | -----------: | --------------: |
|  1 | Francisco González   | O'Higgins            |   7.44 |         6.85 |           1.086 |
|  2 | Kevin Méndez         | Unión La Calera      |   7.35 |         6.79 |           1.083 |
|  3 | Arturo Vidal         | Colo-Colo            |   7.51 |         6.98 |           1.075 |
|  4 | Fernando Zampedri    | Universidad Católica |   7.56 |         7.03 |           1.075 |
|  5 | Jorge Henríquez      | Deportes Concepción  |   7.20 |         6.71 |           1.073 |
|  6 | Juan Cornejo         | Coquimbo Unido       |   7.45 |         6.96 |           1.071 |
|  7 | Jean Meneses         | Deportes Limache     |   7.41 |         6.95 |           1.067 |
|  8 | Matías Zaldivia      | Universidad de Chile |   7.44 |         6.99 |           1.064 |
|  9 | Gabriel Castellón    | Universidad de Chile |   7.44 |         6.99 |           1.064 |
| 10 | Jeisson Vargas       | Deportes La Serena   |   7.19 |         6.80 |           1.057 |
| 11 | Nicolás Vargas       | Huachipato           |   7.19 |         6.80 |           1.057 |
| 12 | Matías Palavecino    | Universidad Católica |   7.42 |         7.03 |           1.055 |
| 13 | Alejandro Santander  | Cobresal             |   7.16 |         6.80 |           1.052 |
| 14 | Bryan Carvallo       | Cobresal             |   7.15 |         6.80 |           1.051 |
| 15 | Víctor Felipe Méndez | Colo-Colo            |   7.33 |         6.98 |           1.050 |

### Bottom 10 — jugadores que más quedan por debajo de su equipo

|  # | Jugador           | Equipo                    | Rating | Prom. equipo | Rating relativo |
| -: | ----------------- | ------------------------- | -----: | -----------: | --------------: |
|  1 | Alan Robledo      | O'Higgins                 |   6.43 |         6.85 |           0.938 |
|  2 | Joaquín Gutiérrez | Deportes La Serena        |   6.39 |         6.80 |           0.939 |
|  3 | Emiliano Ramos    | Everton de Viña del Mar   |   6.53 |         6.92 |           0.943 |
|  4 | Diego Carrasco    | Deportes Concepción       |   6.39 |         6.71 |           0.952 |
|  5 | Javier Altamirano | Universidad de Chile      |   6.67 |         6.99 |           0.954 |
|  6 | Jorge Espejo      | Universidad de Concepción |   6.45 |         6.75 |           0.955 |
|  7 | Yahir Salazar     | Deportes La Serena        |   6.50 |         6.80 |           0.955 |
|  8 | Franco Bechtholdt | Cobresal                  |   6.50 |         6.80 |           0.955 |
|  9 | Marcelo Flores    | Deportes Limache          |   6.66 |         6.95 |           0.959 |
| 10 | Clemente Montes   | Universidad Católica      |   6.75 |         7.03 |           0.960 |

##  Metodología

1. **Recolección**: se descargan las estadísticas de temporada de todos los jugadores desde Sofascore con la librería [`LanusStats`](https://pypi.org/project/LanusStats/) (usa un navegador real por debajo para evitar bloqueos).
2. **Selección de variables**: Se escogieron 5 variables `player`, `team`, `appearances`, `minutesPlayed` y `rating`.
3. **Filtro de regularidad**: solo jugadores con **≥ 675 minutos** (la mitad de los 1350 posibles en las 15 fechas de la primera rueda). Esto busca nutrir al dataset de consistencia sin dejar a ningún equipo sub-representado (y quitando del ejercicio a jugadores que jugaron pocos partidos, ya sea por lesión o por desición técnica). De 414 jugadores iniciales quedan **165**, con los 16 equipos representados (9–11 jugadores cada uno).
4. **Cálculo de la métrica**: rating promedio por equipo (`groupby` + `transform`) y luego el rating relativo y la diferencia en puntos.
5. **Visualización**: dashboard interactivo en Streamlit + Plotly.

##  Dashboard

El dashboard permite filtrar por equipo, ordenar por distintas métricas y explorar:

- Ranking Top N de jugadores.
- Dispersión *rating del jugador vs. promedio de su equipo* (con línea de referencia).
- Tabla completa filtrable.

Para lanzarlo:

```bash
streamlit run app.py
```

##  Estructura del proyecto

```
.
├── 01_exploracion.ipynb              # Notebook: recolección, limpieza y cálculo
├── app.py                            # Dashboard interactivo (Streamlit)
├── data/
│   ├── raw/                          # Datos crudos descargados de Sofascore
│   └── processed/                    # Dataset final con la métrica calculada
├── requirements.txt                  # Dependencias del dashboard
├── requirements-dev.txt              # Entorno completo (notebook + scraping)
├── .gitignore
└── README.md
```

##  Cómo reproducirlo

```bash
# 1. Clonar el repositorio
git clone <URL-de-tu-repo>
cd <carpeta-del-repo>

# 2. Crear y activar un entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS / Linux

# 3. Instalar dependencias del dashboard
pip install -r requirements.txt
#    (Para reproducir el notebook y el scraping: pip install -r requirements-dev.txt)

# 4. (Opcional) Volver a descargar los datos ejecutando el notebook,
#    o usar directamente el CSV ya incluido en data/processed/

# 5. Lanzar el dashboard
streamlit run app.py
```

> Requiere tener **Google Chrome** instalado (LanusStats lo usa por debajo para descargar los datos).

##  Notas y posibles mejoras

- El *rating* de Sofascore es una métrica propietaria y aproximada; los resultados deben leerse como una guía, no como una verdad absoluta.
- Posibles extensiones: ponderar el promedio de equipo por minutos jugados, separar el análisis por posición, o comparar varias temporadas.

## 🙏 Créditos

- Datos: [Sofascore](https://www.sofascore.com/) vía la librería `LanusStats`.
- La idea de la métrica relativa está inspirada en un análisis similar hecho sobre la segunda división del fútbol argentino por el canal de Youtube Lanus Stats.

---

Proyecto desarrollado por Leonardo Jara M. como pieza de portafolio de ciencia de datos.
