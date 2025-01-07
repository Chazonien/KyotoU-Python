import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Kandidatendaten
kandidaten = {
    "SPD": {
        "name": "Olaf Scholz",
        "kompetenz": 75,
        "beliebtheit": 65,
        "ambition": 70,
        "bild": r"bilder\spd.jpg"
    },
    "CDU/CSU": {
        "name": "Friedrich Merz",
        "kompetenz": 80,
        "beliebtheit": 65,
        "ambition": 65,
        "bild": r"bilder/cdu.jpg"
    },
    "Grüne": {
        "name": "Robert Habeck",
        "kompetenz": 80,
        "beliebtheit": 70,
        "ambition": 60,
        "bild": r"bilder/gruene.jpg"
    },
    "FDP": {
        "name": "Christian Lindner",
        "kompetenz": 75,
        "beliebtheit": 60,
        "ambition": 75,
        "bild": r"bilder/fdp.jpg"
    },
    "AfD": {
        "name": "Alice Weidel",
        "kompetenz": 70,
        "beliebtheit": 60,
        "ambition": 80,
        "bild": r"bilder/afd.jpg"
    },
    "Linke": {
        "name": "van Aken & Reichinnek",
        "kompetenz": 65,
        "beliebtheit": 55,
        "ambition": 90,
        "bild": r"bilder/linke.jpg"
    },
    "BSW": {
        "name": "Sarah Wagenknecht",
        "kompetenz": 80,
        "beliebtheit": 65,
        "ambition": 75,
        "bild": r"bilder/bsw.jpg"
    }
}

class SpielStart(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Hintergrundbild
        self.setze_hintergrundbild(r"bilder/bundestag.jpg")

        # Spiel starten-Button
        tk.Label(self, text="Bundestagswahl 2025", font=("Arial", 24, "bold"), bg="white").pack(pady=50)
        tk.Button(self, text="Spiel starten", font=("Arial", 20), cursor="hand2",
                  command=lambda: controller.show_frame("StartSeite")).pack(pady=20)

    def setze_hintergrundbild(self, pfad):
        """Fügt ein Hintergrundbild in das Frame ein."""
        if not os.path.exists(pfad):
            print(f"Fehler: Bildpfad nicht gefunden: {pfad}")
            return
        
        # Hintergrundbild laden
        image = Image.open(pfad).resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)

        # Label für Hintergrundbild
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

class StartSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.aktueller_frame = None
        self.ausgewaehlte_partei = None  # Hier wird die gewählte Partei gespeichert

        # Hintergrundbild einfügen
        self.setze_hintergrundbild(r"bilder\bundestag.jpg")

        # Überschrift
        tk.Label(self, text="Wählen Sie Ihren Kanzlerkandidaten:", font=("Arial", 16, "bold")).pack(pady=10)

        # Hauptframe für Kandidaten
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(expand=True, padx=20, pady=20)

        # Kandidaten anzeigen
        self.reihenfolge = list(kandidaten.keys())
        for partei in self.reihenfolge:
            self.erzeuge_kandidaten_frame(self.main_frame, partei, kandidaten[partei])

        # Wahlkampf starten-Button
        self.wahlkampf_button = tk.Button(
            self, text="Wahlkampf starten", font=("Arial", 14),
            cursor="hand2", command=self.start_wahlkampf
        )
        self.wahlkampf_button.pack(side="bottom", pady=10)

    def setze_hintergrundbild(self, pfad):
        """Fügt ein Hintergrundbild in den Frame ein."""
        if not os.path.exists(pfad):
            print(f"Fehler: Bildpfad nicht gefunden: {pfad}")
            return
        
        # Bild laden und skalieren
        image = Image.open(pfad).resize((self.winfo_screenwidth(), self.winfo_screenheight()), Image.Resampling.LANCZOS)
        self.bg_image = ImageTk.PhotoImage(image)

        # Label für Hintergrundbild
        bg_label = tk.Label(self, image=self.bg_image)
        bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def waehlen(self, partei, frame):
        """Markiert den gewählten Kandidatenrahmen und speichert die gewählte Partei."""
        if self.aktueller_frame:
            self.aktueller_frame.config(highlightbackground="black", highlightthickness=2)

        frame.config(highlightbackground="green", highlightthickness=6)
        self.aktueller_frame = frame
        self.ausgewaehlte_partei = partei

        # Speichere die gewählte Partei und Kandidatendaten im Controller
        self.controller.ausgewaehlte_partei = partei
        self.controller.kandidat_daten = {
            "name": kandidaten[partei]["name"],
            "kompetenz": kandidaten[partei]["kompetenz"],
            "beliebtheit": kandidaten[partei]["beliebtheit"],
            "ambition": kandidaten[partei]["ambition"]
        }

    def start_wahlkampf(self):
        """Wechselt zur Wahlkampf-Seite oder zeigt eine Fehlermeldung."""
        if not self.ausgewaehlte_partei:
            messagebox.showerror("Fehler", "Bitte wählen Sie zuerst einen Kanzlerkandidaten aus!")
            return
        # Wechsle zum Wahlkampf-Frame
        self.controller.show_frame("WahlkampfSeite")

    def erzeuge_kandidaten_frame(self, parent, partei, daten):
        """Erstellt einen Frame für einen Kandidaten."""
        frame = tk.Frame(parent, borderwidth=2, relief="groove", padx=10, pady=10, highlightbackground="black", highlightthickness=2, width=200, height=300)
        frame.grid(row=self.reihenfolge.index(partei) // 4, column=self.reihenfolge.index(partei) % 4, padx=10, pady=10)
        frame.grid_propagate(False)

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
        tk.Button(frame, text="Wählen", font=("Arial", 10), cursor="hand2", command=lambda: self.waehlen(partei, frame)).pack(pady=5)