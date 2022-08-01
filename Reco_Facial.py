
from asyncio.windows_events import NULL
from winreg import CloseKey
import cv2
import os
import imutils
import time
import tkinter as tk
from tkinter import messagebox
import numpy as np
from pathlib import Path
import time
#para instalar el modulo tkinter simplemente:
#pip3 install tkinter
# o bien py -m pip install tkinter

# variables globales
# ------------------
props_dict={}

def init(props):
    global props_dict
    print("Python: Enter in init")
    res=executeChallenge()
    print(res)
    #props es un diccionario
    props_dict= props
    if res <= 0:
        return 0
    elif res > 0 and res <= 70:
        return 1
    elif res> 70 and res<= 75:
        return 2
    elif res> 75 and res<= 80:
        return 3
    elif res> 80 and res<= 85:
        return 4
    elif res> 85 and res<= 90:
        return 5
    elif res> 90 and res<= 95:
        return 6
    elif res> 95 and res<= 100:
        return 7
    elif res> 100 and res<= 105:
        return 8
    elif res> 105 and res<= 110:
        return 9
    elif res> 110 and res<= 115:
        return 10
    elif res> 115 and res<= 120:
        return 11
    elif res> 120:
        return 12

           
def executeChallenge():
    print("Starting execute")
    #for key in os.environ: print(key,':',os.environ[key])
    dataPath=os.environ['SECUREMIRROR_CAPTURES']

    print ("storage folder is :",dataPath)
    
    
    # mecanismo de lock BEGIN
    # -----------------------
    while os.path.exists(dataPath+"/"+"lock"):
        time.sleep(1)
    Path(dataPath+"/"+"lock").touch()

    #dataPath = 'B:/Doctorado/Challenges/Data' #Cambia a la ruta donde hayas almacenado Data
    imagePaths = os.listdir(dataPath+ "/" + "Data")
    print('imagePaths=',imagePaths)
    
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Leyendo el modelo
    face_recognizer.read(dataPath+ "/" + 'modeloLBPHFace.xml')
    
    #popup pidiendo interaccion
    # pregunta si el usuario tiene movil con capacidad foto
    ca=messagebox.askquestion(title= "Recon_Facial", message="Tines Pc con camara apta para tomar foto")
    print (ca)
    
    if (ca=="yes"):
       #En la siguiente línea se realiza un video en directo
       cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
    else:
      ca1=messagebox.askquestion(title= "Recon_Facial", message="Tienes un movil con bluetooth activo y emparejado con tu PC con capacidad para tomar un video")
      if (ca1=="yes"):
          #En la siguiente línea se lee  un video almacenado para hacer pruebas
          cap = cv2.VideoCapture(dataPath+ "/" + 'Video.mp4')
        
      else:
         os.remove(dataPath+"/"+"lock")
         return 0 # clave cero, longitud cero

    faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
    print("MODELO LEIDO")
    
    if True:
        res=0
        ret,frame = cap.read()
        if ret == False: return 0 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #cv2.imshow('gray',gray)
        auxFrame = gray.copy()
        faces = faceClassif.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            rostro = auxFrame[y:y+h,x:x+w]
            rostro = cv2.resize(rostro,(150,150),interpolation= cv2.INTER_CUBIC)
            result = face_recognizer.predict(rostro)
            cv2.putText(frame,'{}'.format(result),(x,y-5),1,1.3,(255,255,0),1,cv2.LINE_AA)
            print(result)
        
            # LBPHFace
            if result[1] > 0 and result[1] <= 70:
               cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
               cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
               cv2.imshow('frame',frame)
               cv2.waitKey(0)
               res= result[1]
               #print (resultado)
            elif result[1] <= 0 or result[1] > 70:
                cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                cv2.imshow('frame',frame)
                cv2.waitKey(0)              
                res= result[1]
             
    cv2.destroyAllWindows()
    cap.release()


    #mecanismo de lock END
    #-----------------------
    os.remove(dataPath+"/"+"lock") 

    #construccion de la respuesta
    #cad="%d"%(resultado)
    #key = bytes(cad,'utf-8')
    #print (key)
    #key_size = len(key)
    #res =(key, key_size)
    #print ("result:",res)
    return res

if __name__ == "__main__":
    midict={}
    print(init(midict))
    #executeChallenge()