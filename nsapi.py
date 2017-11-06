# import modules
import requests
import xmltodict
from tkinter import *
from PIL import ImageTk, Image
from auth import *

# assign color variables
bg = "#FFD723" # yellow
fg = "#013097" # blue

# creates home GUI
root = Tk()
root.title("Welkom bij de NS")
root.geometry("450x550")
root.resizable(width=False, height=False)
root.configure(background=bg)

# assign buttons
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


# function that opens the search GUI
def command():
    # create search GUI
    top = Toplevel(root)
    top.title("Plan uw reis")
    top.configure(background=bg)
    top.geometry("450x550")
    top.resizable(width=False, height=False)
    top.withdraw()

    root.withdraw()
    top.deiconify()

    # function to check search results
    def search():
        search_url = api_url + entry_from.get()
        # sets the default to alphen if there is no input
        if search_url == 'http://webservices.ns.nl/ns-api-avt?station=':
            search_url = 'http://webservices.ns.nl/ns-api-avt?station=alphen'
        response = requests.get(search_url, auth=auth_details)
        # returns search-information
        vertrekXML = xmltodict.parse(response.text)
        count = 0
        # subtitle.pack(pady=(20, 0))
        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            # displays a maximum of 10 trains on the screen
            if count <= 9:
                eindbestemming = vertrek['EindBestemming']
                vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
                vertrektijd = vertrektijd[11:16]  # 18:36
                vertrekspoor = vertrek['VertrekSpoor'] # returns ordered dict
                trein = vertrek['TreinSoort']
                results = Label(top, text="", background=bg, foreground=fg, font=("bold"))
                # if entry_to.get() in eindbestemming.lower() and opmerking != "":
                #     results["text"] = "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + opmerking
                #     results.pack()
                # el
                if entry_to.get() in eindbestemming.lower():
                    results["text"] = "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + " vanaf spoor " + vertrekspoor['#text']
                    if vertrekspoor["@wijziging"] == 'true':
                        results["text"] = "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + \
                                          vertrekspoor['#text'] + "\n !Let op: Spoorswijziging"

                    results.pack()
                count += 1

    def showhome():
        root.deiconify()
        top.withdraw()

    # assign variables
    entry_from = Entry(top)
    backbttn = Button(top, text="Home", command=showhome)
    from_txt = Label(top, text="van*", foreground=fg, background=bg, font=('Helvetica'))
    entry_to = Entry(top)
    to_txt = Label(top, text="naar", foreground=fg, background=bg, font=('Helvetica'))
    description = Label(top, text="Of zoek uw reis handmatig:", foreground=fg, background=bg, font=('Helvetica'))
    footer2 = Label(master=top, background=fg)
    searchbttn = Button(top, text="Zoeken", command=search)
    currentbttn = Button(top, text="Huidige stationsinformatie", command=search)
    title = Label(top, text="Welkom bij NS", foreground=fg, background=bg, font=('Helvetica', 22, 'bold'))
    # subtitle = Label(top, text="Dit zijn de vertrekkende treinen:\n", foreground=fg, background=bg, font=('Helvetica'))

    # prints the variables to the GUI
    title.pack(pady=(20,0)) # pady works as a tuple: (top, bottom)
    backbttn.pack(pady=(20,0))
    currentbttn.pack(pady=(10,0))
    description.pack(pady=(10,0))
    from_txt.pack()
    entry_from.pack(padx=10, pady=0)
    entry_from.focus() # allows you to type in this inputfield without clicking first
    to_txt.pack()
    entry_to.pack(padx=10, pady=0)
    searchbttn.pack(pady=(15,25))
    footer2.pack(side=BOTTOM, fill=X)


# shows variables on the GUI
title.pack(pady=20)
panel.pack(padx=10)
placeholder.pack(side=LEFT, padx=20)
searchbtn = Button(master = root, text="Reis \nplannen", foreground="white", background=fg, command=command).pack(side=LEFT, padx=5, pady=80)
ticketbtn.pack(side=LEFT, padx=5, pady=80)
cardbtn.pack(side=LEFT, padx=5, pady=80)
abroadbtn.pack(side=LEFT, padx=5, pady=80)
footer.place(x=0, y=530, width=650)

# open GUI
root.mainloop()