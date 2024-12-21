def event_library(identity):

    if identity == "A":
        img = r"bilder\laschet_lacht.png"
        head = "Du lachst während der Flutkatastrophe"
        text = "Der Bundespräsident hält eine Rede im Katastrophengebiet bei der das ganze Gebiet in Verwüstung hinterlassen hat und mehrere Menschen tödlich umgekommen sind. Dooferweise stehst du neben einer semi-witzigen Person und musst unkontrolliert lachen bei diesem sehr seriösen Event."
        opt1 = "Du entschuldigst dich zu tiefst bei jedem folgenden Wahlkampfevent"
        w1 = -1
        opt2 = "Du rufst bei der BILD an und lässt einen zweiseitigen Artikel schreiben, wo u.a. der Witz erzählt wird."
        w2 = -2
        opt3 = "Du entscheidest dich beim Tageschau-Interview den Witz zu erzählen du bist der einzige der lacht."
        w3 = -3
    
    return img, head, text, opt1, opt2, opt3, w1, w2, w3