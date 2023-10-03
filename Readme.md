# Proyecto de Análisis de Reseñas y Sistema de Recomendación

Este proyecto se enfoca en el análisis de reseñas de usuarios y en la implementación de un sistema de recomendación basado en algoritmos de filtrado colaborativo. El objetivo principal es proporcionar información valiosa a los usuarios y ayudarles a descubrir nuevos juegos o aplicaciones que podrían interesarles.

## Tabla de Contenidos

- [Archivos de Datos](#archivos-de-datos)
- [Funciones de los Endpoints](#funciones-de-los-endpoints)
- [Configuración del Sistema de Recomendación](#configuración-del-sistema-de-recomendación)
- [Ejecución del Proyecto](#ejecución-del-proyecto)
- [Autor](#autor)
- [Contribuciones](#contribuciones)
- [Licencia](#licencia)
- [Agradecimientos](#agradecimientos)

## Archivos de Datos

En este proyecto, trabajamos con tres archivos CSV que contienen información relevante:

1. `reviews_nlp.csv`: Este archivo contiene las reseñas de usuarios, incluyendo detalles como la fecha de publicación, el usuario, el ID del artículo y la recomendación.

2. `games.csv`: Este archivo proporciona información sobre los juegos o aplicaciones, incluyendo su fecha de lanzamiento, desarrollador y otros detalles importantes.

3. `df_train_filtrado.csv`: Este archivo es utilizado para entrenar el sistema de recomendación y contiene datos de usuarios, ítems y recomendaciones.

Asegúrate de que estos archivos estén ubicados en el directorio `Data/Datos_csv` para que el código pueda acceder a ellos correctamente.

## Funciones de los Endpoints

Hemos implementado una serie de endpoints que proporcionan información y funcionalidad útiles a los usuarios:

- `/UsersRecommend/{Anio}`: Esta función toma un año como entrada y filtra las reseñas de usuarios que recomendaron el juego (recommend=True) y tienen sentimientos positivos o neutrales.
Luego, cuenta la cantidad de reseñas para cada juego y filtra los juegos cuyos ID están presentes en el DataFrame "games".
Obtiene los 3 juegos más recomendados y crea una lista de diccionarios que contiene el puesto y el nombre de cada juego.
Devuelve esta lista como resultado.

- `/UsersNotRecommend/{Anio}`: Similar a la función anterior, pero filtra las reseñas de usuarios que no recomendaron el juego (recommend=False) y tienen sentimientos negativos.
Luego, cuenta la cantidad de reseñas negativas para cada juego y filtra los juegos cuyos ID están presentes en el DataFrame "games".
Obtiene los 3 juegos menos recomendados y crea una lista de diccionarios que contiene el puesto y el nombre de cada juego.
Devuelve esta lista como resultado.

- `/sentiment_analysis/{Anio}`: Esta función toma un año como entrada y filtra las reseñas que coinciden con ese año.
Luego, realiza un conteo de las categorías de sentimiento ("Negative", "Neutral" y "Positive") en las reseñas.
Devuelve un diccionario con los recuentos de cada categoría de sentimiento en el formato {Negative: n, Neutral: n, Positive: n}.

- `/recomendacion_usuario/{id_de_usuario}`: Esta función toma el ID de un usuario como entrada y utiliza un modelo de recomendación previamente entrenado (usando la biblioteca Surprise) para encontrar usuarios similares al usuario de interés.
Luego, filtra las reseñas de los usuarios similares y selecciona las reseñas de juegos que han sido recomendados (recommend=True) por esos usuarios.
Obtiene una lista de juegos recomendados por usuarios similares y selecciona los primeros 5 juegos encontrados.
Devuelve una lista de diccionarios que contienen el ID y el nombre de estos juegos encontrados.

## Configuración del Sistema de Recomendación

Hemos utilizado la biblioteca Surprise para implementar el sistema de recomendación. El proceso de entrenamiento se realiza de la siguiente manera:

1. Configuramos el lector y la escala de calificación para nuestros datos.

2. Cargamos los datos del DataFrame `df_train_filtrado`, que contiene información sobre usuarios, ítems y recomendaciones.

3. Dividimos los datos en conjuntos de entrenamiento y prueba.

4. Creamos un modelo KNN (K-Nearest Neighbors) basado en similitud de usuarios.

5. Entrenamos el modelo en el conjunto de entrenamiento.

6. Implementamos una función que encuentra juegos recomendados para un usuario específico.

## Ejecución del Proyecto

Para ejecutar este proyecto, debes seguir los siguientes pasos:

1. Asegúrate de tener instaladas todas las bibliotecas necesarias. Puedes usar `pip install -r requirements.txt` para instalar las dependencias.

2. Ubica los archivos CSV en la carpeta `Data/Datos_csv` o ajusta las rutas de archivo en el código según sea necesario.

3. Ejecuta la aplicación FastAPI utilizando el comando `uvicorn main:app --reload`. La aplicación se ejecutará en `http://localhost:8000`.

4. Accede a los endpoints mencionados anteriormente en tu navegador o utilizando una herramienta como Postman.

5. Explora los resultados y la funcionalidad proporcionada por el sistema de recomendación y el análisis de reseñas.

¡Disfruta explorando y analizando los datos y recomendaciones! Si tienes alguna pregunta o problema, no dudes en ponerte en contacto con nosotros.

## Autor

Gio M

## Contacto
gio75388gmail.com

## Contribuciones

Las contribuciones a este proyecto son bienvenidas. Si deseas colaborar, no dudes en abrir un problema o enviar una solicitud de extracción.

## Licencia

Este proyecto se encuentra bajo la Licencia MIT