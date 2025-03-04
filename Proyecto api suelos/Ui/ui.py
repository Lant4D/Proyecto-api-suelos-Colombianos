def pedir_datos_usuario():
    print("-----------------------Análisis de suelos en Colombia------------------------\n")
    departamento = input("Ingrese el departamento: ").strip().upper()
    municipio = input("Ingrese el municipio: ").strip().upper()
    cultivo = input("Ingrese el cultivo: ").strip().lower().capitalize()

    try:
        limit = int(input("Ingrese el número de registros a consultar: "))
    except ValueError:
        print("El límite debe ser un número entero.")
        return None
    
    print("\n\n-----------------------Datos obtenidos------------------------\n")

    return departamento, municipio, cultivo, limit

def mostrar_resultados(df_filtrado, medianas):
    print("\nResultados:")
    print(df_filtrado[['Departamento', 'Municipio', 'Cultivo', 'Topografia']])
    print("\nMediana de variables edáficas:")
    for key, value in medianas.items():
        print(f"{key}: {value}")
    return