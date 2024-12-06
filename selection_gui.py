import tkinter as tk
import os
from tkinter import messagebox
from PIL import Image, ImageTk
import subprocess  # To run wahlkampf.py

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

# Wahlfunktion
def waehlen(partei):
    messagebox.showinfo("Wahl bestätigt", f"Sie haben {kandidaten[partei]['name']} von der {partei} gewählt!")
    # Nach der Wahl startet der Wahlkampf
    start_wahlkampf(partei)

# Wahlkampf starten
def start_wahlkampf(partei):
    # Führt das Skript wahlkampf.py mit der gewählten Partei als Argument aus
    try:
        subprocess.Popen(["python", "wahlkampf.py", partei])
        root.destroy()  # Hauptfenster schließen
    except Exception as e:
        messagebox.showerror("Fehler", f"Der Wahlkampf konnte nicht gestartet werden: {e}")

# Hauptfenster erstellen
root = tk.Tk()
root.title("Bundestagswahl 2025")
root.attributes("-fullscreen", True)  # Fullscreen aktivieren

# Überschrift
header = tk.Label(root, text="Wählen Sie Ihren Kanzlerkandidaten:", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Hauptrahmen für die Kandidaten
main_frame = tk.Frame(root)
main_frame.pack(expand=True, padx=20, pady=20)

# Kandidaten in einem Grid anordnen
reihenfolge = list(kandidaten.keys())
for i, partei in enumerate(reihenfolge):
    daten = kandidaten[partei]
    # Frame für jeden Kandidaten
    frame = tk.Frame(main_frame, borderwidth=2, relief="groove", padx=10, pady=10)
    frame.grid(row=i // 4, column=i % 4, padx=10, pady=10)  # 4 Spalten, dann nächste Reihe

    # Bild laden
    try:
        if not os.path.exists(daten["bild"]):
            raise FileNotFoundError(f"Bild nicht gefunden: {daten['bild']}")
        image = Image.open(daten["bild"])
        image = image.resize((150, 150), Image.Resampling.LANCZOS)  # Pillow 9.1.0 oder neuer
        photo = ImageTk.PhotoImage(image)
        bild_label = tk.Label(frame, image=photo)
        bild_label.image = photo  # Referenz speichern, um GC zu verhindern
        bild_label.pack()
    except Exception as e:
        print(f"Fehler beim Laden des Bildes für {daten['name']}: {e}")
        tk.Label(frame, text="Bild fehlt!", font=("Arial", 12)).pack()

    # Partei- und Kandidateninformationen
    tk.Label(frame, text=f"Partei: {partei}", font=("Arial", 14, "bold")).pack(anchor="w")
    tk.Label(frame, text=f"Kandidat: {daten['name']}", font=("Arial", 12)).pack(anchor="w")
    tk.Label(frame, text=f"Kompetenz: {daten['kompetenz']}", font=("Arial", 12)).pack(anchor="w")
    tk.Label(frame, text=f"Beliebtheit: {daten['beliebtheit']}", font=("Arial", 12)).pack(anchor="w")
    tk.Label(frame, text=f"Ambition: {daten['ambition']}", font=("Arial", 12)).pack(anchor="w")
    
    # Wahl-Button
    tk.Button(frame, text="Wählen", font=("Arial", 12), command=lambda p=partei: waehlen(p)).pack(pady=5)

# Beenden-Button
beenden_button = tk.Button(root, text="Beenden", font=("Arial", 14), command=root.destroy)
beenden_button.pack(side="bottom", pady=10)

# Hauptschleife starten
root.mainloop()