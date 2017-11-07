# import modules
import requests
import xmltodict
from tkinter import *
from tkinter import messagebox
import tkinter.ttk as tkk
from PIL import ImageTk, Image
from auth import *


# all stations to a tuple
def allstations():
    stationlist = []
    stations_url = "http://webservices.ns.nl/ns-api-stations"
    response = requests.get(stations_url, auth=auth_details)
    stationsXML = xmltodict.parse(response.text)
    for station in stationsXML['stations']['station']:
        stationlist.append(station['name'])
    return tuple(stationlist)


# all NS staions
stations = allstations()


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

    # create textbox for results
    results = Text(top, background=bg, foreground=fg, font=("bold", 10), wrap=NONE, padx=5, pady=5)

    # function to check stationinformation results
    def stationsinformatie():
        # deletes text box before putting in some other text
        results.delete('0.0', END)

        # getting formatted entry from the combobox
        vertrekstation = str(entry_from.get()).replace(' ', '+')


        search_url = api_url_station + vertrekstation
        print(search_url)
        # sets the default to alphen if there is no input
        if search_url == 'http://webservices.ns.nl/ns-api-avt?station=':
            search_url = 'http://webservices.ns.nl/ns-api-avt?station=alphen'

        response = requests.get(search_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)

        # checks if station is foreign
        try:
            if vertrekXML['error']['message'] == 'Foreign stations are not supported.':
                messagebox.showinfo("Error", "Buitenlandse stations kunt u hiervoor niet gebruiken.")
                return
        except:
            pass

        for vertrek in vertrekXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            eindbestemming = vertrek['EindBestemming']
            vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
            vertrektijd = vertrektijd[11:16]  # 18:36
            vertrekspoor = vertrek['VertrekSpoor']  # returns ordered dict
            trein = vertrek['TreinSoort']

            if vertrekspoor["@wijziging"] == 'true':
                results.insert(0.0, "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + vertrekspoor['#text'] + "\n !Let op: Spoorswijziging")
            else:
                results.insert(0.0, "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + " vanaf spoor " + vertrekspoor['#text'] + "\n")

            results.pack(side=LEFT, fill='both', expand=YES, padx=5, pady=5)


    # function to check route information results
    def routeinformatie():
        # deletes text box before putting in some other text
        results.delete('0.0', END)

        # check if both fields are filled in
        if entry_from.get() is "":
            messagebox.showinfo("Error", "Zorg ervoor dat het beginstation is ingevuld.")
            return
        if entry_to.get() is "":
            messagebox.showinfo("Error", "Zorg ervoor dat het eindstation is ingevuld.")
            return


        # getting formatted entries from the comboboxes
        vertrekstation = 'fromStation=' + str(entry_from.get()).replace(' ', '+')
        eindstation = 'toStation=' + str(entry_to.get()).replace(' ', '+')


        search_url = api_url_route + vertrekstation + '&' + eindstation
        # sets the default to alphen if there is no input
        if search_url == 'http://webservices.ns.nl/ns-api-treinplanner?':
            search_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation=Utrecht+Centraal&toStation=Wierden'
        response = requests.get(search_url, auth=auth_details)
        vertrekXML = xmltodict.parse(response.text)
        print(vertrekXML)


        for vertrek in vertrekXML['ReisMogelijkheden']['ReisMogelijkheid']:
            print(vertrek)


            # eindbestemming = vertrek['EindBestemming']
            # vertrektijd = vertrek['VertrekTijd']  # 2016-09-27T18:36:00+0200
            # vertrektijd = vertrektijd[11:16]  # 18:36
            # vertrekspoor = vertrek['VertrekSpoor']  # returns ordered dict
            # trein = vertrek['TreinSoort']
            #
            # if entry_to.get() in eindbestemming.lower() and count <= 9:
            #     count += 1
            #     results.insert(0.0, "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + " vanaf spoor " + vertrekspoor['#text'] + "\n")
            #     if vertrekspoor["@wijziging"] == 'true':
            #         results.insert(0.0, "Om " + vertrektijd + " vertrekt de " + trein + " naar " + eindbestemming + vertrekspoor['#text'] + "\n !Let op: Spoorswijziging")
            #
            # results.pack(side=LEFT, fill='both', expand=YES, padx=5, pady=5)




    def showhome():
        root.deiconify()
        top.withdraw()

    # assign variables

    # create entry_from field, dropdown menu and default value
    entry_from = tkk.Combobox(top)
    entry_from.insert(END, 'Alphen a/d Rijn')
    entry_from['values'] = stations

    backbttn = Button(top, text="home", font=('Helvetica'), command=showhome)
    from_txt = Label(top, text="van*", foreground=fg, background=bg, font=('Helvetica'))

    # create entry_to field and dropdown menu
    entry_to = tkk.Combobox(top)
    entry_to['values'] = stations

    to_txt = Label(top, text="naar", foreground=fg, background=bg, font=('Helvetica'))
    description = Label(top, text="Of zoek uw reis handmatig:", foreground=fg, background=bg, font=('Helvetica'))
    footer2 = Label(master=top, background=fg)
    currentbttn = Button(top, text="Huidige stationsinformatie", command=stationsinformatie)
    searchbttn = Button(top, text="Traject informatie", command=routeinformatie)
    title = Label(top, text="Welkom bij NS", foreground=fg, background=bg, font=('Helvetica', 22, 'bold'))

    # prints the variables to the GUI
    backbttn.pack()
    title.pack(pady=(20,0)) # pady works as a tuple: (top, bottom)
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