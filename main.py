import tkinter as tk
from startseite import SpielStart, StartSeite
from wahlkampf_seite import WahlkampfSeite

class WahlkampfApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Bundestagswahl 2025")
        self.root.attributes("-fullscreen", True)

        # Variablen für ausgewählte Partei und Kandidaten-Daten initialisieren
        self.ausgewaehlte_partei = None
        self.kandidat_daten = {}

        # Container für Frames
        self.main_container = tk.Frame(root)
        self.main_container.pack(fill="both", expand=True)

        # Frames initialisieren
        self.frames = {}
        for F in (SpielStart, StartSeite, WahlkampfSeite):  # Weitere Seiten hinzufügen
            page_name = F.__name__
            frame = F(parent=self.main_container, controller=self)
            self.frames[page_name] = frame
            frame.place(relwidth=1, relheight=1)

        # Button zum Schließen des Programms
        self.erzeuge_schliessen_button()

        # Startseite anzeigen
        self.show_frame("SpielStart")

    def erzeuge_schliessen_button(self):
        """Erstellt einen globalen Schließen-Button oben rechts."""
        canvas = tk.Canvas(self.root, cursor="hand2", width=40, height=40, bg="red", highlightthickness=0)
        canvas.place(relx=0.98, rely=0.02, anchor="ne")  # Platzierung oben rechts

        # Zeichne das Kreuz
        canvas.create_line(10, 10, 30, 30, fill="black", width=3)
        canvas.create_line(30, 10, 10, 30, fill="black", width=3)

        # Klick-Event für das Schließen des Programms
        canvas.bind("<Button-1>", lambda event: self.root.destroy())

    def show_frame(self, page_name):
        """Zeigt den gewünschten Frame."""
        frame = self.frames[page_name]
        if page_name == "WahlkampfSeite":
            frame.update_data()  # Aktualisiere die Daten für den Wahlkampf-Frame
        frame.tkraise()

if __name__ == "__main__":
    root = tk.Tk()
    app = WahlkampfApp(root)
    root.mainloop()
