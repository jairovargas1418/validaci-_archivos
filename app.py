# ============================================
# App web (Streamlit) para limpieza y validación de datos .xls/.xlsx
# Autor: Jairo Vargas 
# ============================================

import io
import datetime
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Validación de XLS", page_icon="✅", layout="wide")
st.title("✅ Validación y limpieza de datos")

st.markdown("Sube un archivo Excel, aplica reglas de validación y descarga uno corregido con hoja de errores.")

# -------------------------------
# Función de validación específica
# -------------------------------
def validar_datos(df: pd.DataFrame):
    """
    Aplica reglas específicas:
    - Ventas > 0
    - Unidades > 0 y enteras
    - Fechas válidas (no NaT)
    Devuelve: df_limpio, df_errores
    """
    df = df.copy()

    # Convertir tipos
    df["Ventas"] = pd.to_numeric(df["Ventas"], errors="coerce")
    df["Unidades"] = pd.to_numeric(df["Unidades"], errors="coerce")
    df["Fecha"] = pd.to_datetime(df["Fecha"], errors="coerce", dayfirst=True)

    # Reglas de validación
    errores = (
        (df["Ventas"].isna()) |
        (df["Ventas"] <= 0) |
        (df["Unidades"].isna()) |
        (df["Unidades"] <= 0) |
        (df["Fecha"].isna())
    )

    df_errores = df[errores].copy()
    df_limpio = df[~errores].copy()

    return df_limpio, df_errores

# -------------------------------
# Exportar a Excel con hoja de errores
# -------------------------------
def exportar_excel(df_limpio, df_errores):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
        df_limpio.to_excel(writer, index=False, sheet_name="Datos_Limpios")
        df_errores.to_excel(writer, index=False, sheet_name="Errores")
    buffer.seek(0)
    return buffer

# -------------------------------
# Interfaz Streamlit
# -------------------------------
archivo = st.file_uploader("Sube tu archivo Excel (.xls o .xlsx)", type=["xls", "xlsx"])

if archivo is not None:
    df = pd.read_excel(archivo)

    st.subheader("Vista previa")
    st.dataframe(df.head(20), use_container_width=True)

    if st.button("Validar y limpiar"):
        df_limpio, df_errores = validar_datos(df)

        st.success("Validación completada ✅")
        st.write(f"Filas limpias: {len(df_limpio)}")
        st.write(f"Filas con errores: {len(df_errores)}")

        st.subheader("Errores detectados")
        st.dataframe(df_errores.head(20), use_container_width=True)

        # Exportar archivo corregido
        fecha_str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_archivo = f"datos_validacion_{fecha_str}.xlsx"
        xlsx_bytes = exportar_excel(df_limpio, df_errores)

        st.download_button(
            label="📥 Descargar archivo corregido",
            data=xlsx_bytes,
            file_name=nombre_archivo,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
else:
    st.info("Sube un archivo Excel para comenzar.")
