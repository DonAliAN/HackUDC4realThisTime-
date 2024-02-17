# HackUDC4realThisTime 
 Always learning, always growing. 


16-02-24 --------

Buenas, somos estudiantes de primero de ingeniería informática en la UDC, y este es nuestro primer hackathon. 

En este proyecto buscamos ante todo aprender y ganar experiencia con un ambiente de desarrollo real. 
Hemos escogido hacer una web ya que tenemos conocimientos básicos, y es una buena manera de participar en el reto de gradiant de forma sencilla. 

El primer problema que afrontamos fue encontrar una idea en la que trabajar que se adecúe a nuestro nivel de experiencia y en el que podamos colaborar en grupo. Tras debatir las distintas posibilidades, encontramos que hacer una web sencilla y utilizando python en la lógica es la forma más simple de poder participar en un reto. A pesar de haber terminado un modelo básico sobre el que podemos construir, el debate sobre si alguna otra opción siguió surgiendo durante el desarrollo. 

Tras trabajo y aprendizaje de nuevas herramientas como el uso de Git y GitHub, nuevas funcionalidades de IDEs como VS Code y Jet Brains, así como escribir documentación, nuevos conocimientos en Python, sobretodo en la librería de Streamlit y matplot para graficar los datos, que nos permite tener una interfaz básica para la web sin malgastar demasiado tiempo jugando con el frontend. Al final del día logramos alcanzar un modelo funcional que servirá como base para implementar las funcionalidades que demanda el reto para que sea al menos presentable. 

17-02-24 ---------

El debate sobre el proyecto se vió conluído, debido al avance positivo del reto de Gradiant y la web en desarrollo. Nos dedicamos a profundizar en la funcionalidad de la web, de modo que añadimos por encima de las gráficas de consumo básicas, un pequeño algoritmo que aconseja ciertas prácticas al usuario sobre cómo ahorrar en su consumo. Este y otros detalles estéticos hicieron que nos pongamos a trabajar al 100% en esta idea. 

Tras trabajar en nuevas funciones nos encontramos con numerosos errores, ya sea dentro del git, el repositorio, los propios editores de texto, problemas con la descarga de python y las librerías. Pasamos mucho tiempo arreglando los errores que nos llevaba avanzar, por lo que descartamos varias funcionalidades que pensábamos implementar como la API pública de la luz española.


La aplicación opera analizando el archivo CSV que el usuario selecciona. Para este análisis, empleamos los algoritmos proporcionados por la empresa Gradiant en su archivo Jupyter Notebook. A través de los datos recopilados, se generan dos gráficas que representan la información contenida en el archivo CSV de una forma visual para que se pueda facilmente. Luego, se incorpora la funcionalidad de un chatbot que, si bien no utiliza directamente inteligencia artificial, la aplica de manera indirecta para clasificar las intenciones del usuario mediante etiquetas y asi obtener una respuesta mas precisa. A partir de la etiqueta predicha por el modelo preentrenado, se ejecuta una función asociada que devuelve e imprime información acerca de lo que el usuario solicitó.