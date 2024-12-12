import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import sys
import random
import subprocess
from main_gui import kandidaten

# Argument: Ausgewählte party
if len(sys.argv) < 2:
    sys.exit("Fehler: Keine party ausgewählt.")
selected_party = sys.argv[1]

# Initiale Umfragewerte der partyen (sollten immer 100% ergeben)
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
    "Wahlkampfveranstaltung",
    "Werbung in sozialen Medien",
    "Debatte",
    "Flyer & Werbegeschenke",
    "Spenden sammeln"
]

# Spezielle Aktionen pro party
special_actions = {
    "SPD": "Wahlkampf: Daran kann ich mich leider nicht erinnern!",
    "SPD": "Finanzierung: Spende von der Warburg-Bank P.S. Danke Olaf",
    "CDU/CSU": "Wahlkampf: DiE GrÜnEn?!?",
    "CDU/CSU": "Finanzierung: Haben wir noch Reserven vom Maskendeal?",
    "Grüne": "Wir brauchen eine 360 Grad Wende",
    "Grüne": "Verkauf hauseigener Homöpathiker",
    "FDP": "Christian Linder Schwarz-Weiß Bild",
    "FDP": "Beim Porsche-Vorstand anrufen",
    "AfD": "Verfassungschutzmitglieder treten der party bei",
    "AfD": "Anspruch auf Gold aus schweizer Banken erheben",
    "Linke": "Gregor Gysi rausholen",
    "Linke": "Geld erben, weil Toter die Nachfahren verarschen will",
    "BSW": "Putin ein bisschen um Hilfe bitten",
    "BSW": "Porsche Klaus macht Kontakte klar"
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

def character_specific_influence(party, w1, w2, w3):
    return (w1 * kandidaten[party]["kompetenz"] + w2 * kandidaten[party]["beliebtheit"] + w3 * kandidaten[party]["ambition"])/100

# Aktion ausführen
def perform_action(party, action):
    # Simulate the player's action
    if action in actions:
        if action == "Wahlkampfveranstaltung":
            character_bonus = character_specific_influence(party, 0.3, 0.5, 0.2)
            own_weight = random.uniform(-1 + character_bonus, character_bonus)
        elif action == "Werbung in sozialen Medien":
            character_bonus = character_specific_influence(party, 0.1, 0.3, 0.6)
            own_weight = random.uniform(-1 + character_bonus, character_bonus)
        elif action == "Debatte":
            character_bonus = character_specific_influence(party, 0.5, 0.2, 0.3)
            own_weight = random.uniform(-1 + character_bonus, character_bonus)
        elif action == "Flyer und Werbegeschenke":
            character_bonus = character_specific_influence(party, 0.3, 0.4, 0.3)
            own_weight = random.uniform(-1 + character_bonus, character_bonus)
        elif action == "Spenden sammeln":
            character_bonus = character_specific_influence(party, 0.1, 0.6, 0.3)
            own_weight = random.uniform(-1 + character_bonus, character_bonus)
        else:
            own_weight = random.uniform(-1,1) 
    elif action == special_actions[party] and not special_action_used[party]:
        own_weight = random.uniform(1, 2)  # Spezielle Aktion
        special_action_used[party] = True  # Spezialaktion wurde genutzt

    # Simulate the voter shift for other parties
    voter_shift_summary, own_change = simulate_voter_shift(party, own_weight)
    polls[party] += own_change
    
    # Normalize after player's action
    normalize_polls()
    # Show the results popup
    show_results_popup(party, action, own_change, voter_shift_summary)
    update_polls()

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
    results_text += "Andere partyen:\n"
    
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
def update_polls():
    ergebnisse = "\n".join([f"{party}: {polls[party]:.1f}%" for party in polls])
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
update_polls()

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

bg_path = r"bilder\bundestag.jpg"  # Replace with your image file
image = Image.open(bg_path)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
image = image.resize((screen_width, screen_height))
bg_image = ImageTk.PhotoImage(image)

# Create a Label to display the background image
bg_label = tk.Label(root, image=bg_image)
bg_label.lower()
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Aktionen-Button
tk.Button(root, text="Aktionen durchführen", font=("Arial", 14), command=zeige_aktionen).pack(pady=10)

# Beenden-Button
tk.Button(root, text="Beenden", font=("Arial", 14), command=root.destroy).pack(pady=10)

# Hauptschleife starten
root.mainloop()