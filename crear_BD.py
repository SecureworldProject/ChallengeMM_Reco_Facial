
import cv2
import os
import imutils
import time
import tkinter as tk
from tkinter import messagebox
import numpy as np

#Se muestra una GUI para que el usuario entre su nombre y apellidos para identificalo
ventana= tk.Tk()
ventana.geometry('400x100')
tk.Label(ventana,text='Entre nombre y apellidos', font = "Calibri 20").pack()

nombre=tk.StringVar()
nomb=tk.Entry(ventana, textvariable=nombre, font = "Calibri 12", width = 40).pack()

#Se obtiene el nombre entrado por el usuario en personName
# para crear la carpeta de imagenes para entrenar el modelo
def obtTex():
    personName = str(nombre.get())
    print (personName)
    return (personName)

def cerrar():
    ventana.destroy()

#Botón para cerrar ventana una vez que el usuario introdujo su nombre y apellidos
button1 = tk.Button(ventana, text = "OK", command = cerrar).pack(side= tk.BOTTOM)
ventana.mainloop()

#Se crea una carpeta con el nombre del usuario a reconocer, 
#esta se creará dentro de la carpeta Data que ya se había creado previamente de forma manual. 
# Finalmente personPath será la ruta completa.

d_Path=os.environ['SECUREMIRROR_CAPTURES']
dataPath = d_Path + '/' + 'Data' #Cambia a la ruta donde hayas almacenado Data
personPath = dataPath + '/' + obtTex()

if not os.path.exists(personPath):
    print('Carpeta creada: ',personPath)
    os.makedirs(personPath)

ca=messagebox.askquestion(title= "Recon_Facial", message="Tines Pc con camara apta para tomar foto/video")
print (ca)
if (ca=="yes"):
    #En la siguiente línea se realiza un video en directo
    cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
else:
    ca1=messagebox.askquestion(title= "Recon_Facial", message="Tienes un movil con bluetooth activo y emparejado con tu PC con capacidad para tomar video")
    if (ca1=="yes"):
        #En la siguiente línea se lee  un video almacenado para hacer pruebas
        cap = cv2.VideoCapture(d_Path+ "/" + 'Video.mp4')
   
    
   
faceClassif = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
count = 0
while True:
    
    ret, frame = cap.read()
    if ret == False: break
    frame =  imutils.resize(frame, width=640)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    auxFrame = frame.copy()
    faces = faceClassif.detectMultiScale(gray,1.3,5)
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
        rostro = auxFrame[y:y+h,x:x+w]
        rostro = cv2.resize(rostro,(150,150),interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(personPath + '/rotro_{}.jpg'.format(count),rostro)
        count = count + 1
    cv2.imshow('frame',frame)
    k =  cv2.waitKey(1)
    if k == 27 or count >= 300:
        break
cap.release()
cv2.destroyAllWindows()

#******* FASE DE ENTRENAMIENTO**************************
peopleList = os.listdir(dataPath)
print('Lista de personas: ', peopleList)

labels = []
facesData = []
label = 0

for nameDir in peopleList:
    personPath = dataPath + '/' + nameDir
    print('Leyendo las imagenes')

    for fileName in os.listdir(personPath):
        #print('Rostros: ', nameDir + '/' + fileName)
        labels.append(label)
        facesData.append(cv2.imread(personPath+'/'+fileName,0))
        image = cv2.imread(personPath+'/'+fileName,0)
        #cv2.imshow('image',image)
        #cv2.waitKey(10)
    label = label + 1
#print('labels= ',labels)
#print('Numero de etiquetas 0: ',np.count_nonzero(np.array(labels)==0))
#print('Numero de etiquetas 1: ',np.count_nonzero(np.array(labels)==1))
#print('Numero de etiquetas 2: ',np.count_nonzero(np.array(labels)==2))

#Entrenando el modelo
face_recognizer = cv2.face.LBPHFaceRecognizer_create()
# Entrenando el reconocedor de rostros
print("Entrenando...")
face_recognizer.train(facesData, np.array(labels))

face_recognizer.write(d_Path + "/" + 'modeloLBPHFace.xml')
print("Modelo almacenado...")