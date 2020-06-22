import json
import requests as r
from tkinter import messagebox

def parse_log():
    f = open("log.json", "rb+")
    log = json.loads(f.read())
    registros =[]
    for reg in log['urls']:
        registros.append(reg)
    f.close()
    registros.reverse()
    return registros


def save_reg_url(registro):
    
    regjson = json.dumps(registro)
    f = open("log.json", "rb+")
    f.seek(-2,2)
    f.write(bytes(","+regjson+"]}", 'utf-8'))
    f.close()

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
            return "err1"
        try:
            response = r.post(url, data)
            return response
        except:
            return None
        

    @staticmethod
    def update(url,data):
        if url == '':
            return "err1"
        else:
            try:
                response = r.put(url, data)
                return response
            except:
                return None


    @staticmethod
    def delete(url):
        if url == '':
            return "err1"
            return response
        else:
            try:
                response = r.delete(url)
                return response
            except:
                return None

