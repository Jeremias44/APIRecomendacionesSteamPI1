from fastapi import FastAPI
import pandas as pd
import numpy as np
from datetime import datetime

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import pairwise_distances
from sklearn.impute import SimpleImputer
from sklearn.cluster import KMeans


app = FastAPI()

# Saludo
@app.get('/')
def saludo():
    return {'Hola, te doy la bienvenida a Steam': 'Podrás realizar las siguientes consultas',
'1) userdata(user_id: str)': 'devuelve',
'2) countreviews(fecha1: str,fecha2: str)': 'devuelve',
'3) genre(genero: str)': 'devuelve',
'4) userforgenre(genero: str)': 'devuelve',
'5) developer(desarrollador: str)' : 'devuelve',
'6) sentiment_analysis(año: int)' : 'devuelve',
'7) recomendacion_juego(item_id: int)' : 'devuelve'
}

# Función 1
@app.get('/userdata')
def userdata(user_id: str): 
    #Cantidad de dinero gastado
    df = pd.read_csv(r'1userdata.csv')
    dinero_gastado = sum(df.price[df.user_id == user_id])
    #Porcentaje de recomendación
    df2 = pd.read_csv(r'reviews_desanidado.csv')
    recomendaciones_positivas = df2.recommend[df2.user_id == user_id].sum()
    recomendaciones_totales = df2.recommend[df2.user_id == user_id].count()
    porcentaje_recomendaciones = round((recomendaciones_positivas/recomendaciones_totales)*100,2)
    #Cantidad de items
    cantidad_items = df.items_count[df.user_id == user_id].max()
    return {'dinero gastado por el usuario': round(dinero_gastado,2),
            'porcentaje de recomendaciones positivas': porcentaje_recomendaciones,
            'cantidad de items del usuario': cantidad_items}

# Función 2
@app.get('/countreviews')
def countreviews(fecha1: str,fecha2: str):
    fecha1 = datetime.strptime(fecha1, "%Y-%m-%d")
    fecha2 = datetime.strptime(fecha2, "%Y-%m-%d")

    # Cantidad de usuarios que recomendaron entre fecha1 y fecha2
    reviews = pd.read_csv(r'reviews_desanidado.csv')
    # Convierto los valores a tipo datetime
    reviews['posted'] = pd.to_datetime(reviews['posted'], errors='coerce')
    # Obtengo la cantidad de usuarios únicos que postearon reviews entre fecha1 y fecha2
    cantidad_usuarios = len(reviews.user_id[(fecha1 < reviews.posted) & (fecha2 > reviews.posted)].unique())
    # Porcentaje de recomendaciones de estos usuarios
    lista_user = reviews.user_id[(fecha1 < reviews.posted) & (fecha2 > reviews.posted)].unique()
    recomendaciones_positivas = reviews.recommend[reviews.user_id.isin(lista_user)].sum()
    recomendaciones_totales = reviews.recommend[reviews.user_id.isin(lista_user)].count()
    porcentaje_recomendaciones = round((recomendaciones_positivas/recomendaciones_totales)*100,2)

    return {'cantidad de usuarios': cantidad_usuarios,
            'porcentaje de recomendaciones de los usuarios': porcentaje_recomendaciones}

# Función 3
@app.get('/genre')
def genre(genero: str):
    ranking = [('Action', 1), ('Indie', 2), ('RPG', 3), ('Adventure', 4), ('Simulation', 5), ('Strategy', 6), ('Free to Play', 7),
    ('Massively Multiplayer', 8), ('Casual', 9), ('Early Access', 10), ('Sports', 11), ('Racing', 12), ('Utilities', 13),
    ('Web Publishing', 14), ('Design &amp; Illustration', 15), ('Animation &amp; Modeling', 16), ('Video Production', 17),
    ('Education', 18), ('Software Training', 19), ('Audio Production', 20), ('Photo Editing', 21)]

    for genre_tuple in ranking:
        if genre_tuple[0] == genero:
            puesto = genre_tuple[1]
            break  # Se rompe el bucle una vez que se encuentra el género

    return {f'El género "{genero}" se encuentra en el puesto del ranking': puesto}

