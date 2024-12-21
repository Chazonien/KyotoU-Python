import tkinter as tk
from tkinter import messagebox
import random
from startseite import kandidaten  # Import candidates data
import os
from PIL import Image, ImageTk

class WahlkampfSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Hintergrundbild
        self.setze_hintergrundbild(r"bilder/bundestag_innen.jpg")

        # Poll-Daten initialisieren
        self.polls = self.init_polls()

        # Aktionen und Spezialaktionen initialisieren
        self.actions = self.init_actions()
        self.special_actions = self.init_special_actions()
        self.special_action_used = self.init_special_action_used()

        # Widgets für Kandidatendaten
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

        # Umfragen-Anzeige
        self.label_polls = tk.Label(self, text="", font=("Arial", 14), justify="left", bg="white")
        self.label_polls.pack(pady=10)

        # Aktionen-Container
        self.actions_frame = tk.Frame(self, bg="white")
        self.actions_frame.pack(pady=20)

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

    def init_polls(self):
        """Initialisiert die Poll-Daten."""
        return {
            "CDU/CSU": 31.9,
            "AfD": 18.8,
            "SPD": 16.2,
            "Grüne": 13,
            "BSW": 5.5,
            "FDP": 3.7,
            "Linke": 3
        }
    
    def init_actions(self):
        """Initialisiert die Liste der Standardaktionen."""
        return [
            "Wahlkampfveranstaltung",
            "Werbung in sozialen Medien",
            "Debatte",
            "Flyer & Werbegeschenke",
            "Spenden sammeln"
        ]

    def init_special_actions(self):
        """Initialisiert die Spezialaktionen für jede Partei."""
        return {
            "SPD": "Daran kann ich mich leider nicht erinnern!",
            "CDU/CSU": "DiE GrÜnEn?!?",
            "Grüne": "Wir brauchen eine 360 Grad Wende",
            "FDP": "Christian Lindner Schwarz-Weiß-Bild",
            "AfD": "Verfassungsschutzmitglieder treten bei",
            "Linke": "Gregor Gysi rausholen",
            "BSW": "Putin ein bisschen um Hilfe bitten"
        }

    def init_special_action_used(self):
        """Initialisiert den Status der Spezialaktionen für jede Partei."""
        return {party: False for party in self.polls}

    def update_data(self):
        """Aktualisiert Labels mit aktuellen Kandidatendaten und zeigt Polls."""
        partei = self.controller.ausgewaehlte_partei
        kandidat_daten = self.controller.kandidat_daten

        self.label_partei.config(text=f"Wahlkampf für die Partei: {partei}")
        self.label_kandidat.config(text=f"Kandidat: {kandidat_daten.get('name', 'Unbekannt')}")
        self.label_kompetenz.config(text=f"Kompetenz: {kandidat_daten.get('kompetenz', 0)}")
        self.label_beliebtheit.config(text=f"Beliebtheit: {kandidat_daten.get('beliebtheit', 0)}")
        self.label_ambition.config(text=f"Ambition: {kandidat_daten.get('ambition', 0)}")
        
        # Aktualisiere Polls
        self.update_polls()

        # Aktualisiere Buttons
        self.erzeuge_action_buttons(partei)

    def update_polls(self):
        """Aktualisiert und zeigt die Umfragewerte."""
        ergebnisse = "\n".join([f"{party}: {self.polls[party]:.1f}%" for party in self.polls])
        self.label_polls.config(text=f"Aktuelle Umfragewerte:\n{ergebnisse}")

    def erzeuge_action_buttons(self, partei):
        """Erstellt Buttons für alle verfügbaren Aktionen und die Spezialaktion."""
        # Entferne vorherige Buttons
        for widget in self.actions_frame.winfo_children():
            widget.destroy()

        # Standardaktionen hinzufügen
        for action in self.actions:
            tk.Button(
                self.actions_frame,
                text=action,
                font=("Arial", 12),
                command=lambda a=action: self.perform_action(partei, a)
            ).pack(side="top", pady=5)

        # Spezialaktion hinzufügen
        special_action = self.special_actions.get(partei)
        if special_action and not self.special_action_used[partei]:
            tk.Button(
                self.actions_frame,
                text=f"Spezialaktion: {special_action}",
                font=("Arial", 12, "bold"),
                fg="red",
                command=lambda: self.perform_action(partei, special_action)
            ).pack(side="top", pady=10)
    
    def perform_action(self, party, action):
        """Führt eine Aktion aus und aktualisiert die Umfragewerte."""
        if party not in self.polls:
            messagebox.showerror("Fehler", "Ungültige Partei!")
            return

        if action in self.actions:
            if action == "Wahlkampfveranstaltung":
                character_bonus = self.character_specific_influence(party, 0.3, 0.5, 0.2)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Werbung in sozialen Medien":
                character_bonus = self.character_specific_influence(party, 0.1, 0.3, 0.6)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Debatte":
                character_bonus = self.character_specific_influence(party, 0.5, 0.2, 0.3)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Flyer und Werbegeschenke":
                character_bonus = self.character_specific_influence(party, 0.3, 0.4, 0.3)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Spenden sammeln":
                character_bonus = self.character_specific_influence(party, 0.1, 0.6, 0.3)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            else:
                own_weight = random.uniform(-1,1) 
        elif action == self.special_actions.get(party) and not self.special_action_used[party]:
            own_weight = random.uniform(1, 2)
            self.special_action_used[party] = True
        else:
            own_weight = random.uniform(-1, 1)        

        # Simuliere Verschiebung der Wählerstimmen
        voter_shift_summary, own_change = self.simulate_voter_shift(party, own_weight)
        
        # Aktualisiere Polls
        self.polls[party] += own_change
        self.normalize_polls()

        # Aktualisiere die GUI
        self.update_polls()

        # Zeige die Änderungen direkt im Poll-Container
        self.update_poll_changes(party, action, own_change, voter_shift_summary)

    def simulate_voter_shift(self, current_party, own_weight):
        """Simulates voter shift based on the player's action."""
        total_shift = random.uniform(0.5, 5)
        party_weights = {party: random.uniform(-1, 1) for party in self.polls if party != current_party}

        positive_sum = sum(w for w in party_weights.values() if w > 0)
        negative_sum = sum(w for w in party_weights.values() if w < 0)

        if own_weight > 0:
            positive_sum += own_weight
        elif own_weight < 0:
            negative_sum += own_weight

        party_changes = {}
        for party, weight in party_weights.items():
            if weight > 0:
                party_changes[party] = (weight / positive_sum) * total_shift
            elif weight < 0:
                party_changes[party] = -(weight / negative_sum) * total_shift
            else:
                party_changes[party] = 0

        for party, change in party_changes.items():
            self.polls[party] += change

        own_change = 0
        if own_weight > 0:
            own_change = (own_weight / positive_sum) * total_shift
        elif own_weight < 0:
            own_change = (own_weight / negative_sum) * total_shift

        return party_changes, own_change

    def character_specific_influence(self, party, w1, w2, w3):
        """Calculates the specific influence of a candidate."""
        kandidat = kandidaten.get(party, {})
        return (w1 * kandidat.get("kompetenz", 0) +
                w2 * kandidat.get("beliebtheit", 0) +
                w3 * kandidat.get("ambition", 0)) / 100

    def normalize_polls(self):
        """Normalizes the poll percentages to ensure they add up to 100%."""
        total = sum(self.polls.values())
        for party in self.polls:
            self.polls[party] = round(self.polls[party] / total * 100, 1)

    def update_poll_changes(self, player_party, player_action, player_change, voter_shift_summary):
        """Aktualisiert label_polls mit den aktuellen Werten und Veränderungen."""
        # Erstelle den Text für die aktuellen Polls und die Veränderungen
        results_text = "Aktuelle Umfragewerte mit Änderungen:\n"
        for party, value in self.polls.items():
            change = voter_shift_summary.get(party, 0)  # Veränderung abrufen, 0 falls keine
            results_text += f"{party}: {value:.1f}% ({'+' if change >= 0 else ''}{change:.1f}%)\n"

        # Schreibe die aktualisierten Poll-Werte und Veränderungen in label_polls
        self.label_polls.config(text=results_text)