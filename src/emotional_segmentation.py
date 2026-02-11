"""
Módulo de segmentación por estado emocional.
"""
import pandas as pd
import numpy as np


class EmotionalSegmenter:
    """Segmenta los datos según el estado emocional previo del usuario."""
    
    def __init__(self):
        """Inicializa el segmentador."""
        self.segments = {}
        self.segment_stats = {}
    
    def segment_by_emotion(self, df):
        """
        Segmenta el dataset por estado emocional previo.
        
        Args:
            df: DataFrame con columna 'estado_emocional_previo'
            
        Returns:
            Diccionario con DataFrames segmentados por estado emocional
        """
        self.segments = {}
        self.segment_stats = {}
        
        for estado in df['estado_emocional_previo'].unique():
            segment_df = df[df['estado_emocional_previo'] == estado].copy()
            self.segments[estado] = segment_df
            
            # Calcular estadísticas del segmento
            self.segment_stats[estado] = {
                'n_eventos': len(segment_df),
                'efectividad_media': segment_df['efectividad'].mean(),
                'efectividad_std': segment_df['efectividad'].std(),
                'n_usuarios': segment_df['usuario_id'].nunique(),
                'microacciones_distribucion': segment_df['microaccion'].value_counts().to_dict()
            }
        
        return self.segments
    
    def get_segment_stats(self, estado=None):
        """
        Obtiene estadísticas de un segmento o de todos.
        
        Args:
            estado: Estado emocional específico (opcional)
            
        Returns:
            Estadísticas del segmento o de todos los segmentos
        """
        if estado:
            return self.segment_stats.get(estado, None)
        return self.segment_stats
    
    def analyze_microaction_effectiveness(self, estado):
        """
        Analiza la efectividad de cada microacción en un estado emocional.
        
        Args:
            estado: Estado emocional a analizar
            
        Returns:
            DataFrame con efectividad por microacción
        """
        if estado not in self.segments:
            return None
        
        segment_df = self.segments[estado]
        
        # Agrupar por microacción y calcular métricas
        effectiveness = segment_df.groupby('microaccion').agg({
            'efectividad': ['mean', 'std', 'count'],
            'efectividad_normalizada': ['mean', 'std']
        }).round(3)
        
        effectiveness.columns = ['_'.join(col).strip() for col in effectiveness.columns.values]
        effectiveness = effectiveness.reset_index()
        effectiveness = effectiveness.sort_values('efectividad_mean', ascending=False)
        
        return effectiveness
    
    def get_best_microactions(self, estado, top_n=3):
        """
        Obtiene las mejores microacciones para un estado emocional.
        
        Args:
            estado: Estado emocional
            top_n: Número de microacciones a retornar
            
        Returns:
            Lista de las mejores microacciones ordenadas por efectividad
        """
        effectiveness = self.analyze_microaction_effectiveness(estado)
        
        if effectiveness is None or len(effectiveness) == 0:
            return []
        
        return effectiveness.head(top_n)['microaccion'].tolist()
