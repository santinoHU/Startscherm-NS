# import modules
from auth import *
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter.ttk as tkk
import requests
import webbrowser
import xmltodict

# all stations to a tuple
def allstations():
    stationlist = []
    stations_url = "http://webservices.ns.nl/ns-api-stations"
    response = requests.get(stations_url, auth=auth_details)
    stationsXML = xmltodict.parse(response.text)
    for station in stationsXML['stations']['station']:
        stationlist.append(station['name'])
    return tuple(stationlist)


# Opens webpage
def callback():
    webbrowser.open_new(r"https://www.ns.nl")


# all NS staions
stations = allstations()

# assign color variables
bg = "#FFD723" # yellow
fg = "#013097" # blue

# creates home GUI
root = Tk()
root.configure(background=bg)
root.geometry("450x550")
root.resizable(width=False, height=False)
root.title("Welkom bij de NS")

# assign buttons
abroadbtn = Button(master = root, text="Ik wil naar \n het buitenland", foreground="white", background=fg, command=callback)
cardbtn = Button(master = root, text="OV-Chipkaart \n opladen", foreground="white", background=fg, command=callback)
ticketbtn = Button(master = root, text="Kopen \n los kaartje", foreground="white", background=fg, command=callback)

# assign image
nsimg = ImageTk.PhotoImage(Image.open("img/ns_img.png"))

# assign labels
footer = Label(master = root, background=fg)
panel = Label(root, image = nsimg, background=bg)
placeholder = Label(master = root, background=bg)
title = Label(text="Welkom bij NS", foreground="#002272", background=bg, font=('Helvetica', 22, 'bold'))

# opens the search GUI
def command():
    # create search GUI
    top = Toplevel(root)
    top.configure(background=bg)
    top.geometry("450x550")
    top.resizable(width=False, height=False)
    top.title("Plan uw reis")

    root.withdraw()

    # creates textbox for results
    results = Text(top, background=bg, foreground=fg, font=("bold", 10), wrap=NONE, padx=5, pady=5)

    # checks stationinfo results
    def stationinfo():
        results.delete('0.0', END)

        # getting formatted entry from the combobox
        departure = str(entry_from.get()).replace(' ', '+')

        search_url = api_url_station + departure
        # sets the default to alphen
        if search_url == 'http://webservices.ns.nl/ns-api-avt?station=':
            search_url = 'http://webservices.ns.nl/ns-api-avt?station=alphen'

        response = requests.get(search_url, auth=auth_details)
        departureXML = xmltodict.parse(response.text)

        # checks if station is foreign
        try:
            if departureXML['error']['message'] == 'Foreign stations are not supported.':
                messagebox.showinfo("Error", "Buitenlandse stations kunt u hiervoor niet gebruiken.")
                return
        except:
            pass

        for train in departureXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            destination = train['EindBestemming']
            departuretime = train['VertrekTijd']  # 2016-09-27T18:36:00+0200
            departuretime = departuretime[11:16]  # 18:36
            tracknr = train['VertrekSpoor']  # returns ordered dict
            type = train['TreinSoort']

            if tracknr["@wijziging"] == 'true':
                results.insert(0.0, "Om " + departuretime + " vertrekt de " + type + " naar " + destination + tracknr['#text'] + "\n !Let op: Spoorswijziging")
            else:
                results.insert(0.0, "Om " + departuretime + " vertrekt de " + type + " naar " + destination + " vanaf spoor " + tracknr['#text'] + "\n")

            results.pack(side=LEFT, fill='both', expand=YES, padx=5, pady=5)


    # checks route information results
    def routeinformation():
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
        departure = 'fromStation=' + str(entry_from.get()).replace(' ', '+')
        eindstation = 'toStation=' + str(entry_to.get()).replace(' ', '+')

        search_url = api_url_route + departure + '&' + eindstation
        # sets the default to Alphen if there is no input
        if search_url == 'http://webservices.ns.nl/ns-api-treinplanner?':
            search_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation=Utrecht+Centraal&toStation=Woerden'
        response = requests.get(search_url, auth=auth_details)
        departureXML = xmltodict.parse(response.text)
        print(departureXML)

        for train in departureXML['ReisMogelijkheden']['ReisMogelijkheid']:
            print(train)


    def showhome():
        root.deiconify()
        top.withdraw()


    # create field, dropdown menu and default value
    entry_from = tkk.Combobox(top)
    entry_from.insert(END, 'Alphen a/d Rijn')
    entry_from['values'] = stations

    homebtn = Button(top, text="terug", font=('Helvetica'), command=showhome)
    from_text = Label(top, text="van", foreground=fg, background=bg, font=('Helvetica'))

    # create entry_to field and dropdown menu
    entry_to = tkk.Combobox(top)
    entry_to['values'] = stations

    to_text = Label(top, text="naar", foreground=fg, background=bg, font=('Helvetica'))
    description = Label(top, text="Of zoek uw reis handmatig:", foreground=fg, background=bg, font=('Helvetica'))
    footer = Label(master=top, background=fg)
    currentbtn = Button(top, text="Huidige stationsinformatie", command=stationinfo)
    searchbtn = Button(top, text="Traject informatie", command=routeinformation)
    title = Label(top, text="Welkom bij NS", foreground=fg, background=bg, font=('Helvetica', 22, 'bold'))

    # prints the variables to the GUI
    homebtn.pack(padx=(0,393), pady=(7,0))
    title.pack(pady=(20,0)) # pady works as a tuple: (top, bottom)
    currentbtn.pack(pady=(10,0))
    description.pack(pady=(10,0))
    from_text.pack()
    entry_from.pack(padx=10, pady=0)
    entry_from.focus() # allows you to type in this inputfield without clicking first
    to_text.pack()
    entry_to.pack(padx=10, pady=0)
    searchbtn.pack(pady=(15,25))
    footer.pack(side=BOTTOM, fill=X)


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