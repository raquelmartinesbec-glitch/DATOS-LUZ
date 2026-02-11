"""
Módulo de normalización por usuario para el análisis de microacciones.
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler


class UserNormalizer:
    """Normaliza las métricas de efectividad por usuario."""
    
    def __init__(self):
        """Inicializa el normalizador."""
        self.scalers = {}
        self.user_stats = {}
    
    def fit_transform(self, df):
        """
        Normaliza la efectividad por usuario usando z-score.
        
        Args:
            df: DataFrame con columnas 'usuario_id' y 'efectividad'
            
        Returns:
            DataFrame con columna adicional 'efectividad_normalizada'
        """
        df_normalized = df.copy()
        efectividad_normalizada = []
        
        for usuario_id in df['usuario_id'].unique():
            mask = df['usuario_id'] == usuario_id
            user_data = df.loc[mask, 'efectividad'].values.reshape(-1, 1)
            
            # Calcular estadísticas del usuario
            media = np.mean(user_data)
            std = np.std(user_data)
            
            self.user_stats[usuario_id] = {
                'media': media,
                'std': std if std > 0 else 1.0,
                'min': np.min(user_data),
                'max': np.max(user_data)
            }
            
            # Normalización z-score
            if std > 0:
                normalized = (user_data - media) / std
            else:
                normalized = np.zeros_like(user_data)
            
            efectividad_normalizada.extend(normalized.flatten().tolist())
        
        df_normalized['efectividad_normalizada'] = efectividad_normalizada
        return df_normalized
    
    def transform(self, df):
        """
        Aplica la normalización a nuevos datos usando estadísticas guardadas.
        
        Args:
            df: DataFrame con columnas 'usuario_id' y 'efectividad'
            
        Returns:
            DataFrame con columna adicional 'efectividad_normalizada'
        """
        df_normalized = df.copy()
        efectividad_normalizada = []
        
        for idx, row in df.iterrows():
            usuario_id = row['usuario_id']
            efectividad = row['efectividad']
            
            if usuario_id in self.user_stats:
                stats = self.user_stats[usuario_id]
                normalized = (efectividad - stats['media']) / stats['std']
            else:
                # Si el usuario no existe, usar normalización sin sesgo
                normalized = 0.0
            
            efectividad_normalizada.append(normalized)
        
        df_normalized['efectividad_normalizada'] = efectividad_normalizada
        return df_normalized
    
    def get_user_baseline(self, usuario_id):
        """
        Obtiene la línea base de un usuario específico.
        
        Args:
            usuario_id: ID del usuario
            
        Returns:
            Diccionario con estadísticas del usuario
        """
        return self.user_stats.get(usuario_id, None)
