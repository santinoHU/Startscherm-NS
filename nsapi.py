# import required modules
import requests
import xmltodict
import tkinter as tk
from PIL import ImageTk, Image

# function for button

def clicked():
    return
    # label["hoi"] = entry.get()

# creates root screen
root = tk.Tk()
search = tk.Tk()

# decide which screen shows
tk.homepage = tk.Frame(master = root)
tk.homepage.pack(fill="both", expand=True)

def showHomepage():
    tk.searchpage.pack_forget()
    tk.homepage.pack()
tk.searchpage = tk.Frame(master= search)
tk.searchpage.pack(fill="both", expand=True)


def showSearchpage():
    tk.homepage.pack_forget()
    tk.searchpage.pack()

# loginfield = tk.Entry(master=tk.homepage)
# loginfield.pack(padx=20, pady=20)
# loginbutton = tk.Button(master=tk.homepage, text='login', command=clicked)
# loginbutton.pack(padx=20, pady=20)

def login():
 if loginfield.get() == "admin":
    showSearchpage()
 else:
    print('Verkeerde gebruikersnaam!')


showHomepage()

bg = "#FFD723" # yellow - background color
fg = "#013097" # blue - foreground color
root.configure(background=bg)

# define variables of tkinter
title = tk.Label(text="Welkom bij NS", foreground="#002272", background=bg, font=('Helvetica', 22, 'bold'))
img = ImageTk.PhotoImage(Image.open("img/ns_img.png"))
placeholder = tk.Label(master = root, background=bg)
d_info = tk.Button(master = root, text="Ik wil naar \n Amsterdam", foreground="white", background=fg, command=clicked)
button2 = tk.Button(master = root, text="Kopen \n los kaartje", foreground="white", background=fg)
button3 = tk.Button(master = root, text="Kopen \n OV-Chipkaart", foreground="white", background=fg)
button4 = tk.Button(master = root, text="Ik wil naar \n het buitenland", foreground="white", background=fg)
footer = tk.Label(master = root, background=fg)

# print variables to the root
title.pack(pady=20)
panel = tk.Label(root, image = img, background=bg)
panel.pack(padx=10)
placeholder.pack(side=tk.LEFT, padx=20)
d_info.pack(side=tk.LEFT, padx=5, pady=80)
button2.pack(side=tk.LEFT, padx=5, pady=80)
button3.pack(side=tk.LEFT, padx=5, pady=80)
button4.pack(side=tk.LEFT, padx=5, pady=80)

# footer.pack(side=tk.BOTTOM, fill=tk.X)
footer.place(x=0, y=513, width=650)

# run root
root.mainloop()




# auth_details = ('santino.denbrave@student.hu.nl', 'P_v4mmnZiBdVPeEOPsIzVbggnwm1T9EPYPwT0yDZX6vo7Q5rK3VLpw')
# api_url = 'http://webservices.ns.nl/ns-api-avt?station=alphen'
# response = requests.get(api_url, auth=auth_details)
# # print(response.text)
#
# vertrekXML = xmltodict.parse(response.text)
#
# print('Dit zijn de vertrekkende treinen:')
# for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
#  eindbestemming = vertrek['EindBestemming']
#  vertrektijd = vertrek['VertrekTijd'] # 2016-09-27T18:36:00+0200
#  vertrektijd = vertrektijd[11:16] # 18:36
#  print('Om '+ vertrektijd+' vertrekt een trein naar '+ eindbestemming)
# with open('vertrektijden.xml', 'w') as myXMLFile:
#  myXMLFile.write(response.text)
