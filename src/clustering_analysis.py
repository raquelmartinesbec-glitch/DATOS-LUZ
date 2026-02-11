"""
Módulo de análisis de clustering para identificar patrones latentes.
"""
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import LabelEncoder


class ClusteringAnalyzer:
    """Identifica patrones latentes usando clustering."""
    
    def __init__(self, n_clusters=3):
        """
        Inicializa el analizador de clustering.
        
        Args:
            n_clusters: Número de clusters a identificar
        """
        self.n_clusters = n_clusters
        self.kmeans = None
        self.label_encoders = {}
        self.cluster_patterns = {}
    
    def prepare_features(self, df):
        """
        Prepara las características para el clustering.
        
        Args:
            df: DataFrame con los datos
            
        Returns:
            Array de características y mapeo de etiquetas
        """
        df_encoded = df.copy()
        
        # Codificar variables categóricas
        categorical_cols = ['estado_emocional_previo', 'microaccion', 'estado_emocional_posterior']
        
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df_encoded[f'{col}_encoded'] = le.fit_transform(df[col])
                self.label_encoders[col] = le
        
        # Seleccionar características para clustering
        feature_cols = [
            'estado_emocional_previo_encoded',
            'microaccion_encoded',
            'efectividad_normalizada',
            'tiempo_aplicacion_seg',
            'estado_emocional_posterior_encoded'
        ]
        
        features = df_encoded[feature_cols].values
        return features, df_encoded
    
    def fit_predict(self, df):
        """
        Aplica clustering a los datos.
        
        Args:
            df: DataFrame con los datos
            
        Returns:
            DataFrame con asignación de clusters
        """
        features, df_encoded = self.prepare_features(df)
        
        # Normalizar características
        from sklearn.preprocessing import StandardScaler
        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)
        
        # Aplicar K-Means
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        clusters = self.kmeans.fit_predict(features_scaled)
        
        df_encoded['cluster'] = clusters
        
        # Analizar patrones de cada cluster
        self._analyze_cluster_patterns(df_encoded)
        
        return df_encoded
    
    def _analyze_cluster_patterns(self, df):
        """
        Analiza los patrones característicos de cada cluster.
        
        Args:
            df: DataFrame con asignación de clusters
        """
        self.cluster_patterns = {}
        
        for cluster_id in range(self.n_clusters):
            cluster_df = df[df['cluster'] == cluster_id]
            
            # Identificar patrones dominantes
            estado_previo_dominante = cluster_df['estado_emocional_previo'].mode()[0] if len(cluster_df) > 0 else None
            microaccion_dominante = cluster_df['microaccion'].mode()[0] if len(cluster_df) > 0 else None
            
            self.cluster_patterns[cluster_id] = {
                'tamaño': len(cluster_df),
                'estado_emocional_previo_dominante': estado_previo_dominante,
                'microaccion_dominante': microaccion_dominante,
                'efectividad_media': cluster_df['efectividad'].mean(),
                'efectividad_normalizada_media': cluster_df['efectividad_normalizada'].mean(),
                'tiempo_aplicacion_medio': cluster_df['tiempo_aplicacion_seg'].mean(),
                'distribucion_estados_previos': cluster_df['estado_emocional_previo'].value_counts().to_dict(),
                'distribucion_microacciones': cluster_df['microaccion'].value_counts().to_dict()
            }
    
    def get_cluster_patterns(self, cluster_id=None):
        """
        Obtiene los patrones de un cluster o de todos.
        
        Args:
            cluster_id: ID del cluster (opcional)
            
        Returns:
            Patrones del cluster o de todos los clusters
        """
        if cluster_id is not None:
            return self.cluster_patterns.get(cluster_id, None)
        return self.cluster_patterns
    
    def interpret_clusters(self):
        """
        Interpreta los clusters identificados.
        
        Returns:
            DataFrame con interpretación de clusters
        """
        interpretations = []
        
        for cluster_id, patterns in self.cluster_patterns.items():
            interpretations.append({
                'cluster_id': cluster_id,
                'tamaño': patterns['tamaño'],
                'patron_principal': f"{patterns['estado_emocional_previo_dominante']} → {patterns['microaccion_dominante']}",
                'efectividad_media': round(patterns['efectividad_media'], 3),
                'efectividad_normalizada_media': round(patterns['efectividad_normalizada_media'], 3),
                'tiempo_aplicacion_medio_seg': round(patterns['tiempo_aplicacion_medio'], 1)
            })
        
        return pd.DataFrame(interpretations).sort_values('efectividad_media', ascending=False)
