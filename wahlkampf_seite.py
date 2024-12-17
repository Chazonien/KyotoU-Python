import tkinter as tk
from tkinter import messagebox

class WahlkampfSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Platzhalter für Widgets
        self.label_partei = tk.Label(self, text="", font=("Arial", 16, "bold"), bg="white")
        self.label_partei.pack(pady=10)

        self.label_kandidat = tk.Label(self, text="", font=("Arial", 14), bg="white")
        self.label_kandidat.pack(pady=5)

        self.label_kompetenz = tk.Label(self, text="", font=("Arial", 12), bg="white")
        self.label_kompetenz.pack(pady=5)

        self.label_beliebtheit = tk.Label(self, text="", font=("Arial", 12), bg="white")
        self.label_beliebtheit.pack(pady=5)

        self.label_ambition = tk.Label(self, text="", font=("Arial", 12), bg="white")
        self.label_ambition.pack(pady=5)

        # Platzhalter für Aktionen
        tk.Button(
            self, text="Aktion durchführen", font=("Arial", 14), cursor="hand2",
            command=self.durchfuehre_aktion
        ).pack(pady=10)

        # Beenden-Button
        tk.Button(
            self, text="Zurück zum Hauptmenü", font=("Arial", 14), cursor="hand2",
            command=lambda: controller.show_frame("StartSeite")
        ).pack(pady=10)

    def update_data(self):
        """Aktualisiert die angezeigten Daten basierend auf der Auswahl."""
        partei = self.controller.ausgewaehlte_partei
        kandidat_daten = self.controller.kandidat_daten

        # Aktualisiere die Labels mit den Kandidaten-Daten
        self.label_partei.config(text=f"Wahlkampf für die Partei: {partei}")
        self.label_kandidat.config(text=f"Kandidat: {kandidat_daten.get('name', 'Unbekannt')}")
        self.label_kompetenz.config(text=f"Kompetenz: {kandidat_daten.get('kompetenz', 0)}")
        self.label_beliebtheit.config(text=f"Beliebtheit: {kandidat_daten.get('beliebtheit', 0)}")
        self.label_ambition.config(text=f"Ambition: {kandidat_daten.get('ambition', 0)}")

    def durchfuehre_aktion(self):
        messagebox.showinfo("Aktion", "Hier können Sie Aktionen durchführen!")


