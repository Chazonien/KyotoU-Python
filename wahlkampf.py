import tkinter as tk
from tkinter import messagebox
import sys
import random
import subprocess
from main_gui import kandidaten

# Argument: Ausgewählte Partei
if len(sys.argv) < 2:
    sys.exit("Fehler: Keine Partei ausgewählt.")
selected_party = sys.argv[1]

# Initiale Umfragewerte der Parteien (sollten immer 100% ergeben)
polls = {
    "SPD": 20,
    "CDU/CSU": 25,
    "Grüne": 15,
    "FDP": 10,
    "AfD": 12,
    "Linke": 8,
    "BSW": 10
}

# Politische Aktionen
actions = [
    "Wahlkampfveranstaltung organisieren",
    "Werbung in sozialen Medien schalten",
    "Debatte vorbereiten",
    "Flyer verteilen",
    "Spenden sammeln"
]

# Spezielle Aktionen pro Partei
special_actions = {
    "SPD": "Daran kann ich mich leider nicht erinnern!",
    "CDU/CSU": "DiE GrÜnEn?!?",
    "Grüne": "Wir brauchen eine 360 Grad Wende",
    "FDP": "Christian Linder Schwarz-Weiß Bild",
    "AfD": "Verfassungschutzmitglieder treten der Partei bei",
    "Linke": "Gregor Gysi rausholen",
    "BSW": "Bitte Putin um ein bisschen Hilfe im Wahlkampf"
}

special_action_used = {party: False for party in polls}  # Verfolgung der Spezialaktionen

# Prozentwerte normalisieren, damit sie 100% ergeben
def normalize_polls():
    # Round each poll value to 1 decimal place before normalization
    for party in polls:
        polls[party] = round(polls[party], 1)
    
    total = sum(polls.values())
    
    # Normalize the values and round them again to 1 decimal place
    for party in polls:
        polls[party] = round(polls[party] / total * 100, 1)

# Aktion ausführen
def perform_action(partei, action):
    # Simulate the player's action
    change = 0
    if action in actions:
        if action == "Wahlkampfveranstaltung organisieren":
            own_weight = random.uniform(-1 + (0.2 * kandidaten[partei]["kompetenz"] + 0.7 * kandidaten[partei]["beliebtheit"] +0.1 * kandidaten[partei]["ambition"])/100, (0.2 * kandidaten[partei]["kompetenz"] + 0.7 * kandidaten[partei]["beliebtheit"] +0.1 * kandidaten[partei]["ambition"])/100)
            print(0.2 * kandidaten[partei]["kompetenz"])
            print(0.7 * kandidaten[partei]["beliebtheit"])
            print(0.1 * kandidaten[partei]["ambition"])
        else:
            own_weight = random.uniform(-1,1) 
    elif action == special_actions[partei] and not special_action_used[partei]:
        own_weight = random.uniform(0, 2)  # Spezielle Aktion
        special_action_used[partei] = True  # Spezialaktion wurde genutzt

    # Simulate the voter shift for other parties
    voter_shift_summary, own_change = simulate_voter_shift(partei, own_weight)
    polls[partei] += own_change
    
    # Normalize after player's action
    normalize_polls()
    # Show the results popup
    show_results_popup(partei, action, own_change, voter_shift_summary)
    aktualisiere_umfragen()

# Simulation der Wählerbewegung
def simulate_voter_shift(current_party, own_weight):
    total_shift = random.uniform(0.5, 5)  # Gesamtänderung (z.B. 5%)
    party_weights = {party: random.uniform(-1, 1) for party in polls if party != current_party}
    # Separate positive and negative weights
    positive_sum = sum(w for w in party_weights.values() if w > 0)
    negative_sum = sum(w for w in party_weights.values() if w < 0)

    if own_weight > 0:
        positive_sum += own_weight
    elif own_weight < 0:
        negative_sum += own_weight

    # Adjust percentages proportionally based on weights
    party_changes = {}
    for party, weight in party_weights.items():
        if weight > 0:  # Gain
            party_changes[party] = (weight / positive_sum) * total_shift
        elif weight < 0:  # Loss
            party_changes[party] = -(weight / negative_sum) * total_shift
        else:
            party_changes[party] = 0

    # Apply changes to polls
    for party, change in party_changes.items():
        polls[party] += change
    
    if own_weight > 0:
        own_change = (own_weight / positive_sum) * total_shift
    elif own_weight < 0:
        own_change = (own_weight / negative_sum) * total_shift
    
    return party_changes, own_change

