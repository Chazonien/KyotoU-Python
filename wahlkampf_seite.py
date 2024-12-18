import tkinter as tk
from tkinter import messagebox
import random
from startseite import kandidaten  # Import candidates data

class WahlkampfSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Widgets for candidate data
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

        # Action buttons
        tk.Button(
            self, text="Aktion durchführen", font=("Arial", 14), cursor="hand2",
            command=self.zeige_aktionen
        ).pack(pady=10)

        tk.Button(
            self, text="Zurück zum Hauptmenü", font=("Arial", 14), cursor="hand2",
            command=lambda: controller.show_frame("StartSeite")
        ).pack(pady=10)

        # Initial polls and actions
        self.polls = {
            "SPD": 20,
            "CDU/CSU": 25,
            "Grüne": 15,
            "FDP": 10,
            "AfD": 12,
            "Linke": 8,
            "BSW": 10
        }

        self.actions = [
            "Wahlkampfveranstaltung",
            "Werbung in sozialen Medien",
            "Debatte",
            "Flyer & Werbegeschenke",
            "Spenden sammeln"
        ]

        self.special_actions = {
            "SPD": "Daran kann ich mich leider nicht erinnern!",
            "CDU/CSU": "DiE GrÜnEn?!?",
            "Grüne": "Wir brauchen eine 360 Grad Wende",
            "FDP": "Christian Lindner Schwarz-Weiß-Bild",
            "AfD": "Verfassungsschutzmitglieder treten bei",
            "Linke": "Gregor Gysi rausholen",
            "BSW": "Putin ein bisschen um Hilfe bitten"
        }

        self.special_action_used = {party: False for party in self.polls}

    def update_data(self):
        """Updates labels with current candidate data."""
        partei = self.controller.ausgewaehlte_partei
        kandidat_daten = self.controller.kandidat_daten

        self.label_partei.config(text=f"Wahlkampf für die Partei: {partei}")
        self.label_kandidat.config(text=f"Kandidat: {kandidat_daten.get('name', 'Unbekannt')}")
        self.label_kompetenz.config(text=f"Kompetenz: {kandidat_daten.get('kompetenz', 0)}")
        self.label_beliebtheit.config(text=f"Beliebtheit: {kandidat_daten.get('beliebtheit', 0)}")
        self.label_ambition.config(text=f"Ambition: {kandidat_daten.get('ambition', 0)}")

    def normalize_polls(self):
        """Normalizes the poll percentages to ensure they add up to 100%."""
        total = sum(self.polls.values())
        for party in self.polls:
            self.polls[party] = round(self.polls[party] / total * 100, 1)

    def update_polls(self):
        ergebnisse = "\n".join([f"{party}: {self.polls[party]:.1f}%" for party in self.polls])
        self.label_polls.config(text=f"Aktuelle Umfragewerte:\n{ergebnisse}")

    def character_specific_influence(self, party, w1, w2, w3):
        """Calculates the specific influence of a candidate."""
        kandidat = kandidaten.get(party, {})
        return (w1 * kandidat.get("kompetenz", 0) +
                w2 * kandidat.get("beliebtheit", 0) +
                w3 * kandidat.get("ambition", 0)) / 100
    
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

    def perform_action(self, party, action):
        """Performs an action and updates polls."""
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

        voter_shift_summary, own_change = self.simulate_voter_shift(party, own_weight)
        self.polls[party] += own_change
        self.normalize_polls()
        self.show_results_popup(party, action, own_change, voter_shift_summary)
        self.update_polls()

    def show_results_popup(self, player_party, player_action, player_change, voter_shift_summary):
        """Displays a popup showing the results of the round."""
        results_window = tk.Toplevel(self)
        results_window.title("Rundenergebnisse")
        results_text = f"Ihre Aktion für {player_party}: {player_action}\nÄnderung: {player_change:+.1f}%\n\n"
        results_text += "Andere Parteien:\n"
        for party, change in voter_shift_summary.items():
            results_text += f"{party}: Änderung: {change:+.1f}%\n"

        tk.Label(results_window, text="Rundenergebnisse", font=("Arial", 14, "bold")).pack(pady=10)
        text_box = tk.Text(results_window, font=("Arial", 12), wrap="word")
        text_box.insert("1.0", results_text)
        text_box.config(state="disabled")
        text_box.pack(padx=10, pady=10, fill="both", expand=True)
        tk.Button(results_window, text="Schließen", command=results_window.destroy).pack(pady=10)

    def zeige_aktionen(self):
        """Displays the available actions for the selected party."""
        selected_party = self.controller.ausgewaehlte_partei

        aktionen_fenster = tk.Toplevel(self)
        aktionen_fenster.title(f"Aktionen für {selected_party}")
        aktionen_fenster.geometry("600x400")  # Adjusted for better usability

        tk.Label(aktionen_fenster, text=f"Wählen Sie eine Aktion für {selected_party}:", font=("Arial", 14)).pack(pady=10)

        # Display standard actions
        for action in self.actions:
            tk.Button(
                aktionen_fenster,
                text=action,
                command=lambda a=action: [self.perform_action(selected_party, a), aktionen_fenster.destroy()]
            ).pack(pady=5)

        # Display special action if available
        if not self.special_action_used[selected_party]:
            special_action = self.special_actions.get(selected_party, None)
            if special_action:
                tk.Button(
                    aktionen_fenster,
                    text=f"Spezialaktion: {special_action}",
                    command=lambda: [self.perform_action(selected_party, special_action), aktionen_fenster.destroy()]
                ).pack(pady=10)