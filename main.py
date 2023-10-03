import pandas as pd

"""Se indican los archivos con los que se va a trabajar
"""

# Se especifican las rutas de los archivos CSV conque se van a trabajar
file_path = 'Data/Datos_csv/reviews_nlp.csv'
file_path1 = 'Data/Datos_csv/games.csv'



# Se leen los archivos CSV y crean los DataFrame
reviews = pd.read_csv(file_path, parse_dates= ['posted'])
games = pd.read_csv(file_path1, parse_dates= ['release_date'])





"""
Se crean las funciones para los endpoints
"""


def UsersRecommend1(año: int):
    # Filtrar reseñas por año, recomendación y comentarios positivos/neutrales
    filtered_reviews = reviews[(reviews['posted'].dt.year == año) &
                                  (reviews['recommend'] == True) &
                                  (reviews['sentiment_analysis'].isin([1, 2]))]
    
    # Contar la cantidad de reseñas para cada juego
    game_counts = filtered_reviews['item_id'].value_counts()
    
    # Filtrar los item_id que están en el DataFrame games
    filtered_game_counts = game_counts[game_counts.index.isin(games['item_id'])]

    # Obtener los top 3 juegos menos recomendados
    top_3_games = filtered_game_counts.head(3)

    # Crear una lista de diccionarios con los juegos y sus puestos
    result = [{"Puesto {}: {}".format(i+1, games.loc[item_id]['app_name']) : item_id}
              for i, item_id in enumerate(top_3_games)]
    
    return result


def UsersNotRecommend1(año: int):
    # Filtrar reseñas por año, no recomendación y sentimiento negativo
    filtered_reviews = reviews[(reviews['posted'].dt.year == año) &
                                  (reviews['recommend'] == False) &
                                  (reviews['sentiment_analysis'] == 0)]
    
    # Contar la cantidad de reseñas negativas para cada juego
    game_counts = filtered_reviews['item_id'].value_counts()
       
    # Filtrar los item_id que están en el DataFrame games
    filtered_game_counts = game_counts[game_counts.index.isin(games['item_id'])]

    # Obtener los top 3 juegos menos recomendados
    top_3_games = filtered_game_counts.head(3)

    # Crear una lista de diccionarios con los juegos y sus puestos
    result = [{"Puesto {}: {}".format(i+1, games.loc[item_id]['app_name']) : item_id}
              for i, item_id in enumerate(top_3_games)]
    
    return result


def sentiment_analysis1(Año : int):
    # Convierte la cadena de fecha de entrada a un objeto datetime
    target_date = pd.to_datetime(Año)
    
    # Filtra las reseñas que coincidan con el año objetivo
    filtered_reviews = reviews[reviews['posted'].dt.year == target_date.year]
    
    # Realiza el conteo de las categorías de sentimiento
    sentiment_counts = filtered_reviews['sentiment_analysis'].value_counts()
    
    # Crea una lista con los recuentos de categorías
    result_list = f'Negative = {sentiment_counts.get(0, 0)}, Neutral = {sentiment_counts.get(1, 0)}, Positive = {sentiment_counts.get(2, 0)}'
    
     # Crear un diccionario con los resultados
    results1 = {
        f"Para el año de lanazamiento {Año} se registraron las siguientes reseñas por categoria: {result_list}" 
    }    
    return results1


"""
Definimos y entrenamos el sistema de recomendacion
"""

import joblib

# Cargar el modelo
algo = joblib.load('modelo_surprise.pkl')


# Supongamos que tenemos un usuario de interés con user_id = 'tu_usuario'
def recomendacion_usuario1(id_de_usuario: str):

    # Encuentra los usuarios más similares al usuario de interés
    similar_users = algo.get_neighbors(algo.trainset.to_inner_uid(id_de_usuario), k=10)

    # Filtra las reseñas de los usuarios similares
    reviews_similares = reviews[reviews['user_id'].isin([algo.trainset.to_raw_uid(uid) for uid in similar_users])]

    # Filtra las reseñas de juegos que han sido recomendados (recommend=True)
    juegos_recomendados = reviews_similares[reviews_similares['recommend']]

    # Obtén la lista de juegos recomendados por usuarios similares
    juegos_recomendados_lista = juegos_recomendados['item_id'].unique()

    # Inicializa una lista vacía para almacenar los juegos encontrados
    juegos_encontrados = []

    # Itera a través de la lista de juegos recomendados
    for juego_id in juegos_recomendados_lista:
        # Busca el juego en el DataFrame games
        juego = games[games['item_id'] == juego_id]
        
        # Si se encuentra el juego, agrégalo a la lista de juegos encontrados
        if not juego.empty:
            juegos_encontrados.append(juego[['item_id', 'app_name']])  # Agrega solo las columnas "item_id" y "app_name" del juego encontrado

        # Si ya hemos encontrado 5 juegos, detén el bucle
        if len(juegos_encontrados) == 5:
            break

    # Convierte la lista de juegos encontrados en un DataFrame
    juegos_encontrados_df = pd.concat(juegos_encontrados, ignore_index=True)

    # Imprime el DataFrame de juegos encontrados con las columnas "item_id" y "app_name"
    juegos_encontrados = juegos_encontrados_df[['item_id', 'app_name']].to_dict(orient='records')
    return juegos_encontrados


from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

@app.get("/UsersRecommend/{Anio}")
def UsersRecommend(Año: int):
    return UsersRecommend1(Año)

@app.get("/UsersNotRecommend/{Anio}")
def UsersNotRecommend(Año: int):
    return UsersNotRecommend1(Año)

@app.get("/sentiment_analysis/{Anio}")
def sentiment_analysis(Año: int):
    return sentiment_analysis1(Año)

@app.get("/recomendacion_usuario/{id_de_usuario}")
def recomendacion_usuario(id_de_usuario: str):
    return recomendacion_usuario1(id_de_usuario)