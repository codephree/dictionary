import tkinter 
from PIL import ImageTk, Image
import requests
import os
import customtkinter
# import _env

class App(customtkinter.CTk):
    #======================= Function to check internet connection ==========================#
    def check_internet(self):
        url = 'http://www.google.com/'
        timeout = 5
        try:
            _ = requests.get(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            return False

    #======================= Function to search for words in Dictionary ==========================#
    def queryApi(self, words):
            url = "https://wordsapiv1.p.rapidapi.com/words/"+words
            headers = {
                'x-rapidapi-host': 'wordsapiv1.p.rapidapi.com',   #os.environ.get("host"),
                'x-rapidapi-key': 'EvnlrUuK15mshjOAnvPOUgUFyldkp1egDpgjsnfiCBoEoc2I93'  #os.environ.get("api-key")
            }

            response = requests.request("GET", url, headers=headers)
            jsonresponse = response.json()
            display = ''
            # print(jsonresponse)
            if response.status_code == 200:
                 final = jsonresponse['results']
                #  print(final)
                 return True, final
            elif response.status_code == 404:
                 return False,  jsonresponse['message'] 
            else:
                 return False , "Error from the API.."
               

            return display
    
    #======================= Function to Put definition into Label ==========================#

    def seerchDico(self):
        serachWords = self.search.get()
        scorrableTitle ="Result words for " + serachWords.capitalize()
        response = self.queryApi(serachWords)
        defini = ''
        
        if len(self.result.get('1.0',tkinter.END)[:-1]):
            self.result.configure(state='normal')
            self.result.delete(1.0, tkinter.END)
            self.result.configure(state='disabled')
        
        if(response[0]):
             for idx, value in enumerate(iterable=response[1]):
                 defini += str(idx + 1) + ' - { '+ value['partOfSpeech'] + ' } ' + value['definition'] + '\n \n'
        else:
            defini = response[1]
         
        self.title.configure(text=scorrableTitle)
        
        # pack_configure(text=scorrableTitle)

        self.result.configure(state='normal')
        self.result.insert('end', text=defini)
        self.result.configure(state='disabled')
        
    #======================= Function to hide scrollable frame ==========================#
    def hide_scrollable(self):
             self.scrollable.pack_forget()   

    #======================= Function to define top menu ==========================#
    def define_app_menu(self, menu):
        self.file_menu = tkinter.Menu(menu, bd=0)
        menu.add_cascade(label='File', menu=self.file_menu)
        self.file_menu.add_command(label='Exit', command=self.quit)

        self.options_menu = tkinter.Menu(menu)
        menu.add_cascade(label='Options', menu=self.options_menu)
        self.options_menu.add_command(label='Refresh app', command=self.quit)
        self.options_menu.add_separator()
        self.options_menu.add_command(label='Internet Option', command=self.quit)
        
        self.exit_menu = tkinter.Menu(menu)
        menu.add_cascade(label='Exit', menu=self.exit_menu)
   
    #======================= Function to Initiate the app ==========================#
    def __init__(self):
        super().__init__()

        self.title("Dictionary")
        self.geometry("400x500")
        self._set_appearance_mode('system')
        self.wm_iconbitmap('dico.ico')
        self.menu = tkinter.Menu(self)
        self.config(menu=self.menu)
        
        
        #======================= Logic to check if the internt is available ==========================#
        if self.check_internet():
            
            self.title = customtkinter.CTkLabel(self,text='Enter your search word below:',
                                                    fg_color='transparent')
            self.title.pack(padx=10, pady=10)

            searchWords = tkinter.StringVar()
            self.search =  customtkinter.CTkEntry(self,width=350, 
                                                height=40, 
                                                corner_radius=10,
                                                textvariable=searchWords,
                                                placeholder_text='Enter your words')
            self.search.pack(padx=10,pady=10)
            
            self.button = customtkinter.CTkButton(self,text='Search', border_spacing=0, command=self.seerchDico)
            self.button.pack(padx=10, pady=10)
            
            self.title = customtkinter.CTkLabel(self, text='')
            self.title.pack()
            
            self.result = customtkinter.CTkTextbox(self, width=350, 
                                               height=250, state='disabled')
            self.result.pack()
        else:
            my_image = customtkinter.CTkImage(light_image=Image.open("caution.png"),
                                  dark_image=Image.open("caution.png"),size=(300, 300)
                                  )
            self.internetError = customtkinter.CTkLabel(self,image=my_image,text="" ,
                                                        highlightthickness=0, relief=tkinter.RIDGE, wrap=tkinter.WORD)
            self.internetError.pack(pady=50)
            self.internetErrorLabelerl = customtkinter.CTkLabel(self, text='Internet Required to use this Application'
                                                            ).pack(pady=4)
        

app = App()
app.mainloop()