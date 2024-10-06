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
        scorrableTitle ="Result word for " + serachWords
        response = self.queryApi(serachWords)
        self.scrollable.configure(label_text=scorrableTitle)
        
        if(response[0]):
             for idx, value in enumerate(iterable=response[1]):
                 defini = str(idx + 1) + ' - { '+ value['partOfSpeech'] + ' } ' + value['definition']
                 self.result = customtkinter.CTkLabel(self.scrollable, width=550, height=10, 
                                                 text=defini, text_color='black',wraplength=500,
                                                 compound="left", justify="left", anchor="w"
                                                 ).pack(pady=(0, 10),expand = True,side = 'top', fill='both')
                
        else:
            self.result = customtkinter.CTkLabel(self.scrollable, width=350, height=10, 
                                                 text=response[1], text_color='black',wraplength=500,
                                                 compound="left", justify="left", anchor="w"
                                                 ).pack(pady=5)
            
    def __init__(self):
        super().__init__()

        self.title("Dictionary")
        self.geometry("650x550")
        self._set_appearance_mode('system')
        self.wm_iconbitmap('dico.ico')
        # self.iconbitmap('dico.png')
        
        if self.check_internet():
            
            self.title = customtkinter.CTkLabel(self,text='Enter your search word below:',
                                                    fg_color='transparent')
            self.title.pack(padx=10, pady=10)

            searchWords = tkinter.StringVar()
            self.search =  customtkinter.CTkEntry(self,width=550, 
                                                height=40, 
                                                corner_radius=10,
                                                textvariable=searchWords,
                                                placeholder_text='Enter your words')
            self.search.pack(padx=10,pady=10)

            self.scrollable = customtkinter.CTkScrollableFrame(self,width=550, height=300, fg_color='white')
            self.scrollable.pack(padx=10, pady=10)


            self.button = customtkinter.CTkButton(self,text='Search', border_spacing=0, command=self.seerchDico)
            self.button.pack(padx=10, pady=10)
        else:
            my_image = customtkinter.CTkImage(light_image=Image.open("caution.png"),
                                  dark_image=Image.open("caution.png"),size=(300, 300)
                                  )
            self.internetError = customtkinter.CTkLabel(self,image=my_image,text="")
            self.internetError.pack(pady=50)
            self.internetErrorLabelerl = customtkinter.CTkLabel(self, text='Internet Required to use this Application'
                                                            ).pack(pady=4)
        

app = App()
app.mainloop()