# Fecha: 15/03/2025
# Descripción: Herramienta que procesa las descargas del ideam en archivos individuales más livianos

import os
import pandas as pd

dir = {
    'Crudos': 'unprocessed_data',
    'Procesados': 'data',
    'Catalogo': 'library/IDEAM_catalog.csv',
    'Resultados' : 'output'
    }

def organizar_crudos(): # Organizar los archivos crudos en un dataframe
    
    # Listar los .csv de los crudos ubicados en el directorio
    lista = []
    for archivo in os.listdir(dir.get('Crudos')):
        if archivo.endswith('.csv'):
            # Leer el archivo CSV
            df = pd.read_csv(os.path.join(dir.get('Crudos'), archivo))

            # Tomar la información disponible de la estación
            nombre = df['NombreEstacion'].iloc[0]
            nombre = " ".join(nombre.replace(',', ' ').split())
            fecha_inicio = pd.to_datetime(df['Fecha'].iloc[0], errors='coerce')
            fecha_fin = pd.to_datetime(df['Fecha'].iloc[-1], errors='coerce')

            variable = df['Parametro'].iloc[0]
            if variable == 'Día pluviométrico (convencional)': variable = 'Día pluviométrico'
            if variable == 'Temperatura mínima diaria': variable = 'Temperatura mínima diaria'
            if variable == 'Temperatura máxima diaria': variable = 'Temperatura máxima diaria'

            # Agregar los valores a la lista
            lista.append([archivo, nombre, variable, fecha_inicio, fecha_fin])

    # Crear un DataFrame con los resultados y los organiza por nombre y fecha
    df_crudos = pd.DataFrame(lista, columns=['Archivo', 'Nombre estacion', 'Variable', 'Fecha inicio', 'Fecha fin'])
    df_crudos = df_crudos.sort_values(by=['Nombre estacion', 'Fecha inicio']).reset_index(drop=True)
    df_crudos.index = df_crudos.index + 1

    # Darle formato de fecha a las columnas
    df_crudos['Fecha inicio'] = df_crudos['Fecha inicio'].dt.strftime('%Y-%m-%d')
    df_crudos['Fecha fin'] = df_crudos['Fecha fin'].dt.strftime('%Y-%m-%d')

    return df_crudos

def resumir_crudos(): # Resumir y complementar información de las estaciones

    # Agrupar dataframe de los crudos por nombre de estación, su fecha de inicio y fecha de fin
    df_procesados = df_crudos.groupby('Nombre estacion').agg({'Variable': 'first' , 'Fecha inicio': 'min', 'Fecha fin': 'max'}).reset_index()

    # Crear dataframe donde añadiremos los parametros que hacen falta de cada estación
    df_parametros = pd.DataFrame(columns=['Codigo', 'Latitud', 'Longitud', 'Departamento', 'Municipio', 'Area hidrografica'])

    # Buscar en el catalogo los parámetros que hacen falta de cada estación
    df_catalogo = pd.read_csv(dir.get('Catalogo'), sep=';', encoding='latin1')
    df_catalogo = df_catalogo.replace(',', ' ', regex=True).replace(r'\s+', ' ', regex=True)

    for Estacion in df_procesados['Nombre estacion']:
        indice = df_catalogo[df_catalogo['NOMBRE'] == Estacion].index[0]
        df_parametros.loc[len(df_parametros)] = [df_catalogo.loc[indice, 'CODIGO'],
                                                round(float(df_catalogo.loc[indice, 'LATITUD']), 6),
                                                round(float(df_catalogo.loc[indice, 'LONGITUD']), 6),
                                                df_catalogo.loc[indice, 'DEPARTAMENTO'],
                                                df_catalogo.loc[indice, 'MUNICIPIO'],
                                                df_catalogo.loc[indice, 'AREA_HIDROGRAFICA']]

    # Pegar la información encontrada en el dataframe del resumen procesado
    df_procesados.insert(0, 'Codigo', df_parametros['Codigo'])
    df_procesados = df_procesados.join(df_parametros.iloc[:, 1:])
    df_procesados.index = df_procesados.index + 1

    return df_procesados

def comprimir_mediciones(): # Crear archivos individuales livianos por estación
    
    # Iterar sobre cada estación para crear archivos individuales livianos
    for Estacion in df_procesados['Nombre estacion']:

        # Crear dataframe donde añadiremos los resultados
        df_estacion = pd.DataFrame(columns=['Fecha', 'Valor'])
        
        # Determinar los indices asociados a la estación en el dataframe del resumen de los crudos (para tomar los archivos asociados a esa estación)
        indice = df_crudos[df_crudos['Nombre estacion'] == Estacion].index

        # Iterar sobre cada indice en el resumen crudo de la misma estación, abrir el archivo crudo de esa estación y extraer las mediciones
        for i in indice:
            ruta_archivo = os.path.join(dir.get('Crudos'), df_crudos.loc[i, 'Archivo'])
            df = pd.read_csv(ruta_archivo)
            df2 = pd.DataFrame({'Fecha': pd.to_datetime(df['Fecha']).dt.strftime('%Y-%m-%d'),
                                'Valor': df['Valor']})

            df_estacion = pd.concat([df_estacion, df2], ignore_index=True)

        # Exportar archivo individual .csv
        id = Estacion.split(' [')[0] + ' (' + Estacion.split(' [')[1].split(']')[0] + ')' 
        df_estacion.to_csv(os.path.join(dir.get('Procesados'), id + '.csv'), index=False, header=True, encoding='utf-8-sig', sep=",")

def output(): # Crear excel con los resultados y abrirlo

    df_crudos.to_csv(os.path.join(dir.get('Resultados'), 'raw_data' + '.csv'), index=False, header=True, encoding='utf-8-sig', sep=",")

    df_procesados.to_csv(os.path.join(dir.get('Resultados'), 'processed_data' + '.csv'), index=False, header=True, encoding='utf-8-sig', sep=",")

df_crudos = organizar_crudos()

df_procesados = resumir_crudos()

comprimir_mediciones()

output()

os.system('cls' if os.name == 'nt' else 'clear')
print('Execution completed\nGo to the root of the “output” folder and move the files to the corresponding subfolder.')