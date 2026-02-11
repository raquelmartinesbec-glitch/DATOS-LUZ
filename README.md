# DATOS-LUZ: Análisis de Microacciones Según Estado Emocional Previo

## Descripción del Proyecto

Este proyecto implementa una metodología avanzada para responder a la pregunta de investigación:

**¿Qué microacciones funcionan mejor según el estado emocional previo del usuario, más allá de la percepción consciente?**

## Metodología

La metodología combina tres enfoques complementarios:

### 1. Normalización por Usuario
- Ajusta las métricas de efectividad según la línea base personal de cada usuario
- Utiliza z-score para identificar patrones independientes de la percepción consciente
- Permite comparar efectividad real vs. percibida

### 2. Segmentación por Estado Emocional
- Agrupa eventos según el estado emocional previo del usuario
- Identifica las microacciones más efectivas para cada estado emocional
- Calcula estadísticas de efectividad por segmento

### 3. Clustering para Patrones Latentes
- Aplica K-Means clustering para identificar patrones ocultos
- Descubre combinaciones óptimas de estado-microacción
- Revela insights más allá del análisis segmentado tradicional

## Estructura del Proyecto

```
DATOS-LUZ/
├── src/
│   ├── __init__.py
│   ├── data_generator.py          # Generación de datos sintéticos
│   ├── normalization.py            # Normalización por usuario
│   ├── emotional_segmentation.py  # Segmentación emocional
│   ├── clustering_analysis.py     # Análisis de clustering
│   └── analysis_pipeline.py       # Pipeline completo
├── notebooks/                       # Notebooks de análisis (opcional)
├── data/                           # Datos generados y resultados
├── main.py                         # Script principal
├── requirements.txt                # Dependencias
└── README.md                       # Este archivo
```

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/raquelmartinesbec-glitch/DATOS-LUZ.git
cd DATOS-LUZ
```

2. Instalar dependencias:
```bash
pip install -r requirements.txt
```

## Uso

### Ejecución Básica

Para ejecutar el análisis completo con datos sintéticos:

```bash
python main.py
```

### Uso Programático

```python
from src.analysis_pipeline import MicroactionAnalysisPipeline

# Crear pipeline
pipeline = MicroactionAnalysisPipeline(n_clusters=5)

# Ejecutar análisis
results = pipeline.run_analysis(
    n_usuarios=100,
    n_eventos_por_usuario=50,
    generate_data=True
)

# Imprimir resultados
pipeline.print_detailed_results(results)

# Guardar resultados
pipeline.save_results(output_dir='data')
```

### Uso de Módulos Individuales

#### Generación de Datos
```python
from src.data_generator import EmotionalDataGenerator

generator = EmotionalDataGenerator(seed=42)
data = generator.generar_datos(n_usuarios=100, n_eventos_por_usuario=50)
```

#### Normalización por Usuario
```python
from src.normalization import UserNormalizer

normalizer = UserNormalizer()
normalized_data = normalizer.fit_transform(data)
```

#### Segmentación Emocional
```python
from src.emotional_segmentation import EmotionalSegmenter

segmenter = EmotionalSegmenter()
segments = segmenter.segment_by_emotion(normalized_data)

# Obtener mejores microacciones para un estado
best_actions = segmenter.get_best_microactions('ansiedad', top_n=3)
```

#### Clustering
```python
from src.clustering_analysis import ClusteringAnalyzer

clusterer = ClusteringAnalyzer(n_clusters=5)
clustered_data = clusterer.fit_predict(normalized_data)

# Interpretar clusters
interpretations = clusterer.interpret_clusters()
```

## Estados Emocionales

El sistema analiza cinco estados emocionales principales:

1. **Alegría** - Estado positivo, alta energía
2. **Tristeza** - Estado negativo, baja energía
3. **Ansiedad** - Estado negativo, alta energía
4. **Calma** - Estado positivo, baja energía
5. **Frustración** - Estado negativo, energía media-alta

## Microacciones

Las microacciones analizadas incluyen:

1. **Respiración profunda** - Técnica de control respiratorio
2. **Pausa breve** - Descanso corto de la actividad
3. **Cambio de postura** - Ajuste físico corporal
4. **Escuchar música** - Intervención auditiva
5. **Ejercicio visual** - Técnica de descanso visual

## Resultados

El análisis genera varios archivos de salida en el directorio `data/`:

- `datos_normalizados.csv` - Datos con normalización por usuario
- `datos_con_clusters.csv` - Datos con asignación de clusters
- `efectividad_{estado}.csv` - Análisis por estado emocional
- `interpretacion_clusters.csv` - Interpretación de patrones latentes

### Métricas Clave

1. **Efectividad Media**: Promedio de efectividad de cada microacción
2. **Efectividad Normalizada**: Efectividad ajustada por usuario
3. **Distribución por Estado**: Frecuencia de cada estado emocional
4. **Patrones Latentes**: Combinaciones óptimas identificadas por clustering

## Insights Esperados

El análisis permite identificar:

- ✅ Microacciones más efectivas para cada estado emocional
- ✅ Patrones latentes más allá de la segmentación simple
- ✅ Diferencias entre efectividad real y percepción consciente
- ✅ Perfiles de usuario según respuesta a microacciones
- ✅ Recomendaciones personalizadas por contexto emocional

## Aplicaciones

Esta metodología puede aplicarse a:

- **Aplicaciones de bienestar digital**: Recomendación de intervenciones personalizadas
- **Sistemas de salud mental**: Identificación de técnicas efectivas por contexto
- **Diseño de experiencia de usuario**: Optimización de interacciones según estado emocional
- **Investigación en psicología**: Análisis de efectividad de intervenciones breves

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Haz fork del proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Añade nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la licencia MIT.

## Contacto

Para preguntas o colaboraciones, por favor abre un issue en el repositorio.

## Referencias

Esta implementación se basa en principios de:
- Análisis de datos emocionales
- Machine learning no supervisado
- Personalización de intervenciones
- Psicología del bienestar digital