# Función 4
@app.get('/userforgenre')
def userforgenre(genero: str):
    grouped_data = pd.read_csv(r'4userforgenre.csv')
    sorted_grouped_data = grouped_data.sort_values(by=genero, ascending=False)
    # Obtengo los cinco primeros registros y selecciono las columnas deseadas
    top_records = sorted_grouped_data.head(5)[['user_id', 'user_url']]
    # Creo un diccionario con la estructura deseada
    result_dict = {}
    count = 1
    for _, row in top_records.iterrows():
        result_dict[f'usuario {count}'] = [row['user_id'], row['user_url']]
        count += 1
    
    return result_dict

# Función 5
@app.get('/developer')
def developer(desarrollador: str):
    g_año = pd.read_csv(r'5developer.csv')
    # Filtro el DataFrame por el desarrollador deseado
    g_año_filtrado = g_año[g_año['developer'] == desarrollador]
    # Agrupo los datos por año y realizo las operaciones de conteo y porcentaje
    g_año_agrupado = g_año_filtrado.groupby('año').agg(
    Cantidad_Items=('contador', 'sum'),
    Porcentaje_Contenido_Free=('price', lambda x: round((x == 0.00).mean() * 100, 2))
    )
    # Convierto el DataFrame en un diccionario clave-valor
    dicc_agrupado = g_año_agrupado.reset_index().to_dict(orient='records')

    return dicc_agrupado

# Función 6
@app.get('/sentiment_analysis')
def sentiment_analysis(año: int):
    año_reviews = pd.read_csv(r'6sentiment_analysis.csv')
    negativo = año_reviews[año_reviews['año'] == año].iloc[0][1]
    neutral = año_reviews[año_reviews['año'] == año].iloc[0][2]
    positivo = año_reviews[año_reviews['año'] == año].iloc[0][3]
        
    return {'negativo': negativo, 'neutral': neutral, 'positivo': positivo}

# Función 7
@app.get('/recomendacion_juego')
def recomendacion_juego(item_id: int):
    df_7 = pd.read_csv(r'7recomendacion_juego.csv')

    # Imputo los valores faltantes con 0
    imputer = SimpleImputer(strategy='constant', fill_value=0)
    df_7i = imputer.fit_transform(df_7.drop('item_id', axis=1))  # Elimino la columna 'item_id'
    # Convierto el array NumPy en un DataFrame de pandas
    df_7i = pd.DataFrame(df_7i, columns=df_7.columns[1:])  # Ignoro la columna 'item_id'

    # Creo una instancia de KMeans
    kmeans = KMeans(n_clusters=5, random_state=0)
    # Entreno el modelo con los datos
    kmeans.fit(df_7i)
    # Obtengo las etiquetas de los clusters asignados a cada fila
    etiquetas_clusters = kmeans.labels_


    # Paso 1: Obtengo el índice del item_id en el DataFrame original
    indice_item_id = df_7[df_7['item_id'] == item_id].index[0]
    # Paso 2: Encuentro a qué cluster pertenece el item_id
    cluster_item_id = etiquetas_clusters[indice_item_id]
    # Paso 3: Filtro los índices de los item_id en el mismo cluster
    indices_mismo_cluster = np.where(etiquetas_clusters == cluster_item_id)[0]
    # Paso 4: Calculo las distancias y obtengo los índices de los 5 más cercanos
    distancias = pairwise_distances(df_7i.iloc[indice_item_id].values.reshape(1, -1), df_7i.iloc[indices_mismo_cluster])
    indices_cercanos = np.argsort(distancias)[0][:6]
    # Paso 5: Obtengo los item_id de los 5 más cercanos
    id_cercanos = df_7.iloc[indices_mismo_cluster[indices_cercanos]]['item_id']

    
    return {'5 item_id recomendados': [id_cercanos.iloc[1], id_cercanos.iloc[2], id_cercanos.iloc[3], id_cercanos.iloc[4], id_cercanos.iloc[5]]}