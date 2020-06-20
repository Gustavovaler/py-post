import json
import requests as r
from tkinter import messagebox

def parse_log():
    f = open("log.json", "r")
    log = json.loads(f.read())
    registros =[]
    for reg in log['urls']:
        registros.append(reg)
    f.close()
    return registros



class SendRequest:
    def __init__(self):
        pass

    @staticmethod
    def get(url, pretty = None):

        if url == '':
            return "err1"            
        try:
            response = r.get(url)
            return response
        except:            
            print("error de conexion")
            return None
                   

    @staticmethod
    def post(url,data=None):
        if url == '':
            UserInterface.error_dialog("Debe ingresar una url.")
        try:
            response = r.post(url, data)
            return response
        except:
            return None
        

    @staticmethod
    def update(url,data):
        if url == '':
            UserInterface.error_dialog("Debe ingresar una url.")
        else:
            try:
                response = r.put(url, data)
                return response
            except:
                return None


    @staticmethod
    def delete(url):
        if url != '':
            response = r.delete(url)
            return response
        else:
            UserInterface.error_dialog("Debe ingresar una url.")
            return None
