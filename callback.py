import webbrowser


# Opens webpage for tickets
def callbacktickets():
    webbrowser.open_new("https://www.ns.nl/producten/losse-kaartjes-toeslagen")


# Opens webpage for ov re-charging
def callbackcharge():
    webbrowser.open_new("https://www.ns.nl/reisinformatie/reizen-met-ov-chipkaart/saldo-laden-op-uw-ov-chipkaart.html")


# Opens webpage for going abroad by train
def callbackabroad():
    webbrowser.open_new("https://www.nsinternational.nl/")