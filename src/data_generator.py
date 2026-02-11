"""
Generador de datos sintéticos para el análisis de microacciones y estados emocionales.
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta


class EmotionalDataGenerator:
    """Genera datos sintéticos de usuarios, estados emocionales y microacciones."""
    
    def __init__(self, seed=42):
        """
        Inicializa el generador de datos.
        
        Args:
            seed: Semilla para reproducibilidad
        """
        np.random.seed(seed)
        self.estados_emocionales = ['alegría', 'tristeza', 'ansiedad', 'calma', 'frustración']
        self.microacciones = ['respiración_profunda', 'pausa_breve', 'cambio_postura', 
                             'escuchar_música', 'ejercicio_visual']
    
    def generar_datos(self, n_usuarios=100, n_eventos_por_usuario=50):
        """
        Genera un dataset sintético de usuarios con eventos emocionales y microacciones.
        
        Args:
            n_usuarios: Número de usuarios a generar
            n_eventos_por_usuario: Número de eventos por usuario
            
        Returns:
            DataFrame con los datos generados
        """
        datos = []
        
        for usuario_id in range(n_usuarios):
            # Cada usuario tiene patrones personales
            preferencia_emocional = np.random.choice(self.estados_emocionales)
            sesgo_efectividad = np.random.uniform(0.3, 0.7)
            
            fecha_inicio = datetime.now() - timedelta(days=30)
            
            for evento in range(n_eventos_por_usuario):
                # Estado emocional previo
                if np.random.random() < 0.3:
                    estado_previo = preferencia_emocional
                else:
                    estado_previo = np.random.choice(self.estados_emocionales)
                
                # Microacción aplicada
                microaccion = np.random.choice(self.microacciones)
                
                # Efectividad basada en el estado emocional
                efectividad_base = self._calcular_efectividad_base(estado_previo, microaccion)
                efectividad = np.clip(efectividad_base + np.random.normal(0, 0.15) + 
                                     (sesgo_efectividad - 0.5), 0, 1)
                
                # Métricas adicionales
                tiempo_aplicacion = np.random.uniform(30, 300)  # segundos
                estado_posterior = self._determinar_estado_posterior(estado_previo, efectividad)
                
                # Timestamp
                timestamp = fecha_inicio + timedelta(hours=evento * 2)
                
                datos.append({
                    'usuario_id': f'user_{usuario_id:03d}',
                    'timestamp': timestamp,
                    'estado_emocional_previo': estado_previo,
                    'microaccion': microaccion,
                    'efectividad': efectividad,
                    'tiempo_aplicacion_seg': tiempo_aplicacion,
                    'estado_emocional_posterior': estado_posterior,
                    'percepcion_consciente': np.random.uniform(0, 1)
                })
        
        return pd.DataFrame(datos)
    
    def _calcular_efectividad_base(self, estado, microaccion):
        """Calcula la efectividad base según patrones conocidos."""
        # Patrones de efectividad según estado-microacción
        patrones = {
            'ansiedad': {
                'respiración_profunda': 0.8,
                'pausa_breve': 0.6,
                'cambio_postura': 0.4,
                'escuchar_música': 0.7,
                'ejercicio_visual': 0.5
            },
            'tristeza': {
                'respiración_profunda': 0.5,
                'pausa_breve': 0.4,
                'cambio_postura': 0.6,
                'escuchar_música': 0.8,
                'ejercicio_visual': 0.3
            },
            'alegría': {
                'respiración_profunda': 0.6,
                'pausa_breve': 0.7,
                'cambio_postura': 0.7,
                'escuchar_música': 0.8,
                'ejercicio_visual': 0.6
            },
            'calma': {
                'respiración_profunda': 0.7,
                'pausa_breve': 0.8,
                'cambio_postura': 0.5,
                'escuchar_música': 0.6,
                'ejercicio_visual': 0.7
            },
            'frustración': {
                'respiración_profunda': 0.7,
                'pausa_breve': 0.5,
                'cambio_postura': 0.8,
                'escuchar_música': 0.5,
                'ejercicio_visual': 0.4
            }
        }
        
        return patrones.get(estado, {}).get(microaccion, 0.5)
    
    def _determinar_estado_posterior(self, estado_previo, efectividad):
        """Determina el estado posterior según la efectividad."""
        if efectividad > 0.7:
            estados_positivos = ['alegría', 'calma']
            return np.random.choice(estados_positivos)
        elif efectividad < 0.3:
            return estado_previo
        else:
            return np.random.choice(self.estados_emocionales)
