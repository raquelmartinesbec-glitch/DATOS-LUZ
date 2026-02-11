"""
Script principal para ejecutar el análisis de microacciones según estado emocional.

Metodología:
1. Normalización por usuario
2. Segmentación por estado emocional
3. Clustering para identificar patrones latentes
"""
from src.analysis_pipeline import MicroactionAnalysisPipeline


def main():
    """Función principal para ejecutar el análisis."""
    
    # Crear pipeline de análisis
    pipeline = MicroactionAnalysisPipeline(n_clusters=5)
    
    # Ejecutar análisis completo
    results = pipeline.run_analysis(
        n_usuarios=100,
        n_eventos_por_usuario=50,
        generate_data=True
    )
    
    # Imprimir resultados detallados
    pipeline.print_detailed_results(results)
    
    # Guardar resultados
    pipeline.save_results(output_dir='data')
    
    print("=" * 80)
    print("ANÁLISIS COMPLETADO")
    print("=" * 80)


if __name__ == '__main__':
    main()
