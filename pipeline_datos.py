import pandas as pd
from motor_fractal import MetaPatternFractal

# Instanciamos el motor
motor = MetaPatternFractal()

# 1. Simulación de tu base de datos de entrada (Sorteos, combinaciones o secuencias)
# Aquí puedes cargar tu DataFrame real: df = pd.read_csv('mis_sorteos.csv')
datos_historicos = [
    {"id_sorteo": 1, "combinacion": [10, 20, 30, 40, 51], "tipo": "Historico"},
    {"id_sorteo": 2, "combinacion": [20, 10, 30, 40, 51], "tipo": "Historico"}, # Mismos números, orden inverso
    {"id_sorteo": 3, "combinacion": [7, 1, 2, 2, 11], "tipo": "Sincronicidad_7122"},
]

# 2. Pipeline de procesamiento
registros_procesados = []

for item in datos_historicos:
    secuencia = item["combinacion"]
    
    # Ejecutar calibración geométrica
    x, y = motor.transformar_secuencia(secuencia)
    iter_escape = motor.calibrar_escape(x, y)
    id_tecnico, desc_tecnica = motor.clasificar_metrica(iter_escape)
    
    # Estructura limpia para la Base de Datos
    registro = {
        "id_elemento": item["id_sorteo"],
        "secuencia_origen": str(secuencia),
        "tipo_analisis": item["tipo"],
        "coor_x": round(x, 6),
        "coor_y": round(y, 6),
        "iter_escape": iter_escape,
        "clase_tecnica": id_tecnico,
        "descripcion": desc_tecnica
    }
    registros_procesados.append(registro)

# Convertir a DataFrame de Pandas (Listo para guardar en SQL, NoSQL o CSV)
df_fractal = pd.DataFrame(registros_procesados)

print("=== MATRIZ GEOMÉTRICA DE DATOS GENERADA ===")
print(df_fractal.to_string(index=False))