# Ergebnisse anzeigen
def show_results_popup(player_party, player_action, player_change, voter_shift_summary):
    results_window = tk.Toplevel(root)
    results_window.title("Rundenergebnisse")
    results_window.attributes("-fullscreen", True)  # Vollbildmodus
    
    results_text = f"Ihre Aktion für {player_party}: {player_action}\nÄnderung: {player_change:+.1f}%\n\n"
    results_text += "Andere Parteien:\n"
    
    # Generate actions for the other parties
    for party, change in voter_shift_summary.items():
        action = random.choice(actions + [special_actions[party]])
        results_text += f"{party}: Aktion: {action}, Änderung: {change:+.1f}%\n"
    
    tk.Label(results_window, text="Rundenergebnisse", font=("Arial", 14, "bold")).pack(pady=10)
    text_box = tk.Text(results_window, font=("Arial", 12), wrap="word")
    text_box.insert("1.0", results_text)
    text_box.config(state="disabled")  # Nur Anzeige, keine Bearbeitung
    text_box.pack(padx=10, pady=10, fill="both", expand=True)
    tk.Button(results_window, text="Schließen", command=results_window.destroy).pack(pady=10)

# Umfragen aktualisieren
def aktualisiere_umfragen():
    ergebnisse = "\n".join([f"{partei}: {polls[partei]:.1f}%" for partei in polls])
    umfrage_label.config(text=f"Aktuelle Umfragewerte:\n{ergebnisse}")

# Hauptfenster erstellen
root = tk.Tk()
root.title(f"Wahlkampf Simulation - {selected_party}")
root.attributes("-fullscreen", True)  # Set the main window to fullscreen

# Überschrift
header = tk.Label(root, text=f"Wahlkampf für {selected_party}", font=("Arial", 16, "bold"))
header.pack(pady=10)

# Umfragen-Anzeige
umfrage_label = tk.Label(root, text="", font=("Arial", 14), justify="left")
umfrage_label.pack(pady=10)
aktualisiere_umfragen()

# Aktionen-Menü
def zeige_aktionen():
    aktionen_fenster = tk.Toplevel(root)
    aktionen_fenster.title(f"Aktionen für {selected_party}")
    aktionen_fenster.attributes("-fullscreen", True)  # Fullscreen for actions window
    tk.Label(aktionen_fenster, text=f"Wählen Sie eine Aktion für {selected_party}:", font=("Arial", 14)).pack(pady=10)

    # Normale Aktionen
    for action in actions:
        tk.Button(
            aktionen_fenster, 
            text=action, 
            command=lambda a=action: [perform_action(selected_party, a), aktionen_fenster.destroy()]
        ).pack(pady=5)

    # Spezielle Aktion
    if not special_action_used[selected_party]:
        tk.Button(
            aktionen_fenster, 
            text=special_actions[selected_party], 
            command=lambda: [perform_action(selected_party, special_actions[selected_party]), aktionen_fenster.destroy()]
        ).pack(pady=10)

# Aktionen-Button
tk.Button(root, text="Aktionen durchführen", font=("Arial", 14), command=zeige_aktionen).pack(pady=10)

# Beenden-Button
tk.Button(root, text="Beenden", font=("Arial", 14), command=root.destroy).pack(pady=10)

# Hauptschleife starten
root.mainloop()