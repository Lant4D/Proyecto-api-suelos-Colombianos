from Api import api
from Ui import ui

def main():
    df = api.cargar_datos()

    if df is None:
        return

    datos_usuario = ui.pedir_datos_usuario()
    if datos_usuario is None:
        return

    departamento, municipio, cultivo, limit = datos_usuario
    df_filtrado = api.filtrar_datos(df, departamento, municipio, cultivo, limit)

    if df_filtrado.empty:
        print("No se encontraron datos para la consulta realizada.")
        return

    medianas = api.calcular_mediana(df_filtrado)

    ui.mostrar_resultados(df_filtrado, medianas)

if __name__ == "__main__":
    main()
 