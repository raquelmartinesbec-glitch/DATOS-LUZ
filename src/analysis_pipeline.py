"""
Pipeline principal de análisis de microacciones según estado emocional.
"""
import pandas as pd
import numpy as np
from src.data_generator import EmotionalDataGenerator
from src.normalization import UserNormalizer
from src.emotional_segmentation import EmotionalSegmenter
from src.clustering_analysis import ClusteringAnalyzer


class MicroactionAnalysisPipeline:
    """Pipeline completo para el análisis de microacciones y estados emocionales."""
    
    def __init__(self, n_clusters=3):
        """
        Inicializa el pipeline de análisis.
        
        Args:
            n_clusters: Número de clusters para el análisis
        """
        self.generator = EmotionalDataGenerator()
        self.normalizer = UserNormalizer()
        self.segmenter = EmotionalSegmenter()
        self.clusterer = ClusteringAnalyzer(n_clusters=n_clusters)
        
        self.data = None
        self.normalized_data = None
        self.segments = None
        self.clustered_data = None
    
    def run_analysis(self, n_usuarios=100, n_eventos_por_usuario=50, generate_data=True):
        """
        Ejecuta el análisis completo.
        
        Args:
            n_usuarios: Número de usuarios (si se generan datos)
            n_eventos_por_usuario: Número de eventos por usuario (si se generan datos)
            generate_data: Si True, genera datos sintéticos; si False, usa datos existentes
            
        Returns:
            Diccionario con resultados del análisis
        """
        print("=" * 80)
        print("ANÁLISIS DE MICROACCIONES SEGÚN ESTADO EMOCIONAL PREVIO")
        print("=" * 80)
        print()
        
        # Paso 1: Generar o cargar datos
        if generate_data:
            print("[1/4] Generando datos sintéticos...")
            self.data = self.generator.generar_datos(n_usuarios, n_eventos_por_usuario)
            print(f"  ✓ Generados {len(self.data)} eventos para {n_usuarios} usuarios")
        else:
            print("[1/4] Cargando datos existentes...")
            # Aquí se cargarían datos reales
            self.data = pd.read_csv('data/emotional_data.csv')
            print(f"  ✓ Cargados {len(self.data)} eventos")
        
        print()
        
        # Paso 2: Normalización por usuario
        print("[2/4] Normalizando por usuario...")
        self.normalized_data = self.normalizer.fit_transform(self.data)
        print(f"  ✓ Normalización completada para {self.data['usuario_id'].nunique()} usuarios")
        print()
        
        # Paso 3: Segmentación por estado emocional
        print("[3/4] Segmentando por estado emocional previo...")
        self.segments = self.segmenter.segment_by_emotion(self.normalized_data)
        print(f"  ✓ Identificados {len(self.segments)} estados emocionales")
        
        # Analizar efectividad por segmento
        for estado in self.segments.keys():
            best_actions = self.segmenter.get_best_microactions(estado, top_n=3)
            print(f"    - {estado.capitalize()}: mejores microacciones → {', '.join(best_actions)}")
        
        print()
        
        # Paso 4: Clustering para patrones latentes
        print("[4/4] Identificando patrones latentes mediante clustering...")
        self.clustered_data = self.clusterer.fit_predict(self.normalized_data)
        print(f"  ✓ Identificados {self.clusterer.n_clusters} clusters de patrones")
        print()
        
        # Generar resumen de resultados
        results = self._generate_results_summary()
        
        return results
    
    def _generate_results_summary(self):
        """
        Genera un resumen de los resultados del análisis.
        
        Returns:
            Diccionario con resumen de resultados
        """
        results = {
            'datos_generales': {
                'n_eventos_totales': len(self.data),
                'n_usuarios': self.data['usuario_id'].nunique(),
                'n_estados_emocionales': len(self.segments),
                'n_microacciones': self.data['microaccion'].nunique()
            },
            'estadisticas_por_estado': {},
            'mejores_microacciones_por_estado': {},
            'patrones_clustering': self.clusterer.get_cluster_patterns()
        }
        
        # Estadísticas por estado emocional
        for estado, segment_df in self.segments.items():
            results['estadisticas_por_estado'][estado] = {
                'n_eventos': len(segment_df),
                'efectividad_media': segment_df['efectividad'].mean(),
                'efectividad_std': segment_df['efectividad'].std()
            }
            
            # Mejores microacciones
            effectiveness = self.segmenter.analyze_microaction_effectiveness(estado)
            if effectiveness is not None and len(effectiveness) > 0:
                results['mejores_microacciones_por_estado'][estado] = effectiveness.to_dict('records')
        
        return results
    
    def print_detailed_results(self, results):
        """
        Imprime resultados detallados del análisis.
        
        Args:
            results: Diccionario con resultados del análisis
        """
        print("=" * 80)
        print("RESULTADOS DETALLADOS")
        print("=" * 80)
        print()
        
        # Datos generales
        print("📊 DATOS GENERALES")
        print("-" * 80)
        for key, value in results['datos_generales'].items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print()
        
        # Análisis por estado emocional
        print("🎭 ANÁLISIS POR ESTADO EMOCIONAL PREVIO")
        print("-" * 80)
        for estado, stats in results['estadisticas_por_estado'].items():
            print(f"\n  Estado: {estado.upper()}")
            print(f"    - Eventos: {stats['n_eventos']}")
            print(f"    - Efectividad media: {stats['efectividad_media']:.3f}")
            print(f"    - Desviación estándar: {stats['efectividad_std']:.3f}")
            
            if estado in results['mejores_microacciones_por_estado']:
                print(f"    - Mejores microacciones:")
                for idx, ma in enumerate(results['mejores_microacciones_por_estado'][estado][:3], 1):
                    print(f"      {idx}. {ma['microaccion']}: {ma['efectividad_mean']:.3f} "
                          f"(n={ma['efectividad_count']:.0f})")
        
        print()
        
        # Patrones de clustering
        print("🔍 PATRONES LATENTES (CLUSTERING)")
        print("-" * 80)
        cluster_interpretation = self.clusterer.interpret_clusters()
        print(cluster_interpretation.to_string(index=False))
        print()
        
        # Insights principales
        print("💡 INSIGHTS PRINCIPALES")
        print("-" * 80)
        self._print_key_insights(results)
        print()
    
    def _print_key_insights(self, results):
        """
        Imprime insights clave del análisis.
        
        Args:
            results: Diccionario con resultados del análisis
        """
        # Estado con mayor efectividad
        max_efectividad_estado = max(
            results['estadisticas_por_estado'].items(),
            key=lambda x: x[1]['efectividad_media']
        )
        print(f"  1. Estado emocional con mayor efectividad promedio:")
        print(f"     → {max_efectividad_estado[0].upper()} "
              f"({max_efectividad_estado[1]['efectividad_media']:.3f})")
        
        # Cluster más efectivo
        cluster_patterns = results['patrones_clustering']
        max_efectividad_cluster = max(
            cluster_patterns.items(),
            key=lambda x: x[1]['efectividad_media']
        )
        print(f"\n  2. Patrón latente más efectivo (Cluster {max_efectividad_cluster[0]}):")
        print(f"     → Estado: {max_efectividad_cluster[1]['estado_emocional_previo_dominante']}")
        print(f"     → Microacción: {max_efectividad_cluster[1]['microaccion_dominante']}")
        print(f"     → Efectividad: {max_efectividad_cluster[1]['efectividad_media']:.3f}")
        
        # Variabilidad entre usuarios
        print(f"\n  3. La normalización por usuario revela patrones más allá de la")
        print(f"     percepción consciente, identificando efectividad real vs. percibida")
    
    def save_results(self, output_dir='data'):
        """
        Guarda los resultados del análisis.
        
        Args:
            output_dir: Directorio donde guardar los resultados
        """
        import os
        os.makedirs(output_dir, exist_ok=True)
        
        # Guardar datos procesados
        self.normalized_data.to_csv(f'{output_dir}/datos_normalizados.csv', index=False)
        self.clustered_data.to_csv(f'{output_dir}/datos_con_clusters.csv', index=False)
        
        # Guardar análisis por estado
        for estado, segment_df in self.segments.items():
            effectiveness = self.segmenter.analyze_microaction_effectiveness(estado)
            effectiveness.to_csv(f'{output_dir}/efectividad_{estado}.csv', index=False)
        
        # Guardar interpretación de clusters
        cluster_interpretation = self.clusterer.interpret_clusters()
        cluster_interpretation.to_csv(f'{output_dir}/interpretacion_clusters.csv', index=False)
        
        print(f"✓ Resultados guardados en '{output_dir}/'")
