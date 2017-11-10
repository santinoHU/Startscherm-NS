"""
This project is made by:
    - Santino den Brave
    - Lucas van den Berg
    - Paul Kuster
    - Youri Okkerse
    - Nicky Schoenmakers
    - Youri Mulder

    Don't forget to visit the NS site: https://www.ns.nl/reisinformatie/ns-api
"""



# import modules
from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import tkinter.ttk as tkk
import requests
import xmltodict

# import our own files
from auth import *
from callback import *


def check_route_stations(vertrek, eind, stations):
    if vertrek not in stations:
        messagebox.showinfo("Error", "Het vertrekstation bestaat niet")
        return False
    if eind not in stations:
        messagebox.showinfo("Error", "Het eindstation bestaat niet")
        return False
    if vertrek == eind:
        messagebox.showinfo("Error", "U kunt niet naar hetzelfde station reizen")
        return False


# all stations to a tuple
def allstations():
    stationlist = []
    stations_url = "http://webservices.ns.nl/ns-api-stations"

    # get response and decode it UTF-8
    response = requests.get(stations_url, auth=auth_details)
    response.encoding = 'UTF-8'

    stationsXML = xmltodict.parse(response.text)
    for station in stationsXML['stations']['station']:
        stationlist.append(station['name'])
    return tuple(stationlist)

# disabled the exception messages to keep the console clean
def getrails(stationlist):
    # deze lijst wordt gevuld met de sporen
    allstationrails = []
    global station

    # try catch for the whole function
    try:
        # tries to get the rails without a double for loop
        try:
            station = stationlist['ReisDeel']['ReisStop']
            for s in station:
                try:
                    spoor = s['Spoor']['#text']
                    # als er een spoor in het XML bestand staat return het
                    if spoor == '#text':
                        pass
                    if spoor == 'Spoor':
                        allstationrails.append('- ')
                    else:
                        allstationrails.append(spoor + " ")
                except Exception as e:
                    pass
                    # print("getrails try 1.1:", e)
        except Exception as e:
            pass
            # print("getrails try 1:", e)

        # tries to get the rails with a double for loop
        try:
            for station in stationlist['ReisDeel']:
                for s in station['ReisStop']:
                    try:
                        spoor = s['Spoor']['#text']
                        # als er een spoor in het XML bestand staat return het
                        if spoor == '#text':
                            pass
                        if spoor == 'Spoor':
                            allstationrails.append('- ')
                        else:
                            allstationrails.append(spoor + " ")
                    except Exception as e:
                        pass
                        # print("getrails try 2.1:", e)
        except Exception as e:
            pass
            # print("getrails try 2:", e)
    except Exception as e:
        pass
        # print(e)
    return allstationrails


# all NS staions
stations = allstations()

# assign color variables
bg = "#FFD723" # yellow
fg = "#013097" # blue

# creates home GUI
root = Tk()
root.configure(background=bg)
root.geometry("900x550")
root.resizable(width=False, height=False)
root.title("Welkom bij de NS")

# assign buttons
abroadbtn = Button(master = root, text="Ik wil naar \n het buitenland", foreground="white", background=fg, command=callbackabroad)
cardbtn = Button(master = root, text="OV-Chipkaart \n opladen", foreground="white", background=fg, command=callbackcharge)
ticketbtn = Button(master = root, text="Kopen \n los kaartje", foreground="white", background=fg, command=callbacktickets)

# assign image
nsimg = ImageTk.PhotoImage(Image.open("img/ns_img.png"))

