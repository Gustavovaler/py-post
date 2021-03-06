import os
import json
import datetime
from tkinter import Tk, Button, Label, StringVar, IntVar, Entry, Text, Frame
from tkinter import messagebox
from tkinter import simpledialog as simpledialog
from tkinter import filedialog
import tkinter.font as fnt
from tkinter.ttk import LabelFrame
from utilities import parse_log, SendRequest, save_reg_url


class UserInterface:       

    def __init__(self):
        #colours**********
        self.FG_COLOR = "#ccedd2"
        self.BACK_COLOR = "#655c56"
        self.BG_COLOR = '#deebde'
        self.ORANGE = '#FFCC66'

        # *** sizing *****

        self.width = 1050
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
        self.version_label = Label(self.nav_bar, text= "v - 1.1 ", bg=self.BACK_COLOR, fg=self.FG_COLOR)
        self.version_label.place(x=930, y=5)
        

        #---- special vars----------------------
        self.despy = 35
        self.c_t = StringVar()
        self.url_var = StringVar()
        self.status = StringVar()
        self.length = StringVar()       
       


        #--- set headers area -----------------

        self.frame2 = Frame(self.ventana, width = 700, height=220)
        self.frame2.place(relx = 0.05, y = 140+self.despy)

        self.frame3 = Frame(self.frame2, width =684 , height = 34, bg= self.BACK_COLOR)
        self.frame3.place(relx = 0.01 , y = 181)        

    #-- memory panel--------------------

        self.frame_memory = LabelFrame(self.ventana, width = 250 , height = 220, text = "Recent requests" , labelanchor = 'nw', relief = 'ridge')
        self.frame_memory.place(x=780, y = 130+self.despy)





        self.memory_frame()
        self.memory_panel()
        self.create_widgets()
        self.ventana.mainloop()



    # -------  errors methods -----------


    @staticmethod
    def error_dialog(msg):
        messagebox.showerror("Error", msg)


    #--- widget  methods -----------------------------
    def memory_frame(self):
        self.frame_memory = LabelFrame(self.ventana, width = 250 , height = 220, text = "Recent requests" , labelanchor = 'n', relief = 'ridge')
        self.frame_memory.place(x=780, y = 130+self.despy)

    def memory_panel(self): 

        self.memory_frame()
        self.objects = parse_log()        
        for obj in self.objects:
            b_g = None
            if self.objects.index(obj) > 7:
                break
            if obj['method'] == 'GET':
                b_g = "#B2E6C7"
            elif obj['method'] == 'POST':
                b_g = "#EAE658"
            elif obj['method'] == 'UPDATE':
                b_g = "#F5A66F"
            elif obj['method'] == 'DELETE':
                b_g = "#F53333"

            self.recent_button = Button(self.frame_memory,width=35, text = "{} - {}".format(obj['method'][:3], obj['url'][:35]), bg=b_g,
                command = lambda obj=obj: self.set_var_url(obj['url']))       
            self.recent_button.pack()

    def save_reg_to_file(self,dat):
        self.objects.append(dat)
        


    def create_widgets(self):

        self.label_url = Label(self.ventana, text="Url:",bg=self.BG_COLOR, font=self.font_h6  )
        self.label_url.place(relx = 0.05, y = 50)

        self.url_bar = Text(self.ventana, width = '70', height = 1.2)
        self.url_bar.place(relx = 0.05, y = 40+self.despy)
        self.url_bar.config(font=self.font_entry)
        
        self.get_button = Button(self.ventana, text =" GET ", command = lambda : self.send_request("GET"))
        self.get_button.place(relx = 0.05, y = 75+self.despy)
        self.get_button.config(fg=self.ORANGE, bg= self.BACK_COLOR)
        
        self.post_button = Button(self.ventana, text ="POST", command = lambda : self.send_request("POST"))
        self.post_button.place(relx = 0.10, y = 75+self.despy)
        self.post_button.config(fg=self.ORANGE, bg= self.BACK_COLOR)
        
        self.update_button = Button(self.ventana, text = " UPDATE ", command = lambda : self.send_request("UPDATE"))
        self.update_button.place(relx = 0.15, y = 75+self.despy)
        self.update_button.config(fg=self.ORANGE, bg= self.BACK_COLOR)
        
        self.delete_button = Button(self.ventana, text =" DELETE ",  command = lambda : self.send_request("DELETE"))
        self.delete_button.place(relx = 0.22, y = 75+self.despy)
        self.delete_button.config(fg=self.ORANGE, bg= self.BACK_COLOR)

        self.status_widgets()
        self.content_type_widgets()

        #---- RESPONSE AREA WIDGETS-------------

        self.response_area = Text(self.frame2, width = '85', height = 10, font = self.font_h6, bd=2)
        self.response_area.place(relx = 0.01, y = 4)

        self.save_button = Button(self.ventana, text = "EXPORT TO FILE", bg = self.BACK_COLOR, fg= self.ORANGE, command = self.save_to_file)
        self.save_button.place(relx = 0.63, y = 365+self.despy)

        self.clear_button = Button(self.ventana, text = " CLEAR ", bg =self.BACK_COLOR, fg = self.ORANGE, command = self.clear)
        self.clear_button.place(relx = 0.56 , y = 365+self.despy)

        

  
    def set_var_url(self,url):
        self.url_bar.delete("1.0","end")
        self.url_bar.insert("1.0", url)

    def clear(self):
        self.response_area.delete("1.0", "end")
        self.status.set('')
        self.c_t.set('')
        self.length.set('')

        
    def status_widgets(self):
        self.status_label = Label(self.ventana, text= "Status : ")
        self.status_label.place(relx=0.07, y = 110+self.despy)
        self.status_label.config(bg=self.BG_COLOR, font=self.font_h6)

        self.status_entry = Entry(self.ventana,textvariable = self.status,width = 5, font=self.font_h6)
        self.status_entry.place(relx = 0.13, y = 110+self.despy)

        self.length_label = Label(self.ventana, text = "Content Length:",bg=self.BG_COLOR, font=self.font_h6 )
        self.length_label.place(relx = 0.55 , y= 110+self.despy)

        self.length_entry = Entry(self.ventana,textvariable = self.length,width = 5, font=self.font_h6)
        self.length_entry.place(relx = 0.67, y = 110+self.despy)

    def content_type_widgets(self):
        self.content_label = Label(self.ventana, text='Content-Type:')
        self.content_label.place(relx=0.20, y = 110+self.despy)
        self.content_label.config(bg=self.BG_COLOR, font=self.font_h6)

        self.content_entry = Entry(self.ventana,textvariable = self.c_t ,width = 28, font=self.font_h6)
        self.content_entry.place(relx = 0.30, y = 110+self.despy)


    #----------------methods -------------------
    def send_request(self, method):
        
        self.url = self.url_bar.get("1.0",'end-1c')

        if method == 'GET':
            self.response = SendRequest.get(self.url)

        elif method == 'POST':            
            data = {'method':'POST','body':{'title': 'foo','body': 'bar','userId': 1},'headers': {"Content-type": "application/json; charset=UTF-8"}}      
            jsondata = json.dumps(data)
            self.response = SendRequest.post(self.url,jsondata)

        elif method == 'UPDATE':
            data = self.response_area.get("1.0", 'end-1c')
            jsondata = json.dumps(data)
            self.response = SendRequest.update(self.url, jsondata)

        elif method == 'DELETE':
            self.response = SendRequest.delete(self.url)

        if self.response:
            self.new_reg_memory = {"method":method, "url":self.url, "time":str(datetime.datetime.now())}
            save_reg_url(self.new_reg_memory)           

            if self.response == "err1":
                self.error_dialog("Debe ingresar una url.")
            else:
                self.deploy_data(self.response)
        else:
            self.response_area.insert("1.0", "No se pudo establecer conexión con el servidor")

        self.frame_memory.destroy()
        self.memory_panel()


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


    def save_to_file(self):

        if self.response_area.get("1.0", 'end-1c') == '':
            self.error_dialog("No hay contenido para guradar.")
            return

        my_filetypes = [('all files', '.*'), ('text files', '.txt'), ('web','.html'),('directories', '/*/')]

        answer = filedialog.asksaveasfilename(parent=self.ventana,
                                            initialdir = os.getcwd(),
                                            title = "Seleccione el nombre de archivo y su ubicación: ",
                                            filetype = my_filetypes)
        if answer:
            f = open(answer, "w")
            f.write(self.response_area.get("1.0", 'end-1c'))
            f.close()  




if __name__ == '__main__':

    cdir = os.getcwd()
    if not os.path.isfile(cdir+"/log.json"):
        f=open("log.json", "w")
        f.write('{"urls":[{"method": "", "url": "", "time": "2020-06-21 22:59:47.832558"}]}')
        f.close()   

    app = UserInterface()





