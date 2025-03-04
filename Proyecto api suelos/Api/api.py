import os
import pandas as pd
import numpy as np


def cargar_datos():
    ruta_excel = os.path.join(os.path.dirname(__file__), "..", "resultado_laboratorio_suelo.xlsx")
    try:
        df = pd.read_excel(ruta_excel)

        df['Departamento'] = df['Departamento'].str.upper().str.strip()
        df['Municipio'] = df['Municipio'].str.upper().str.strip()



        return df
    except FileNotFoundError:
        print(f"Archivo no encontrado en {ruta_excel}")
        return None


def filtrar_datos(df, departamento, municipio, cultivo, limit):
    """Filtra los datos y reemplaza valores 'ND' con NaN antes de imputar valores faltantes en pH, Fósforo y Potasio."""

    departamento = departamento.upper().strip()
    municipio = municipio.upper().strip()

    limit = min(limit, 1000)

    columnas_requeridas = [
        'Departamento', 'Municipio', 'Cultivo', 'Topografia',
        'pH agua:suelo 2,5:1,0', 'Fósforo (P) Bray II mg/kg', 'Potasio (K) intercambiable cmol(+)/kg'
    ]


    print(departamento, municipio, cultivo)
    
    df_filtrado = df[
        (df['Departamento'] == departamento) &
        (df['Municipio'] == municipio) &
        (df['Cultivo'] == cultivo)
        ][columnas_requeridas].head(limit)

    if df_filtrado.empty:
        print("No se encontraron datos para la consulta realizada.")
        return df_filtrado

    columnas_a_imputar = ['pH agua:suelo 2,5:1,0', 'Fósforo (P) Bray II mg/kg', 'Potasio (K) intercambiable cmol(+)/kg']

    df_filtrado.replace("ND", np.nan, inplace=True)

    for columna in columnas_a_imputar:
        if df_filtrado[columna].dtype == 'object':
            df_filtrado[columna] = df_filtrado[columna].astype(str).str.replace(',', '.').str.strip()
        df_filtrado[columna] = pd.to_numeric(df_filtrado[columna], errors='coerce')

    df_filtrado[columnas_a_imputar] = df_filtrado[columnas_a_imputar].astype(float)

    for columna in columnas_a_imputar:
        df_filtrado[columna] = df_filtrado[columna].fillna(df_filtrado[columna].median())

    return df_filtrado

def calcular_mediana(df):
    """Calcula la mediana de las variables edáficas."""
    return {
        "pH agua:suelo 2,5:1,0": df["pH agua:suelo 2,5:1,0"].median(),
        "Fósforo (P) Bray II mg/kg": df["Fósforo (P) Bray II mg/kg"].median(),
        "Potasio (K) intercambiable cmol(+)/kg": df["Potasio (K) intercambiable cmol(+)/kg"].median()
    }
