# Proyecto_Individual_1

Steam, plataforma multinacional de videojuegos.

## API de Sistema de consultas y recomendaciones de juego.

## Introducción

Se precisa disponibilizar una API que de respuesta a una serie de consultas en base a los datos de STEAM reeferidos a usuarios, reseñas y videojuegos.

Las consultas a desarrollar son las siguientes:
1) userdata(user_id: str): Proporcionar cantidad de dinero gastado, porcentaje de recomendaciones positivas y cantidad de items del usuario solicitado.
2) countreviews(fecha1: str,fecha2: str): Proporcionar cantidad de usuarios que dieron opiniones entre las fechas dadas y el porcentaje de recomendaciones positivas.
3) genre(genero: str): Proporcionar el puesto en el que se encuentra el género indicado en el ranking de horas jugadas.
4) userforgenre(genero: str): Proporcionar 5 usuarios con más horas de juego en el género indicado.
5) developer(desarrollador: str): Proporcionar cantidad de items y porcentaje de contenido gratis por año de la empresa indicada.
6) sentiment_analysis(año: int): Proporcionar la cantidad de reseñas del año indicado, categorizadas en positivo, negativo y neutral.
7) recomendacion_juego(item_id: int): Proporcionar una lista con 5 juegos recomendados similares al ingresado.

## Desarrollo y arquitectura

En un principio se cuenta con 3 archivos json:

* australian_user_reviews.json: Contiene datos relacionados a reseñas y recomendaciones.
* australian_users_items.json: Contiene datos relacionados a usuarios, juegos, horas jugadas.
* output_steam_games.json: Contiene datos relacionados a los videojuegos, empresas desarrolladoras, género del juego.

Se realiza ETL de cada uno de los tres archivos: se abren se limpian, corrigen y desanidan. Se guardan como csv. De aquí obtenemos:

* games.csv
* games_desanidado.csv
* 2reviews_desanidado.csv
* items_desanidado.csv

Luego de un EDA, estudiando las necesidades del negocio y la naturaleza de las consultas requeridas, hacemos uniones entres los archivos, groupby, recortes y eliminación de columnas innecesarias, guardando archivos csv mucho más compactos y sencillos, que nos utilizaremos dependiendo de la consulta:

* 1userdata.csv
* 2reviews_desanidado.csv
* 4userforgenre.csv
* 5developer.csv
* 6sentiment_analysis.csv
* 7recomendacion_juego.csv

Se cuenta con los archivos ipynb correspondientes para hacer un seguimiento del ETL y EDA, y tener disponible el proceso ante la eventual llegada de nuevos datos.
Los archivos son:

* ETL_Games.ipynb
* ETL_Items.ipynb
* ETL_Reviews.ipynb

* transformaciones.ipynb (aquí se hace una transformación distinta que obedece a las necesidades de cada consulta específica, relacionando los 3 csv anteriores)

* prueba_funciones.ipynb (notebook donde se encuentran importadas las librerías y desarrolladas las 7 funciones. Se utiliza como prueba antes del main.py)

## Resultados

En el archivo main.py tenemos:

* La creación de la API
* La importación de las librerías necesarias
* La importación de los distintos csv que utilizaremos
* Las 7 funciones disponibles para ser consultadas mediante la API

En el archivo requirements.txt tenemos la lista de las librerías a utilizar

Los resultados están disponibles en un sitio de Render de acceso público, desde donde se pueden realizar las consultas


## Detalles

Tenemos disponibles todos los archivos ipynb, txt, py, csv necesarios en el siguiente repositorio de GITHUB:

* https://github.com/Jeremias44/Proyecto_Individual_1.git

Tenemos disponible un sitio en Render para realizar las consultas mencionadas en la introducción:

* Sitio principal: https://consultas-steam-jeremias-pombo.onrender.com/

* Sitio de consultas: https://consultas-steam-jeremias-pombo.onrender.com/docs

Tenemos un video donde se muestra el funcionamiento de la API respondiendo a distintas consultas:

* Link de Youtube: https://www.youtube.com/watch?v=NIOKhnZ9J7E&ab_channel=JEREM%C3%8DASPOMBO

