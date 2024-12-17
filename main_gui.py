import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess

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
    frame.config(highlightbackground="red", highlightthickness=4)
    aktueller_frame = frame

    # Gewählte Partei speichern
    ausgewaehlte_partei = partei

def start_wahlkampf(partei):
    """Startet das Wahlkampfskript."""
    try:
        root.destroy()
        subprocess.Popen(["python", "wahlkampf.py", partei])
    except Exception as e:
        messagebox.showerror("Fehler", f"Der Wahlkampf konnte nicht gestartet werden: {e}")

def erzeuge_kandidaten_frame(parent, partei, daten):
    """Erstellt einen Frame für einen Kandidaten."""
    frame = tk.Frame(parent, borderwidth=2, relief="groove", padx=10, pady=10, highlightbackground="black", highlightthickness=2)
    frame.grid(row=reihenfolge.index(partei) // 4, column=reihenfolge.index(partei) % 4, padx=10, pady=10)
    
    # Bild anzeigen
    try:
        if not os.path.exists(daten["bild"]):
            raise FileNotFoundError(f"Bild nicht gefunden: {daten['bild']}")
        image = Image.open(daten["bild"]).resize((150, 150), Image.Resampling.LANCZOS)
        photo = ImageTk.PhotoImage(image)
        tk.Label(frame, image=photo).pack()
        frame.image = photo  # Referenz verhindern
    except:
        tk.Label(frame, text="Bild fehlt!", font=("Arial", 12)).pack()

    # Text-Infos
    tk.Label(frame, text=f"Partei: {partei}", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(frame, text=f"Kandidat: {daten['name']}", font=("Arial", 12)).pack(anchor="w")
    tk.Label(frame, text=f"Kompetenz: {daten['kompetenz']}", font=("Arial", 12)).pack(anchor="w")
    tk.Label(frame, text=f"Beliebtheit: {daten['beliebtheit']}", font=("Arial", 12)).pack(anchor="w")
    tk.Label(frame, text=f"Ambition: {daten['ambition']}", font=("Arial", 12)).pack(anchor="w")
    
    # Wahl-Button
    tk.Button(frame, text="Wählen", font=("Arial", 12), command=lambda: waehlen(partei, frame)).pack(pady=5)

def setze_hintergrundbild(root, pfad):
    """Setzt ein Hintergrundbild für das Hauptfenster."""
    image = Image.open(pfad).resize((root.winfo_screenwidth(), root.winfo_screenheight()))
    bg_image = ImageTk.PhotoImage(image)
    bg_label = tk.Label(root, image=bg_image)
    bg_label.image = bg_image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    return bg_label

# Hauptprogramm
root = tk.Tk()
root.title("Bundestagswahl 2025")
root.attributes("-fullscreen", True)

# Überschrift
tk.Label(root, text="Wählen Sie Ihren Kanzlerkandidaten:", font=("Arial", 16, "bold")).pack(pady=10)

# Hintergrundbild setzen
setze_hintergrundbild(root, r"bilder\bundestag.jpg")

# Hauptframe für Kandidaten
main_frame = tk.Frame(root)
main_frame.pack(expand=True, padx=20, pady=20)

# Kandidaten anzeigen
reihenfolge = list(kandidaten.keys())
for partei in reihenfolge:
    erzeuge_kandidaten_frame(main_frame, partei, kandidaten[partei])

# Beenden-Button
tk.Button(root, text="Beenden", font=("Arial", 14), command=root.destroy).pack(side="bottom", pady=10)

# Hauptschleife starten
root.mainloop()