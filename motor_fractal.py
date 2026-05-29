import numpy as np

class MetaPatternFractal:
    def __init__(self, max_iter=250):
        self.max_iter = max_iter
        # Límites estrictos del plano complejo de Mandelbrot
        self.x_min, self.x_max = -2.0, 0.5
        self.y_min, self.y_max = -1.2, 1.2

    def transformar_secuencia(self, secuencia):
        """
        Transforma una secuencia numérica en coordenadas (X, Y) únicas.
        Aplicando la corrección de pesos posicionales (np.dot) para que 
        el orden de los números altere drásticamente el resultado.
        """
        datos = np.array(secuencia, dtype=float)
        n = len(datos)
        
        if n == 0:
            return 0.0, 0.0
            
        # Dividimos la secuencia en dos mitades
        mitad = n // 2
        if n % 2 != 0 and n > 1:
            parte_x = datos[:mitad+1]
            parte_y = datos[mitad:]
        elif n == 1:
            parte_x = datos
            parte_y = datos
        else:
            parte_x = datos[:mitad]
            parte_y = datos[mitad:]

        # SOLUCIÓN CHATGPT: Pesos dinámicos basados en la posición (1, 2, 3...)
        pesos_x = np.arange(1, len(parte_x) + 1, dtype=float)
        pesos_y = np.arange(1, len(parte_y) + 1, dtype=float)

        # Producto punto para garantizar que [10, 20] != [20, 10]
        dot_x = np.dot(parte_x, pesos_x)
        dot_y = np.dot(parte_y, pesos_y)

        # Normalización no lineal usando funciones trigonométricas escaladas a [0, 1]
        hash_x = (np.sin(dot_x) + 1.0) / 2.0
        hash_y = (np.cos(dot_y) + 1.0) / 2.0

        # Proyección exacta en el espacio de Mandelbrot
        x_coord = self.x_min + (self.x_max - self.x_min) * hash_x
        y_coord = self.y_min + (self.y_max - self.y_min) * hash_y

        return x_coord, y_coord

    def calibrar_escape(self, x, y):
        """
        Mapea el punto en la ecuación fundamental Z_{n+1} = Z_n^2 + c
        Devuelve métricas puras de ingeniería.
        """
        c = complex(x, y)
        z = 0j
        for i in range(self.max_iter):
            z = z**2 + c
            if abs(z) > 2.0:
                return i
        return self.max_iter

    def clasificar_metrica(self, iteraciones):
        """
        Clasificación técnica basada en la densidad de escape.
        """
        if iteraciones == self.max_iter:
            return "INTERIOR_MANDELBROT", "Estable (Cuerpo Central)"
        elif iteraciones >= 150:
            return "TRANSICION_ALTA", "Frontera Compleja (Bordes/Filamentos)"
        elif iteraciones >= 50:
            return "TRANSICION_BAJA", "Transición Rápida"
        else:
            return "ESCAPE_RAPIDO", "Zona de Dispersión (Exterior/Caos)"
