# ============================================
# Script para generar archivo XLS con 5000 registros y errores intencionales
# Autor: Jairo Vargas 
# ============================================

import pandas as pd
import numpy as np
import random

# -------------------------------
# Configuración
# -------------------------------
n = 5000  # número de registros
archivo_salida = "ventas_erroneas.xls"

# -------------------------------
# Generación de datos
# -------------------------------
ciudades = ["Bogotá", "Medellín", "Cali", "Bucaramanga", "Cartagena", None]
categorias = ["Electrónica", "Ropa", "Alimentos", "Hogar", "Juguetes"]

# Fechas válidas + errores
fechas_validas = pd.date_range("2025-01-01", periods=n).tolist()
fechas_erroneas = ["fecha_invalida"] * (n // 20)
fechas_finales = fechas_validas[: n - len(fechas_erroneas)] + fechas_erroneas
random.shuffle(fechas_finales)

# Ventas con errores
ventas = list(np.random.randint(100, 5000, size=n).astype(float))
for i in range(0, n, 200):
    ventas[i] = -abs(ventas[i])  # negativos
for i in range(50, n, 300):
    ventas[i] = None  # nulos
for i in range(100, n, 400):
    ventas[i] = "texto"  # texto en campo numérico

# Unidades con errores
unidades = list(np.random.randint(1, 20, size=n))
for i in range(120, n, 250):
    unidades[i] = 0  # type: ignore # inválidos

# -------------------------------
# Construcción del DataFrame
# -------------------------------
df = pd.DataFrame({
    "Fecha": fechas_finales[:n],
    "Ciudad": [random.choice(ciudades) for _ in range(n)],
    "Categoria": [random.choice(categorias) for _ in range(n)],
    "Ventas": ventas,
    "Unidades": unidades
})

# -------------------------------
# Exportar a XLS
# -------------------------------
# Exportar a XLSX (formato moderno)
df.to_excel("ventas_erroneas.xlsx", index=False, engine="openpyxl")
print(f"Archivo generado: {archivo_salida} ({n} registros con errores)")