#assign icon image
root.iconbitmap("img/ns_logo_icon.ico")

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
    top.geometry("900x550")
    top.resizable(width=False, height=False)
    top.title("Plan uw reis")
    top.iconbitmap("img/ns_logo_icon.ico")
    root.withdraw()



    txtframe = Frame(top, background=bg, padx=5, pady=5)
    results = Text(txtframe, background=bg, foreground=fg, font=('Consolas', 8), wrap=NONE, relief=FLAT)
    scrollresulty = Scrollbar(txtframe, command=results.yview, cursor="hand2")
    scrollresultx = Scrollbar(txtframe, orient=HORIZONTAL, command=results.xview, cursor="hand2")

    results['xscroll'] = scrollresultx.set
    results['yscroll'] = scrollresulty.set

    scrollresulty.pack(side=RIGHT, fill=Y)
    scrollresultx.pack(side=BOTTOM, fill=X)


    # checks stationinfo results
    def stationinfo():
        results.delete('0.0', END)

        # getting formatted entry from the combobox
        departure = str(entry_from.get()).replace(' ', '+')

        search_url = api_url_station + departure
        # sets the default to alphen
        if search_url == 'http://webservices.ns.nl/ns-api-avt?station=':
            search_url = 'http://webservices.ns.nl/ns-api-avt?station=alphen'

        # get response and decode it UTF-8
        response = requests.get(search_url, auth=auth_details)
        response.encoding = 'UTF-8'

        departureXML = xmltodict.parse(response.text)

        # checks if station is foreign
        try:
            if departureXML['error']['message'] == 'Foreign stations are not supported.':
                messagebox.showinfo("Error", "Buitenlandse stations kunt u hiervoor niet gebruiken.")
                return
            elif departureXML['error']['message'].startswith("Error while trying to get departure information for station"):
                messagebox.showinfo("Error", "Op het moment kunnen wij niet de data van NS verkrijgen.\n"
                                             "probeer later nog eens!")
                return
        except Exception as e:
            # print("XML mention check:", e)
            pass

        for train in departureXML['ActueleVertrekTijden']['VertrekkendeTrein']:
            destination = train['EindBestemming']
            departuretime = train['VertrekTijd']  # 2016-09-27T18:36:00+0200
            departuretime = departuretime[11:16]  # 18:36
            tracknr = train['VertrekSpoor']  # returns ordered dict
            type = train['TreinSoort']

            if tracknr["@wijziging"] == 'true':
                results.insert(END, "Om " + departuretime + " vertrekt de " + type + " naar " + destination + tracknr['#text'] + "\n !Let op: Spoorswijziging")
            else:
                results.insert(END, "Om " + departuretime + " vertrekt de " + type + " naar " + destination + " vanaf spoor " + tracknr['#text'] + "\n")

            # display textbox
            txtframe.pack(side=BOTTOM, fill=X)
            results.pack(side=LEFT, fill='both', expand=YES, padx=5, pady=5)


    # checks route information results
    def routeinformation():
        # Variable for mention check
        eerstemelding = True

        # deletes text box before putting in some other text
        results.delete('0.0', END)

        # check if both fields are filled in
        if entry_from.get() is "":
            messagebox.showinfo("Error", "Zorg ervoor dat het beginstation is ingevuld")
            return
        if entry_to.get() is "":
            messagebox.showinfo("Error", "Zorg ervoor dat het eindstation is ingevuld")
            return

        # getting formatted entries from the comboboxes
        start = entry_from.get()
        end = entry_to.get()
        departure = 'fromStation=' + str(start).replace(' ', '+')
        destination = 'toStation=' + str(end).replace(' ', '+')
        print(destination)

        # checks if is input is valid
        if check_route_stations(start, end, stations) == False:
            return

        search_url = api_url_route + departure + '&' + destination
        # sets the default to alphen if there is no input
        if search_url == 'http://webservices.ns.nl/ns-api-treinplanner?':
            search_url = 'http://webservices.ns.nl/ns-api-treinplanner?fromStation=Utrecht+Centraal&toStation=Wierden'

        # get response and decode it UTF-8
        response = requests.get(search_url, auth=auth_details)
        response.encoding = 'UTF-8'

        vertrekXML = xmltodict.parse(response.text)

        # checks if route is possible
        if vertrekXML['ReisMogelijkheden'] is None:
            messagebox.showinfo("Error", "Deze reis is niet mogelijk probeer andere stations")
            return


        for vertrek in vertrekXML['ReisMogelijkheden']['ReisMogelijkheid']:
            melding = False

            # assigns variables when there is a adjusted schedule
            try:
                id = vertrek['Melding']['Id']
                ernstig = vertrek['Melding']['Ernstig']
                text = vertrek['Melding']['Text']
                melding = True

            # exception raised when there isn't mention on the track
            except Exception as e:
                # print("NS mention variables", e)
                pass

            try:
                aantaloverstappen = vertrek['AantalOverstappen']
                geplandereistijd = vertrek['GeplandeReisTijd']  # 11:05
                actuelereistijd = vertrek['ActueleReisTijd']  # 11:05
                optimaal = vertrek['Optimaal']
                geplandevertrektijd = vertrek['GeplandeVertrekTijd']  # 2016-09-27T18:36:00+0200
                actuelevertrektijd = vertrek['ActueleVertrekTijd']  # 2016-09-27T18:36:00+0200
                geplandeaankomsttijd = vertrek['GeplandeAankomstTijd']  # 2016-09-27T18:36:00+0200
                actueleaankomsttijd = vertrek['ActueleAankomstTijd']  # 2016-09-27T18:36:00+0200
                status = vertrek['Status']

                # formats the time of departure and destination
                f_actuelevertrektijd = actuelevertrektijd[5:10] + ":" + actuelevertrektijd[11:16]
                f_actueleaankomsttijd = actueleaankomsttijd[5:10] + ":" + actueleaankomsttijd[11:16]
            except Exception as e:
                print(e)
                print("Exception raised when assiging routeinformation variables")

            try:
                # created the departure and destination variables
                sporen = getrails(vertrek)
                opstapsporen = ['    ']  # the spaces are there make it look nice in the output
                afstapsporen = ['    ']  # the spaces are there make it look nice in the output

                # checks if passenger should get in or out the train
                for i in range(len(sporen)):
                    if i % 2 == 0:
                        opstapsporen.append(sporen[i])
                    else:
                        afstapsporen.append(sporen[i])
            except Exception as e:
                print(e)
                print("Exception raised when trying to handling rails")


            # if there is an change in route there will be a message, END to reverse the order
            if melding:
                if eerstemelding:
                    messagebox.showinfo("PAS OP!", "Er is een melding op dit traject\n" + text)
                    eerstemelding = False
                if ernstig:
                    results.insert(END, "PAS OP! De volgende reis heeft een melding (Het is ernstig): " + text + "\n")
                else:
                    results.insert(END, "PAS OP! De volgende reis heeft een melding: " + text + "\n")


            result = "{:^30s}|{:^11s}|{:^36s}|{:^15s}|{:^11s} |{:^10s}|{:^15}|{:<15}|{:<15}|\n".format(entry_from.get(), f_actuelevertrektijd, entry_to.get(), aantaloverstappen, f_actueleaankomsttijd, actuelereistijd, status, ''.join(opstapsporen), ''.join(afstapsporen))

            # Handling output. The headers are handled outside the for loop, END to reverse the order
            results.insert(END, result)

            # display textbox
            txtframe.pack(side=BOTTOM, fill=X)
            results.pack(side=LEFT, fill='both', expand=YES, padx=5, pady=5)

        # make a table to display
        results.insert(1.0,"{:^30s}|{:^11s}|{:^36s}|{:^15s}|{:^11s}|{:^10s}|{:^15}|{:^15}|{:^15}|\n".format("Vertrekstation", "Vertrektijd", "Eindstation", "Overstappen", "Aankomsttijd", "Reistijd", "Status", "Opstapsporen", "Afstapsporen"))
        # creates line between results and the header
        results.insert(2.0, '-' * len(result) +"\n")

    def showhome():
        root.deiconify()
        top.withdraw()


    entry_from = tkk.Combobox(top, width=30)
    entry_from.insert(END, 'Alphen a/d Rijn')
    entry_from['values'] = stations

    homebtn = Button(top, text="Terug", font=('Helvetica', 10), foreground="white", background=fg, command=showhome)
    from_text = Label(top, text="van", foreground=fg, background=bg, font=('Helvetica', 12, 'bold'))

    # create entry_to field and dropdown menu
    entry_to = tkk.Combobox(top, width=30)
    entry_to['values'] = stations


    # create field, dropdown menu and default value
    to_text = Label(top, text="naar", foreground=fg, background=bg, font=('Helvetica', 12, 'bold'))
    description = Label(top, text="Of zoek uw reis handmatig:", foreground=fg, background=bg, font=('Helvetica', 12, 'bold'))
    footer = Label(master=top, background=fg)
    currentbtn = Button(top, text="Huidige stationsinformatie", foreground="white", background=fg, command=stationinfo)
    searchbtn = Button(top, text="Traject informatie", foreground="white", background=fg, command=routeinformation)
    title = Label(top, text="Welkom bij NS", foreground=fg, background=bg, font=('Helvetica', 22, 'bold'))

    # prints the variables to the GUI
    homebtn.pack(padx=(0, 843), pady=(7,0))
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
placeholder.pack(side=LEFT, padx=140)
searchbtn = Button(master=root, text="Reis \nplannen", foreground="white", background=fg, command=command).pack(side=LEFT, padx=5, pady=80)
ticketbtn.pack(side=LEFT, padx=5, pady=80)
cardbtn.pack(side=LEFT, padx=5, pady=80)
abroadbtn.pack(side=LEFT, padx=5, pady=80)
footer.place(x=0, y=530, width=root.winfo_screenwidth())

# open GUI
root.mainloop()
