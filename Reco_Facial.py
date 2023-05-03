from asyncio.windows_events import NULL
import cv2
import numpy as np
import os
import tkinter as tk
from tkinter import messagebox
from pathlib import Path
import lock

# Para instalar el módulo tkinter usar uno de los siguiente comandos:
#   pip3 install tkinter
#   py -m pip install tkinter



# Variables globales
# ------------------
props_dict = {}

def init(props):
    global props_dict
    print("CHALLENGE_RECO_FACIAL --> Enter in init")

    # Props es un diccionario
    props_dict = props
    resultado = ('1', 1) #executeChallenge()
    if (resultado[1]>0):
        return 0
    else:
        return -1



def executeChallenge():
    print("CHALLENGE_RECO_FACIAL --> Starting execute")
    #for key in os.environ: print(key, ':', os.environ[key])
    dataPath = os.environ['SECUREMIRROR_CAPTURES']

    print("CHALLENGE_RECO_FACIAL --> Storage folder is:", dataPath)

    # Mecanismo de lock BEGIN
    # -----------------------
    lock.lockIN("Reco_Facial")


    #dataPath = 'B:/Doctorado/Challenges/Data' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath + "/" + "Data")
    print("CHALLENGE_RECO_FACIAL --> imagePaths=", imagePaths)

    face_recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Leyendo el modelo
    face_recognizer.read(dataPath + "/" + 'modeloLBPHFace.xml')

    # Popup pidiendo interacción
    # Pregunta si el usuario tiene móvil con capacidad foto
    ca = messagebox.askquestion(title="Recon_Facial", message="Tines Pc con cámara apta para tomar foto/video")
    print("CHALLENGE_RECO_FACIAL --> Camera: ", ca)

    if (ca=="yes"):
        # En la siguiente línea se realiza un video en directo
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    else:
        ca1 = messagebox.askquestion(title="Recon_Facial", message="Tienes un móvil con bluetooth activo y emparejado con tu PC con capacidad para tomar un video")
        if (ca1=="yes"):
            # En la siguiente línea se lee un video almacenado para hacer pruebas
            cap = cv2.VideoCapture(dataPath + "/" + '1.jpeg')
        else:
            # Mecanismo de lock END
            #----------------------
            lock.lockOUT("Reco_Facial")
            key_size = 0
            result = (NULL, key_size)
            print("CHALLENGE_RECO_FACIAL --> result:", result)
            return result


    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    print("CHALLENGE_RECO_FACIAL --> Model has been read")

    res = 0

    try:
        ret,frame = cap.read()
    except:
        print("CHALLENGE_RECO_FACIAL --> Error: cannot get frame from camera")
        result = (NULL, key_size)
        print("CHALLENGE_RECO_FACIAL --> result:", result)
        return result

    if ret == False:
        cap.release()
        cv2.destroyAllWindows()
        lock.lockOUT("Reco_Facial")
        key_size = 0
        result = (NULL, key_size)
        print("CHALLENGE_RECO_FACIAL --> result:", result)
        return result

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('gray', gray)
    #cv2.waitKey(0)
    auxFrame = gray.copy()
    faces = faceClassif.detectMultiScale(gray, 1.3, 5)
    for (x,y,w,h) in faces:
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro, (150,150), interpolation=cv2.INTER_CUBIC)
        result = face_recognizer.predict(rostro)
        cv2.putText(frame, '{}'.format(result), (x,y-5), 1, 1.3, (255,255,0), 1, cv2.LINE_AA)
        print("CHALLENGE_RECO_FACIAL --> result:", result)

        # LBPHFace
        if result[1] > 0 and result[1] <= 70:
            cv2.putText(frame, '{}'.format(imagePaths[result[0]]), (x,y-25), 2, 1.1, (0,255,0), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(0)
            res = result[1]
        elif result[1] <= 0 or result[1] > 70:
            cv2.putText(frame, 'Desconocido', (x,y-20), 2, 0.8, (0,0,255), 1, cv2.LINE_AA)
            cv2.rectangle(frame, (x,y), (x+w,y+h), (0,0,255), 2)
            cv2.imshow('frame', frame)
            cv2.waitKey(0)
            res = result[1]

    cap.release()
    cv2.destroyAllWindows()


    # Mecanismo de lock END
    #----------------------
    lock.lockOUT("Reco_Facial")

    # Get the mode from the properties dictionary (global variable)
    mode = props_dict["mode"]

    # Construcción de la respuesta
    if mode == "parental":
        if res > 0 and res <= 70:   resp = 1
        else:                       resp = 0

    else:   # Modo no parental
        if res<=0:                  resp = 0
        elif res>0 and res<=70:     resp = 1
        elif res>70 and res<=75:    resp = 2
        elif res>75 and res<=80:    resp = 3
        elif res>80 and res<=85:    resp = 4
        elif res>85 and res<=90:    resp = 5
        elif res>90 and res<=95:    resp = 6
        elif res>95 and res<=100:   resp = 7
        elif res>100 and res<=105:  resp = 8
        elif res>105 and res<=110:  resp = 9
        elif res>110 and res<=115:  resp = 10
        elif res>115 and res<=120:  resp = 11
        elif res>120:               resp = 12


    cad = "%d"%(resp)
    key = bytes(cad, 'utf-8')
    key_size = len(key)
    result = (key, key_size)
    print("CHALLENGE_RECO_FACIAL --> result:", result)
    return result


if __name__ == "__main__":
    midict = {"mode": "parental"}
    print(init(midict))
    print(executeChallenge())
