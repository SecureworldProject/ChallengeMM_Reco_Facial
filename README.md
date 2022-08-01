# ChallengeMM_Reco_Facial
ChallengeMM recognized by a regular user

# DESCRIPCION y FIABILIDAD:
Reco_Facial es un challenge que comprueba si el usuario es un usuario habitual (empleado de la empresa), lo hace mediante
reconocimiento facial donde da como resultado 1 si es un usuario habitual, sino puede dar valores de 0 (si el challenge 
no se ejecuta por falta de cámara del pc o móvil vinculado mediante bluetooth, o si no detecta ningún rostro en la captura),
también puede dar valores de 2 a 12 si el rostro detectado es desconocido, alcanzando una cardinalidad igual a 13. Este challenge
tiene una fiabilidad baja porque el usuario malicioso puede tener un video o una imagen del rostro de un usuario habitual 
almacenado y engañar al challenge. 

# FUNCIONAMIENTO:
Este challenge requiere un proceso inicial de entrenamiento del modelo, esto se hace con el archivo crear_BD.py, donde se realiza
una captura de un video en streaming si el usuario cuenta con webcam en el pc o se captura un video almacenado en un repositorio
donde el movil guarda las capturas de video mediante bluetooth vinculado al pc. De cualquiera de las dos formas se capturan 300
fotos y se almacenan en una carpeta con el nombre del usurio para con estas entrenar el modelo de machine learning (LBPHFaceRecognizer) 
y almacenarlo. .

El challenge se encuentra en el fichero Reco_Facial.py donde se toma la captura y se pasa al modelo almacenado, devolviendo este
un parámetro de nivel de confianza que estará entre 0 y 70 si es un usuario conocido por el modelo. Por lo que se retorna 1 si
el valor de confianza está en ese rango. La clave resultante está desde 0 hasta 12, siendo 1 el valor correcto. 

#Modelos de IA de opencv para reconocimiento Facial:
https://docs.opencv.org/4.2.0/da/d60/tutorial_face_main.html#tutorial_face_eigenfaces

Modelo utilizado: LBPHFaceRecognizer
https://docs.opencv.org/3.4/df/d25/classcv_1_1face_1_1LBPHFaceRecognizer.html

# Requisitos:
Entrenar el modelo antes de usar el challenge, en el lugar de trabajo habitual y con la iluminación habitual. 

La variable de entorno SECUREMIRROR_CAPTURES debe existir y apuntar al path donde el server bluetooth deposita las capturas.

Librerías utilizadas:
Tkinter para las GUI 

Opencv para extraer información de videos tanto en streaming como almacenados y modelos de IA para reconocimiento facial.    
https://www.geeksforgeeks.org/opencv-python-tutorial

para instalar la libreria openCV simplemente:

pip3 install opencv-python

IMPORTANTE Si se muestra el  error: AttributeError: module 'cv2' has no attribute 'face' hacer lo siguiente:
pip install opencv-contrib-python

IMPORTANTE: tras instalar opencv, la dll python3.dll de instalacion de python cambia, debes darle acceso al programa que haga uso de este challenge ubicandola en un directorio al que pueda acceder

para aprender opencv https://www.geeksforgeeks.org/opencv-python-tutorial

para instalar el modulo tkinter simplemente:

pip3 install tkinter

para aprender tkinter: https://www.pythontutorial.net/tkinter/
