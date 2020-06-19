import requests as r
from tkinter import Tk, Button, Label, StringVar, IntVar, Entry, Text, Frame
from tkinter import messagebox
from tkinter import simpledialog as simpledialog
import tkinter.font as fnt
import json

class SendRequest:
    def __init__(self):
        pass

    @staticmethod
    def get(url, pretty = None):

        if url == '':
            UserInterface.error_dialog("Debe ingresar una url.")
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


class UserInterface:       

    def __init__(self):
        #colours**********
        self.FG_COLOR = "#ccedd2"
        self.BACK_COLOR = "#655c56"
        self.BG_COLOR = '#effcef'

        # *** sizing *****

        self.width = 1000
        self.height = 600

        # main window

        self.ventana = Tk()
        self.ventana.geometry(str(self.width)+"x"+str(self.height)+"+200+100")        
        self.ventana.config(bg=self.BG_COLOR)
        self.ventana.resizable(width = False, height = False)        
        self.ventana.title("PY-POST")

        # fonts ******

        self.font_entry = fnt.Font(family="Monospace", size=16)
        self.font_h6 = fnt.Font(family="San Serif", size=11)


        # navigator and menu ----------

        self.nav_bar = Frame(self.ventana, width = self.width, height=35,bg=self.BACK_COLOR)
        self.nav_bar.place(x=0, y=0)
        self.title = Label(self.nav_bar, text="PY-POST", bg=self.BACK_COLOR, fg=self.FG_COLOR)
        self.title.place(x=50, y =5)
        self.version_label = Label(self.nav_bar, text= "v - 1.0 ", bg=self.BACK_COLOR, fg=self.FG_COLOR)
        self.version_label.place(x=930, y=5)
        

        self.despy = 25

        self.c_t = StringVar()
        self.url_var = StringVar()
        self.status = StringVar()
        self.length = StringVar()
        
        
        self.create_widgets()
        self.ventana.mainloop()

    @staticmethod
    def error_dialog(msg):
        messagebox.showerror("Error", msg)

    def create_widgets(self):
        self.url_bar = Text(self.ventana, width = '70', height = 1.2)
        self.url_bar.place(relx = 0.1, y = 40+self.despy)
        self.url_bar.config(font=self.font_entry)
        
        self.get_button = Button(self.ventana, text =" GET ", command = self.send_request_get)
        self.get_button.place(relx = 0.1, y = 75+self.despy)
        self.get_button.config(fg=self.FG_COLOR, bg= self.BACK_COLOR)
        
        self.post_button = Button(self.ventana, text ="POST", command = self.send_request_post)
        self.post_button.place(relx = 0.15, y = 75+self.despy)
        self.post_button.config(fg=self.FG_COLOR, bg= self.BACK_COLOR)
        
        self.update_button = Button(self.ventana, text = " UPDATE ", command = self.send_request_update)
        self.update_button.place(relx = 0.2, y = 75+self.despy)
        self.update_button.config(fg=self.FG_COLOR, bg= self.BACK_COLOR)
        
        self.delete_button = Button(self.ventana, text =" DELETE ",  command = self.send_request_delete)
        self.delete_button.place(relx = 0.27, y = 75+self.despy)
        self.delete_button.config(fg=self.FG_COLOR, bg= self.BACK_COLOR)

        self.status_widgets()
        self.content_type_widgets()

        #---- RESPONSE AREA WIDGETS-------------

        self.response_area = Text(self.ventana, width= '85', height = 10, font=self.font_h6, bd=2)
        self.response_area.place(relx = 0.1, y = 145+self.despy)

        self.save_button = Button(self.ventana, text= "EXPORT TO FILE", bg=self.BACK_COLOR, fg= self.FG_COLOR)
        self.save_button.place(relx = 0.68, y= 335+self.despy)

        self.clear_button = Button(self.ventana, text= " CLEAR ", bg=self.BACK_COLOR, fg= self.FG_COLOR, command = self.clear)
        self.clear_button.place(relx = 0.61 , y= 335+self.despy)

        self.length_label = Label(self.ventana, text = "Content Length:",bg=self.BG_COLOR, font=self.font_h6 )
        self.length_label.place(relx = 0.12 , y= 335+self.despy)

        self.length_entry = Entry(self.ventana,textvariable = self.length,width = 5, font=self.font_h6)
        self.length_entry.place(relx = 0.24, y = 335+self.despy)


    def clear(self):
        self.response_area.delete("1.0", "end")
        self.status.set('')
        self.c_t.set('')
        self.length.set('')
        
    def status_widgets(self):
        self.status_label = Label(self.ventana, text= "Status : ")
        self.status_label.place(relx=0.12, y = 110+self.despy)
        self.status_label.config(bg=self.BG_COLOR, font=self.font_h6)

        self.status_entry = Entry(self.ventana,textvariable = self.status,width = 5, font=self.font_h6)
        self.status_entry.place(relx = 0.18, y = 110+self.despy)

    def content_type_widgets(self):
        self.content_label = Label(self.ventana, text='Content-Type:')
        self.content_label.place(relx=0.25, y = 110+self.despy)
        self.content_label.config(bg=self.BG_COLOR, font=self.font_h6)

        self.content_entry = Entry(self.ventana,textvariable = self.c_t ,width = 28, font=self.font_h6)
        self.content_entry.place(relx = 0.35, y = 110+self.despy)

#----------------FUNCTIONS -------------------
    def send_request_get(self):

        self.url = self.url_bar.get("1.0",'end-1c')

        self.response = SendRequest.get(self.url)

        if self.response:
            self.deploy_data(self.response)
        else:
            self.response_area.insert("1.0", "No se pudo establecer conexión con el servidor")    


    def send_request_post(self):

        data = {'method':'POST','body':{'title': 'foo','body': 'bar','userId': 1},'headers': {"Content-type": "application/json; charset=UTF-8"}}
      
        jsondata = json.dumps(data)

        self.url = self.url_bar.get("1.0", 'end-1c')

        self.response = SendRequest.post(self.url,jsondata)
        if self.response:
            self.deploy_data(self.response)
        else:
            self.clear()
            self.response_area.insert("1.0", "No se pudo establecer conexión con el servidor")


    def send_request_delete(self):

        self.url = self.url_bar.get("1.0", 'end-1c')

        self.response = SendRequest.delete(self.url)

        if self.response:
            self.deploy_data(self.response)
        else:
            self.response_area.insert("1.0", "No se pudo establecer conexión con el servidor")


    def send_request_update(self):

        self.url = self.url_bar.get("1.0", 'end-1c')
        data = self.response_area.get("1.0", 'end-1c')
        jsondata = json.dumps(data)
        self.response = SendRequest.update(self.url, jsondata)
        if self.response:
             self.deploy_data(self.response)
        else:
            self.response_area.insert("1.0", "No se pudo establecer conexión con el servidor")

        

    def deploy_data(self, response):

        self.clear()
        self.headers = self.response.headers
        self.content_type = self.headers['Content-Type']
        self.c_t.set(self.content_type)
        self.status.set(self.response.status_code)
        text = self.response.content
        self.response_area.insert("1.0", text.strip())
        try:
            self.length.set(self.response.headers['content-length'])
        except:
            self.length.set('N/A')       


if __name__ == '__main__':
    app = UserInterface()




