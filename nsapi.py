import requests
import xmltodict
from tkinter import *

root = Tk()

label = Label(master=root, text="Ik wil naar \n Amsterdam", background="blue")

label.pack()

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
