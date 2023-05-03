# module lock

import os
from pathlib import Path
import time
import fnmatch

def searchLock(challenge_name):
    folder = os.environ['SECUREMIRROR_CAPTURES']
    while os.path.isdir(folder)==False:
        print(" challenge : SECUREMIRROR_CAPTURES environment variable not valid")
        return False
        time.sleep(60) # check and sleep forever
        
    # Si llegamos aqui, el directorio existe
        
    for file in os.listdir(folder):
        if fnmatch.fnmatch(file,'lock_*'):
            print("file found:", file)
            # Hemos encontrado un fichero que cumple
            # Si es nuestro challenge, ignoramos
            # if file=="lock_" + challenge_name:
            #     print("El lock es de este mismo challenge: lo ignoramos")
            #     continue
            creation_date = os.path.getctime(folder + "/" + file)
            now = time.time()
            if (now > creation_date+300): # 5 minutos es viejo
                # Es viejo
                print(file, "is old")
                continue
            else:
                return False
    return True
    
def lockIN(challenge_name):
    
    # Mientras exista un fichero lock* se queda en bucle
    while True:
        search = searchLock(challenge_name)
        if (search==True):
            break
        else:
            time.sleep(5)
            
    # Si llegamos aquies que no hay lock o lo que hay es viejo
    # Tambien tenemos garantizado si llegamos aqui que folder existe
    
    folder = os.environ['SECUREMIRROR_CAPTURES']
    # Borramos un posible fichero viejo nuestro
    if os.path.exists(folder + "/" + "lock_" + challenge_name):
        os.remove(folder + "/" + "lock_" + challenge_name)
    # Creamos el nuevo
    Path(folder + "/" + "lock_" + challenge_name).touch()
    

def lockOUT(challenge_name):
    folder = os.environ['SECUREMIRROR_CAPTURES']
    if os.path.exists(folder + "/" + "lock_" + challenge_name):
        os.remove(folder + "/" + "lock_" + challenge_name)
    
