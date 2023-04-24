from deepface import DeepFace
import pandas as pd
import cv2
import random
import time
import os

path = "./member_image/"

def register(name_input, ID):
    # cap = cv2.VideoCapture(0)
    # if not cap.isOpened():
    #     print("Unable to connect to camera")
    # else:
    #     for i in range (0,9):
    #         ret, frame = cap.read()
    #         id = random.randint(0,999999)
    #         name = path + str(name_input) +"_"+ str(ID) + "_" + str(id) + ".jpg"
    #         cv2.imwrite(name, frame)
    #         time.sleep(1)
    # cap.release()
    try:
        os.remove("./member_image/representations_facenet512.pkl")
    except:
        pass
    print("Register successfully from AI !!!!")

             
def Verification(path):
    try: 
        dfs = DeepFace.find(img_path = path, db_path = "./member_image", distance_metric="euclidean_l2",model_name="Facenet512")
    except:
        print("Unknown detected !!!")
        return "Error"

    try:
        namedected = dfs[0].iloc[0]["identity"]
    except:
        print("Unknown detected !!!")
        return "None"
    else:
        print("Verify from AI !!!! ")
        return dfs[0].iloc[0]["identity"]

#register("NguyenTrongTin","16122002")

#print(Verification("JeffBezos_1.jpg"))


