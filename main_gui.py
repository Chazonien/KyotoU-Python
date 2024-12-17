import tkinter as tk
import os
import sys
from PIL import Image, ImageTk
from tkinter import messagebox

# Kandidatendaten
kandidaten = {
    "SPD": {
        "name": "Olaf Scholz",
        "kompetenz": 75,
        "beliebtheit": 70,
        "ambition": 85,
        "bild": r"bilder\spd.jpg"
    },
    "CDU/CSU": {
        "name": "Friedrich Merz",
        "kompetenz": 90,
        "beliebtheit": 85,
        "ambition": 80,
        "bild": r"bilder/cdu.jpg"
    },
    "Grüne": {
        "name": "Robert Habeck",
        "kompetenz": 85,
        "beliebtheit": 90,
        "ambition": 70,
        "bild": r"bilder/gruene.jpg"
    },
    "FDP": {
        "name": "Christian Lindner",
        "kompetenz": 70,
        "beliebtheit": 60,
        "ambition": 95,
        "bild": r"bilder/fdp.jpg"
    },
    "AfD": {
        "name": "Alice Weidel",
        "kompetenz": 50,
        "beliebtheit": 40,
        "ambition": 95,
        "bild": r"bilder/afd.jpg"
    },
    "Linke": {
        "name": "van Aken & Reichinnek",
        "kompetenz": 65,
        "beliebtheit": 80,
        "ambition": 90,
        "bild": r"bilder/linke.jpg"
    },
    "BSW": {
        "name": "Sarah Wagenknecht",
        "kompetenz": 80,
        "beliebtheit": 75,
        "ambition": 85,
        "bild": r"bilder/bsw.jpg"
    }
}

# Globale Variablen
aktueller_frame = None
ausgewaehlte_partei = None  # Hier wird die gewählte Partei gespeichert

def waehlen(partei, frame):
    """Markiert den gewählten Kandidatenrahmen rot und speichert die gewählte Partei."""
    global aktueller_frame, ausgewaehlte_partei

    # Vorherigen Rahmen zurücksetzen
    if aktueller_frame:
        aktueller_frame.config(highlightbackground="black", highlightthickness=2)

    # Neuen Rahmen hervorheben
    frame.config(highlightbackground="green", highlightthickness=6)
    aktueller_frame = frame

    # Gewählte Partei speichern
    ausgewaehlte_partei = partei

def start_wahlkampf():
    """Startet das Wahlkampfskript und übergibt die gewählte Partei."""
    global ausgewaehlte_partei

    if not ausgewaehlte_partei:
        # Fehler anzeigen, wenn keine Partei ausgewählt wurde
        messagebox.showerror("Fehler", "Bitte wählen Sie zuerst einen Kanzlerkandidaten aus!")
        return
    
    try:
        # Ersetze den aktuellen Prozess durch das neue Python-Skript
        os.execv(sys.executable, [sys.executable, "wahlkampf.py", ausgewaehlte_partei])
    except Exception as e:
        messagebox.showerror("Fehler", f"Der Wahlkampf konnte nicht gestartet werden: {e}")

def erzeuge_kandidaten_frame(parent, partei, daten):
    """Erstellt einen Frame für einen Kandidaten mit fester Größe."""
    frame = tk.Frame(parent, borderwidth=2, relief="groove", padx=10, pady=10, highlightbackground="black", highlightthickness=2, width=200, height=300)
    frame.grid(row=reihenfolge.index(partei) // 4, column=reihenfolge.index(partei) % 4, padx=10, pady=10)
    frame.grid_propagate(False)  # Deaktiviert automatische Größenanpassung

    # Bild anzeigen
    try:
        if not os.path.exists(daten["bild"]):
            raise FileNotFoundError(f"Bild nicht gefunden: {daten['bild']}")
        image = Image.open(daten["bild"]).resize((100, 100), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        tk.Label(frame, image=photo).pack(pady=5)
        frame.image = photo  # Referenz verhindern
    except:
        tk.Label(frame, text="Bild fehlt!", font=("Arial", 12)).pack()

    # Text-Infos
    tk.Label(frame, text=f"Partei: {partei}", font=("Arial", 12, "bold"), anchor="w", width=25).pack()
    tk.Label(frame, text=f"Kandidat: {daten['name']}", font=("Arial", 10), anchor="w", width=25).pack()
    tk.Label(frame, text=f"Kompetenz: {daten['kompetenz']}", font=("Arial", 10), anchor="w", width=25).pack()
    tk.Label(frame, text=f"Beliebtheit: {daten['beliebtheit']}", font=("Arial", 10), anchor="w", width=25).pack()
    tk.Label(frame, text=f"Ambition: {daten['ambition']}", font=("Arial", 10), anchor="w", width=25).pack()

    # Wahl-Button
    tk.Button(frame, text="Wählen", font=("Arial", 10), cursor="hand2", command=lambda: waehlen(partei, frame)).pack(pady=5)

def setze_hintergrundbild(root, pfad):
    """Setzt ein Hintergrundbild für das Hauptfenster."""
    image = Image.open(pfad).resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return bg_label

def spiel_starten():
    """Blendet den Start-Frame aus und zeigt den Hauptframe an."""
    start_frame.pack_forget()  # Start-Frame ausblenden
    main_frame.pack(expand=True, padx=20, pady=20)  # Hauptframe anzeigen
    wahlkampf_button.pack(side="bottom", pady=10)  # Wahlkampf starten-Button anzeigen

# Hauptprogramm
root = tk.Tk()
root.title("Bundestagswahl 2025")
root.attributes("-fullscreen", True)

# Überschrift
tk.Label(root, text="Wählen Sie Ihren Kanzlerkandidaten:", font=("Arial", 16, "bold")).pack(pady=10)

# Hintergrundbild setzen
setze_hintergrundbild(root, r"bilder\bundestag.jpg")

# Start-Frame mit Spiel starten-Button
start_frame = tk.Frame(root, bg="white")
start_frame.pack(expand=True)
tk.Button(start_frame, text="Spiel starten", font=("Arial", 20), relief="raised", cursor="hand2", command=spiel_starten).pack(pady=0)

# Hauptframe für Kandidaten
main_frame = tk.Frame(root)

# Kandidaten anzeigen
reihenfolge = list(kandidaten.keys())
for partei in reihenfolge:
    erzeuge_kandidaten_frame(main_frame, partei, kandidaten[partei])

# Wahlkampf_starten-Button
wahlkampf_button = tk.Button(root, text="Wahlkampf starten", font=("Arial", 14), cursor="hand2", command=start_wahlkampf)

# Hauptschleife starten
root.mainloop()