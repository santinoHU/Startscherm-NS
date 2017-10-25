# import modules
import requests
import xmltodict
from tkinter import *
from PIL import ImageTk, Image

# assign color variables
bg = "#FFD723" # yellow
fg = "#013097" # blue

# creates GUI
root = Tk()
root.title("Welkom bij de NS")
root.geometry("450x533")
root.configure(background=bg)

# function that opens the search GUI
def command():
    top = Toplevel(root)
    top.title("Plan uw reis")
    top.configure(background=bg)
    top.geometry("450x533")

    # function to check search results
    def search():
        # enables the use of the ns-api
        auth_details = ('santino.denbrave@student.hu.nl', 'P_v4mmnZiBdVPeEOPsIzVbggnwm1T9EPYPwT0yDZX6vo7Q5rK3VLpw')
        api_url = 'http://webservices.ns.nl/ns-api-avt?station=' + entry.get()
        response = requests.get(api_url, auth=auth_details)

        # returns search-information
        vertrekXML = xmltodict.parse(response.text)
        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindbestemming = vertrek['EindBestemming']
            vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16]  # 18:36
            results["text"] = 'Om ' + vertrektijd + ' vertrekt een trein naar ' + eindbestemming
        subtitle.pack(pady=(40, 0))
        results.pack()

    # assign variables
    entry = Entry(top)
    description = Label(top, text="Voer hieronder station in waarvan u informatie wilt", foreground=fg, background=bg, font=('Helvetica'))
    searchbtn = Button(top, text="Zoeken", command=search)
    title = Label(top, text="Welkom bij NS", foreground=fg, background=bg, font=('Helvetica', 22, 'bold'))
    subtitle = Label(top, text="Dit zijn de vertrekkende treinen:\n", background=bg, font=('Helvetica', 16, 'bold'))
    results = Label(top, text="", background=bg)

    # prints the variables to the GUI
    title.pack()
    description.pack(pady=(40,0)) #pady works as a tuple: (top, bottom)
    entry.pack(padx=10, pady=10)
    searchbtn.pack()

# assign buttons
searchbtn = Button(master = root, text="Reis \nplannen", foreground="white", background=fg, command=command)
ticketbtn = Button(master = root, text="Kopen \n los kaartje", foreground="white", background=fg)
cardbtn = Button(master = root, text="Kopen \n OV-Chipkaart", foreground="white", background=fg)
abroadbtn = Button(master = root, text="Ik wil naar \n het buitenland", foreground="white", background=fg)

# assign image
img = ImageTk.PhotoImage(Image.open("img/ns_img.png"))

# assign labels
footer = Label(master = root, background=fg)
placeholder = Label(master = root, background=bg)
title = Label(text="Welkom bij NS", foreground="#002272", background=bg, font=('Helvetica', 22, 'bold'))
panel = Label(root, image = img, background=bg)

# shows variables on the GUI
title.pack(pady=20)
panel.pack(padx=10)
placeholder.pack(side=LEFT, padx=20)
searchbtn.pack(side=LEFT, padx=5, pady=80)
ticketbtn.pack(side=LEFT, padx=5, pady=80)
cardbtn.pack(side=LEFT, padx=5, pady=80)
abroadbtn.pack(side=LEFT, padx=5, pady=80)
footer.place(x=0, y=513, width=650)

# open GUI
root.mainloop()