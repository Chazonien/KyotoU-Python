import tkinter as tk
from tkinter import messagebox
import random
import itertools
from startseite import kandidaten  # Import candidates data
import os
from PIL import Image, ImageTk

class WahlkampfSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Hintergrundbild
        self.setze_hintergrundbild(r"bilder/bundestag_innen.jpg")

        # Rundenzähler
        self.turns = 0
        self.max_turns = 15

        # Counter oben rechts
        self.weeks_label = tk.Label(
            self,
            text=f"{self.max_turns - self.turns} Wochen bis zur Wahl",
            font=("Arial", 14, "bold"),
            bg="white",
            anchor="e"
        )
        self.weeks_label.place(relx=0.98, rely=0.98, anchor="se") # Position unten rechts

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
        self.label_polls = tk.Text(self, font=("Arial", 14), bg="white", wrap="word", state="disabled", height=11, width=40)
        self.label_polls.pack(pady=10, padx=10, anchor="n")

        # Aktionen-Container
        self.actions_frame = tk.Frame(self, bg="white", height=11, width=40)
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
            "Linke": 3,
            "Sonstige": 7.9
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
        # Aktivieren des Textwidgets für Änderungen
        self.label_polls.config(state="normal")
        self.label_polls.delete("1.0", tk.END)  # Lösche alten Text

        # Tag für zentrierten Text definieren
        self.label_polls.tag_configure("center", justify="center")

        # Schreibe die aktuellen Umfragewerte
        ergebnisse = "Aktuelle Umfragewerte:\n"
        for party, value in self.polls.items():
            ergebnisse += f"{party}: {value:.1f}%\n"
    
        self.label_polls.insert(tk.END, ergebnisse, "center")

        # Deaktiviere das Textwidget
        self.label_polls.config(state="disabled")

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
                cursor="hand2",
                command=lambda a=action: self.perform_action(partei, a)
            ).pack(side="top", pady=5)

        # Spezialaktion hinzufügen
        special_action = self.special_actions.get(partei)
        if special_action and not self.special_action_used[partei]:
            tk.Button(
                self.actions_frame,
                text=f"Spezialaktion: {special_action}",
                font=("Arial", 12, "bold"),
                cursor="hand2",
                fg="red",
                command=lambda: self.perform_action(partei, special_action)
            ).pack(side="top", pady=10)
    
    def perform_action(self, party, action):
        """Führt eine Aktion aus und aktualisiert die Umfragewerte."""
        # Speichert die Umfrageergebnisse bevor eine Aktion durchgeführt wird
        polls_before = self.polls.copy()
        if party not in self.polls:
            messagebox.showerror("Fehler", "Ungültige Partei!")
            return

        if action in self.actions:
            if action == "Wahlkampfveranstaltung":
                character_bonus = self.character_specific_influence(party, 0.3, 0.4, 0.3)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Werbung in sozialen Medien":
                character_bonus = self.character_specific_influence(party, 0.1, 0.2, 0.7)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Debatte":
                character_bonus = self.character_specific_influence(party, 0.7, 0.1, 0.2)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Flyer und Werbegeschenke":
                character_bonus = self.character_specific_influence(party, 0.4, 0.2, 0.4)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            elif action == "Spenden sammeln":
                character_bonus = self.character_specific_influence(party, 0.1, 0.7, 0.2)
                own_weight = random.uniform(-1 + character_bonus, character_bonus)
            else:
                own_weight = random.uniform(-1,1) 
        elif action == self.special_actions.get(party) and not self.special_action_used[party]:
            own_weight = random.uniform(1, 2)
            self.special_action_used[party] = True
        else:
            own_weight = random.uniform(-1, 1)        

        # Simuliere Verschiebung der Wählerstimmen
        own_change = self.simulate_voter_shift(party, own_weight)
        # Aktualisiere Polls
        self.polls[party] += own_change
        self.normalize_polls()
        
        # Event auslösen
        if random.uniform(0, 1) < 0.4 and self.turns != 10:
            # Wechsle zur ZufallsEventSeite und zeige das Event an
            self.controller.show_frame("ZufallsEventSeite")
            event_seite = self.controller.frames["ZufallsEventSeite"]
            event_seite.zeige_event()

        if self.turns == 10:
            self.controller.show_frame("TVDebatteSeite")
            debatte_seite = self.controller.frames["TVDebatteSeite"]
            debatte_seite.zeige_debatte()
        
        # Rundenzähler aktualisieren
        self.turns += 1
        self.weeks_label.config(text=f"{self.max_turns - self.turns} Wochen bis zur Wahl")

        # Prüfe, ob die maximale Rundenzahl erreicht ist
        if self.turns >= self.max_turns:
            self.controller.show_frame("SpielendeSeite")
            spielende_seite = self.controller.frames["SpielendeSeite"]
            spielende_seite.zeige_endscreen(self.polls)
            return

        # Speichert die Umfrageergebnisse nach den durchgeführten Aktionen
        self.normalize_polls()
        polls_after = self.polls.copy()

        # Berechnet die Diifferenz der Umfrageergebnisse
        poll_change_own = polls_after[party] - polls_before[party]
        poll_change_others = {
                party_change: polls_after[party_change] - polls_before[party_change]
                for party_change in self.polls if party_change != party
            }
        
        # Aktualisiere die Daten in der GUI
        self.update_data()

        # Aktualisiere die GUI
        self.update_polls()

        # Zeige die Änderungen direkt im Poll-Container
        self.update_poll_changes(party, action, poll_change_own, poll_change_others)

    def simulate_voter_shift(self, current_party, own_weight):
        """Simulates voter shift based on the player's action."""
        total_shift = random.uniform(1, 5)
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

        return own_change

    def character_specific_influence(self, party, w1, w2, w3):
        """Berechnungen des spezifischen Einflusses eines Kandidaten."""
        kandidat = kandidaten.get(party, {})
        return (w1 * kandidat.get("kompetenz", 0) +
                w2 * kandidat.get("beliebtheit", 0) +
                w3 * kandidat.get("ambition", 0)) / 100

    def normalize_polls(self):
        """Normalisiert die Poll-Werte und stellt sicher, dass keine negativen Werte vorhanden sind."""
        # Setze negative Werte auf 0
        for party in self.polls:
            if self.polls[party] < 0:
                self.polls[party] = 0

        # Normalisiere die Werte, sodass sie insgesamt 100% ergeben
        total = sum(self.polls.values())
        for party in self.polls:
            self.polls[party] = round(self.polls[party] / total * 100, 1)

    def update_poll_changes(self, player_party, player_action, own_change, voter_shift_summary):
        """Aktualisiert label_polls mit den aktuellen Werten und Veränderungen."""
        # Aktivieren des Textwidgets für Änderungen
        self.label_polls.config(state="normal")
        self.label_polls.delete("1.0", tk.END)  # Lösche alten Text

        # Tags definieren
        self.label_polls.tag_configure("center", justify="center")
        self.label_polls.tag_configure("bold", font=("Arial", 14, "bold"))
        self.label_polls.tag_configure("gain", foreground="green")
        self.label_polls.tag_configure("loss", foreground="red")

        # Header hinzufügen
        header = f"Ihre Aktion: {player_action}\n\nAktuelle Umfragewerte mit Änderungen:\n"
        self.label_polls.insert(tk.END, header, "center")

        # Umfragewerte und Änderungen hinzufügen
        for party, value in self.polls.items():
            if party == player_party:
                # Eigene Partei fett markieren
                change = own_change
                entry = f"{party}: {value:.1f}% ({'+' if change >= 0 else ''}{change:.1f}%)\n"
                self.label_polls.insert(tk.END, entry, ("bold", "center", "gain" if change >= 0 else "loss"))
            else:
                # Andere Parteien mit Farbänderung
                change = voter_shift_summary.get(party, 0)
                entry = f"{party}: {value:.1f}% ({'+' if change >= 0 else ''}{change:.1f}%)\n"
                self.label_polls.insert(tk.END, entry, ("center", "gain" if change >= 0 else "loss"))

        # Deaktiviere das Textwidget
        self.label_polls.config(state="disabled")
    
    def get_own_party(self):
        return self.controller.ausgewaehlte_partei
    
    def get_current_polls(self):
        return self.polls

class ZufallsEventSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Initialisiere Events
        self.events = self.init_events()

        # Event-Widgets
        self.label_event_title = tk.Label(self, text="", font=("Arial", 18, "bold"), bg="white")
        self.label_event_title.pack(pady=10)

        self.label_event_description = tk.Label(self, text="", font=("Arial", 14), bg="white", wraplength=600, justify="center")
        self.label_event_description.pack(pady=10)

        self.event_image_label = tk.Label(self, bg="white")
        self.event_image_label.pack(pady=10)

        # Auswahlmöglichkeiten
        self.options_frame = tk.Frame(self, bg="white")
        self.options_frame.pack(pady=20)

    def init_events(self):
        """Initialisiert die Liste der zufälligen Events."""
        return [
            {
                "title": "Umweltdebatte entbrannt!",
                "description": "Umweltbewegungen wie Fridays For Future verstärken aufeinmal die Proteste kurz vor der Wahl. Wie reagieren Sie?",
                "image": r"bilder/umwelt-debatte.png",
                "options": [
                    {"text": "Konstruktive Auseinandersetzung mit den Demonstranten", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Die scheiß Drecksgören sollen zurück in die Schule", "weight": random.uniform(-1, 0)},
                    {"text": "Sie äußern sich überhaupt gar nicht", "weight": random.uniform(-0.5, 0.5)},
                ]
            },
            {
                "title": "Maut-Debakel 2.0!",
                "description": "Nach einem vorgeschlagenen Plan zur Einführung einer Fahrrad-Maut, hagelt es Proteste von Radfahrverbänden. Wie gehen Sie mit der Situation um?",
                "image": r"bilder/maut-debakel.png",
                "options": [
                    {"text": "Den Plan sofort zurückziehen und PR Bilder mit einem Fahrrad (wie fährt man das eigentlich ohne Fahrer?)", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Beharren Sie auf die Maut: 'Radwege sind Luxus! Autos haben ein Recht zum Rasen!'", "weight": random.uniform(-1.5, -0.5)},
                    {"text": "Die Schuld für die Veröffentlichung des Plans dem Generalsekretär geben.", "weight": random.uniform(-0.5, 0.5)}
                ]
            },
            {
                "title": "Flutkatastrophe im nächsten Tal!",
                "description": "Es regnet mal wieder wie in Großbritannien und halb Thüringen ist abgesoffen. Bei einer Veranstaltung, bei der es um strukturelle Hilfe geht, lachst du ausversehen laut. was machst du?",
                "image": r"bilder/laschet-lacht.png",
                "options": [
                    {"text": "Direkt nach Veröffentlichung der Bilder entschuldigen (sowie jeder folgender Wahlkampfeveranstaltung)", "weight": random.uniform(-1.5, 0)},
                    {"text": "Du gehst vor die Presse und erzählst den Witz", "weight": random.uniform(-2, -1)},
                    {"text": "Ignorierst die Bilder und machst einfach weiter Wahlkampf", "weight": random.uniform(-0.5, 0)}
                ]
            },
            {
                "title": "Elon Musk wird Kolumnist der WELT!",
                "description": "Elon Musk schreibt eine Kolumne mit dem Titel 'Deutschland braucht mehr Hustle'. Sie wird sofort kontrovers diskutiert. Wie reagieren Sie?",
                "image": r"bilder/musk-kolumne.png",
                "options": [
                    {"text": "Loben Sie die Kolumne als 'frischen Wind' für die deutsche Medienlandschaft", "weight": random.uniform(-0.5, 0.5)},
                    {"text": "Verurteilen Sie die Kolumne als 'kapitalistischen Unsinn'", "weight": random.uniform(-1, 1)},
                    {"text": "Erklären Sie, dass Elon Musk deutsche Politik nicht versteht", "weight": random.uniform(0, 0.5)}
                ]
            },
            {
                "title": "BER plant den 'Terminal für die Zukunft'!",
                "description": "Ein neuer Terminal am BER wird angekündigt: Diesmal speziell für Hyperloop-Passagiere. Die Kosten sind unklar. Wie reagieren Sie?",
                "image": r"bilder/ber-terminal.png",
                "options": [
                    {"text": "Feiern Sie das Projekt als Innovation 'Made in Germany'", "weight": random.uniform(-0.25, 0.25)},
                    {"text": "Kritisieren Sie den Plan und fordern stattdessen funktionierende Rolltreppen", "weight": random.uniform(1, 1.5)},
                    {"text": "Fordern Sie erstmal eine Bürgerbefragung über den Terminal, und reichen die erste Baubeschwerde ein", "weight": random.uniform(-1, 0)}
                ]
            },
            {
                "title": "Musk gegen Gewerkschaften!",
                "description": "Elon Musk fordert ein Verbot von Gewerkschaften in Deutschland, da sie 'Innovation behindern'. Was sagen Sie dazu?",
                "image": r"bilder/musk-gewerkschaften.png",
                "options": [
                    {"text": "Verteidigen Sie Gewerkschaften als 'Grundpfeiler der Demokratie'", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Unterstützen Sie Musk und erklären, dass Gewerkschaften 'veraltet' sind", "weight": random.uniform(-1.5, -0.5)},
                    {"text": "Weichen Sie aus: 'Das Thema verdient weitere Diskussion'", "weight": random.uniform(-0.5, 0.5)}
                ]
            },
            {
                "title": "Trump twittert: 'Germany owes me Bratwurst!'",
                "description": "Donald Trump behauptet auf Twitter, Deutschland habe ihm 'eine Bratwurst und mehr Respekt' versprochen. Was tun Sie?",
                "image": r"bilder/trump-twitter.png",
                "options": [
                    {"text": "Sie vermitteln einen Würstchenstandbesuch mit Markus Söder", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Ignorieren Sie den Tweet und hoffen, dass es niemand ernst nimmt", "weight": random.uniform(-0.5, 0.5)},
                    {"text": "Geben Sie Trump die Bratwurst und laden ihn nach Thüringen ein. Dank des bestehenden Funklochs, erlösen Sie die Welt für ein paar Stunden von seinem getwitter", "weight": random.uniform(1.5, 2)}
                ]
            },
            {
                "title": "EU führt Kartoffel-Norm 3000 ein!",
                "description": "Die EU beschließt eine neue Richtlinie: Kartoffeln dürfen maximal 8 cm lang und 4 cm dick sein. Bauern protestieren. Was tun Sie?",
                "image": r"bilder/eu-kartoffeln.png",
                "options": [
                    {"text": "Unterstützen Sie die Bauern: 'Wir lassen uns die Folienkartoffel nicht verbieten!'", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Verteidigen Sie die EU und erklären die Regelung als 'wissenschaftlich fundiert'", "weight": random.uniform(-1.5, -0.5)},
                    {"text": "Versprechen Sie Kartoffellieferungen an die Ukraine für Munition von Kartoffelkanonen", "weight": random.uniform(-0.5, 0.5)}
                ]
            },
            {
                "title": "Bürgermeister outet sich öffentlich!",
                "description": "Ein Bürgermeister einer Großstadt macht öffentlich, dass er homosexuell ist. Die Nachricht sorgt für unterschiedliche Reaktionen in der Gesellschaft. Wie positionieren Sie sich?",
                "image": r"bilder/wowereit.png",
                "options": [
                    {"text": "Feiern Sie den Mut und sprechen Sie sich für mehr Offenheit und Toleranz aus.", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Reagieren Sie neutral und betonen, dass die sexuelle Orientierung Privatsache ist.", "weight": random.uniform(-0.5, 0.5)},
                    {"text": "Solange der Bürgermeister sich mir nicht nähert ist alles gut und Sie appellieren an traditionelle Werte.", "weight": random.uniform(-1.5, -0.5)}
                ]
            },
            {
                "title": "Neuer Wahlkampfslogan in Bayern enthüllt: 'Bayern First!'",
                "description": "Eine Partei schlägt vor, dass Bayern eine Sonderstellung in der Bundespolitik erhalten soll. Andere Bundesländer reagieren irritiert. Was tun Sie?",
                "image": r"bilder/bayernfirst.png",
                "options": [
                    {"text": "Unterstützen Sie den Vorschlag und schlagen einen Bier-Soli vor", "weight": random.uniform(-0.5, 0.5)},
                    {"text": "Fordern Sie, dass alle Bundesländer gleich behandelt werden", "weight": random.uniform(1, 1.5)},
                    {"text": "Schlagen Sie vor, dass Bayern sich von Deutschland trennt, wenn sie das ernst meinen", "weight": random.uniform(0.5, 1.5)}
                ]
            },
            {
                "title": "Jugendwort des Jahres!'",
                "description": "Susanne Daubner haut wieder das Jugendwort des Jahres raus. Bei einer Wahlkampfveranstaltung wollen Sie mit der Jugend anknüpfen. Was sagen Sie?",
                "image": r"bilder/jugendwort.png",
                "options": [
                    {"text": "Ich bin ein richtiges Sigma! Wer micht wählt +5000 Aura", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Cringe wer nicht wählen geht! Richtige Lowperformer!", "weight": random.uniform(0, 1)},
                    {"text": "Die Talahons am Berliner Bahnhof, ey, verticken echt das beste Gras", "weight": random.uniform(0, 1)}
                ]
            },
            {
                "title": "Bierzelt Wahlkampf!",
                "description": "Wie jeder gute Deutsche, trifft man seine Wahlentscheidung im Bierzelt! Beim dritten Bier kommt es dazu: Gras!",
                "image": r"bilder/cannabis.png",
                "options": [
                    {"text": "Karl Lauterbach auf die Bühne holen und einen Bubatz durchziehen", "weight": random.uniform(0.5, 1.5)},
                    {"text": "Kiffer raus aus Bayern", "weight": random.uniform(-1, 0)},
                    {"text": "Ich bin gegen alle Drogen! Bier ist das einzig Wahre von Gott gegeben!", "weight": random.uniform(0, 1)}
                ]
            }
            # Weitere Events können hier hinzugefügt werden
        ]

    def zeige_event(self):
        """Zeigt ein zufälliges Event an."""
        event = random.choice(self.events)
        self.events.remove(event)

        # Setze Titel und Beschreibung
        self.label_event_title.config(text=event["title"])
        self.label_event_description.config(text=event["description"])

        # Lade und zeige das Bild
        image_path = event["image"]
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((600, 400), Image.Resampling.LANCZOS)
            self.event_image = ImageTk.PhotoImage(image)
            self.event_image_label.config(image=self.event_image)
        else:
            print(f"Fehler: Bildpfad nicht gefunden: {image_path}")

        # Erstelle Auswahlmöglichkeiten
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for option in event["options"]:
            tk.Button(
                self.options_frame,
                text=option["text"],
                font=("Arial", 12),
                cursor="hand2",
                command=lambda o=option: self.handle_event_choice(o)
            ).pack(pady=5)

    def handle_event_choice(self, option):
        """Behandelt die Wahl eines Event-Options und aktualisiert die Wählerumfragen."""
        # Gewicht aus der gewählten Option extrahieren
        action_weight = option["weight"]
        
        wahlkampf_seite = self.controller.frames["WahlkampfSeite"]
        current_party = wahlkampf_seite.get_own_party()

        # Poll-Daten vor dem Event speichern
        previous_polls = wahlkampf_seite.get_current_polls().copy()

        # Simuliere die Wählerwanderung basierend auf dem Gewicht
        own_change = self.simulate_voter_shift_event(action_weight, current_party)
        # Aktualisiere die Polls in der Wahlkampf-Seite
        wahlkampf_seite.polls[current_party] += own_change
        self.normalize_polls()
        # Wechsel zurück zur Wahlkampf-Seite
        self.controller.show_frame("WahlkampfSeite")

        # Zeige die Änderungen an
        wahlkampf_seite.update_poll_changes(
            current_party,
            "Zufalls-Event",
            own_change,
            {party: wahlkampf_seite.polls[party] - previous_polls[party] for party in wahlkampf_seite.polls if party != current_party}
        )

    def simulate_voter_shift_event(self, action_weight, current_party):
        """Simuliert die Veränderung der Wählerstimmen basierend auf dem Gewicht der Aktion."""
        total_shift = random.uniform(0.5, 5)
        party_weights = {party: random.uniform(-1, 1) for party in self.controller.frames["WahlkampfSeite"].polls if party != current_party}

        positive_sum = sum(w for w in party_weights.values() if w > 0) + max(0, action_weight)
        negative_sum = sum(w for w in party_weights.values() if w < 0) + min(0, action_weight)

        party_changes = {}
        for party, weight in party_weights.items():
            if weight > 0:
                party_changes[party] = (weight / positive_sum) * total_shift
            elif weight < 0:
                party_changes[party] = -(weight / negative_sum) * total_shift
            else:
                party_changes[party] = 0

        wahlkampf_seite = self.controller.frames["WahlkampfSeite"]
        for party, change in party_changes.items():
            wahlkampf_seite.polls[party] += change

        own_change = (action_weight / positive_sum) * total_shift if action_weight > 0 else 0

        return own_change

    def normalize_polls(self):
        """Normalisiert die Poll-Werte."""
        # Setze negative Werte auf 0
        wahlkampf_seite = self.controller.frames["WahlkampfSeite"]
        for party in wahlkampf_seite.polls:
            if wahlkampf_seite.polls[party] < 0:
                wahlkampf_seite.polls[party] = 0

        # Normalisiere die Werte, sodass sie insgesamt 100% ergeben       
        total = sum(wahlkampf_seite.polls.values())
        for party in wahlkampf_seite.polls:
            wahlkampf_seite.polls[party] = round(wahlkampf_seite.polls[party] / total * 100, 1)

class TVDebatteSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        # Punktlimit und Strategien
        self.max_points = 30
        self.remaining_points = tk.IntVar(value=self.max_points)
        self.strategy_sliders = {}

        # Initialisiere Events
        self.events = self.init_events()

        # Event-Widgets
        self.label_event_title = tk.Label(self, text="", font=("Arial", 18, "bold"), bg="white")
        self.label_event_title.pack(pady=10)

        self.label_event_description = tk.Label(self, text="", font=("Arial", 14), bg="white", wraplength=600, justify="center")
        self.label_event_description.pack(pady=10)

        self.event_image_label = tk.Label(self, bg="white")
        self.event_image_label.pack(pady=10)

        # Auswahlmöglichkeiten mit Schiebereglern
        self.options_frame = tk.Frame(self, bg="white")
        self.options_frame.pack(pady=20)

        # Anzeige für verbleibende Punkte
        self.remaining_label = tk.Label(self, text=f"Verbleibende Punkte: {self.remaining_points.get()}", font=("Arial", 12), bg="white")
        self.remaining_label.pack(pady=5)

        # Bestätigungs-Button
        self.confirm_button = tk.Button(self, text="Bestätigen", font=("Arial", 12), cursor="hand2", state="disabled", command=self.confirm_selection)
        self.confirm_button.pack(pady=10)

    def init_events(self):
        """Initialisiert die Liste der zufälligen Events."""
        return [
            {
                "title": "TV-Debatte zur Primetime!",
                "description": "Der Höhepunkt des Wahlkampfs: Die TV Debatte im Ersten findet statt und alle Spitzenkandidaten der großen Parteien sind anwesend. Was ist Ihre Strategie um siegreich die Debatte zu verlassen?",
                "image": r"bilder/tv-debatte.jpg",
                "options": [
                    {"text": "Faktenbasiertheit"},
                    {"text": "Populismus"},
                    {"text": "Schlagfertigkeit"},
                    {"text": "Angriffslust"},
                    {"text": "Humor"}
                ]
            }
        ]

    def zeige_debatte(self):
        """Zeigt ein zufälliges Event an."""
        event = random.choice(self.events)
        self.events.remove(event)

        # Setze Titel und Beschreibung
        self.label_event_title.config(text=event["title"])
        self.label_event_description.config(text=event["description"])

        # Lade und zeige das Bild
        image_path = event["image"]
        if os.path.exists(image_path):
            image = Image.open(image_path).resize((300, 200), Image.Resampling.LANCZOS)
            self.event_image = ImageTk.PhotoImage(image)
            self.event_image_label.config(image=self.event_image)
        else:
            print(f"Fehler: Bildpfad nicht gefunden: {image_path}")

        # Erstelle Schieberegler für Strategien
        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for option in event["options"]:
            frame = tk.Frame(self.options_frame, bg="white")
            frame.pack(pady=5, fill="x")

            label = tk.Label(frame, text=option["text"], font=("Arial", 12), bg="white")
            label.pack(side="left", padx=10)

            slider = tk.Scale(frame, from_=0, to=10, orient="horizontal", cursor="hand2", bg="white", command=self.update_points)
            slider.pack(side="right", padx=10)

            self.strategy_sliders[option["text"]] = slider

    def update_points(self, *args):
        """Aktualisiert die verbleibenden Punkte und aktiviert/deaktiviert den Bestätigungs-Button."""
        total_used = sum(slider.get() for slider in self.strategy_sliders.values())
        self.remaining_points.set(self.max_points - total_used)
        self.remaining_label.config(text=f"Verbleibende Punkte: {self.remaining_points.get()}")

        if self.remaining_points.get() < 0:
            self.remaining_label.config(fg="red")
            self.confirm_button.config(state="disabled")
        else:
            self.remaining_label.config(fg="black")
            self.confirm_button.config(state="normal" if self.remaining_points.get() == 0 else "disabled")

    def confirm_selection(self):
        """Berechnet die finalen Gewichtungen basierend auf den Eingaben."""
        wahlkampf_seite = self.controller.frames["WahlkampfSeite"]
        current_party = wahlkampf_seite.get_own_party()

        # Poll-Daten vor dem Event speichern
        previous_polls = wahlkampf_seite.get_current_polls().copy()

        # own_score für TV-Debatte berechnen
        kandidat = kandidaten.get(current_party, {})
        f_weight = (self.strategy_sliders.get("Faktenbasiertheit").get() * kandidat.get("kompetenz", 0))
        p_weight = (self.strategy_sliders.get("Populismus").get() * kandidat.get("ambition", 0))
        s_weight = (self.strategy_sliders.get("Schlagfertigkeit").get() * (kandidat.get("ambition", 0) + kandidat.get("kompetenz", 0) / 2))
        a_weight = (self.strategy_sliders.get("Angriffslust").get() * (kandidat.get("ambition", 0) + kandidat.get("beliebtheit", 0) / 2))
        h_weight = (self.strategy_sliders.get("Humor").get() * (kandidat.get("kompetenz", 0) + kandidat.get("beliebtheit", 0) / 2))
        own_score = (f_weight + p_weight + s_weight + a_weight + h_weight) / 300

        # Gewicht für eigene Partei zufällig auf Basis von own_score
        own_weight = random.uniform(-1 + own_score, own_score)

        # Simuliere Wählerwanderung
        own_change = self.simulate_voter_shift_tvdebatte(own_weight, current_party)

        # Aktualisiere die Polls in der Wahlkampf-Seite
        wahlkampf_seite.polls[current_party] += own_change
        self.normalize_polls()

        # Wechsel zurück zur Wahlkampf-Seite
        self.controller.show_frame("WahlkampfSeite")

        # Zeige die Änderungen an
        wahlkampf_seite.update_poll_changes(
            current_party,
            "TV-Debatte",
            own_change,
            {party: wahlkampf_seite.polls[party] - previous_polls[party] for party in wahlkampf_seite.polls if party != current_party}
        )

    def simulate_voter_shift_tvdebatte(self, action_weight, current_party):
        """Simuliert die Veränderung der Wählerstimmen basierend auf dem Gewicht der Aktion."""
        total_shift = random.uniform(10, 15)
        party_weights = {party: random.uniform(-1, 1) for party in self.controller.frames["WahlkampfSeite"].polls if party != current_party}

        positive_sum = sum(w for w in party_weights.values() if w > 0) + max(0, action_weight)
        negative_sum = sum(w for w in party_weights.values() if w < 0) + min(0, action_weight)

        party_changes = {}
        for party, weight in party_weights.items():
            if weight > 0:
                party_changes[party] = (weight / positive_sum) * total_shift
            elif weight < 0:
                party_changes[party] = -(weight / negative_sum) * total_shift
            else:
                party_changes[party] = 0

        wahlkampf_seite = self.controller.frames["WahlkampfSeite"]
        for party, change in party_changes.items():
            wahlkampf_seite.polls[party] += change

        own_change = (action_weight / positive_sum) * total_shift if action_weight > 0 else 0

        return own_change

    def normalize_polls(self):
        """Normalisiert die Poll-Werte."""
        # Setze negative Werte auf 0
        wahlkampf_seite = self.controller.frames["WahlkampfSeite"]
        for party in wahlkampf_seite.polls:
            if wahlkampf_seite.polls[party] < 0:
                wahlkampf_seite.polls[party] = 0

        # Normalisiere die Werte, sodass sie insgesamt 100% ergeben       
        total = sum(wahlkampf_seite.polls.values())
        for party in wahlkampf_seite.polls:
            wahlkampf_seite.polls[party] = round(wahlkampf_seite.polls[party] / total * 100, 1)

class SpielendeSeite(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="white")
        self.controller = controller

        self.label_titel = tk.Label(self, text="Endergebnisse der Wahl", font=("Arial", 18, "bold"), bg="white")
        self.label_titel.pack(pady=20)

        self.polls_canvas = tk.Canvas(self, width=800, height=600, bg="white")
        self.polls_canvas.pack(pady=20)

        self.bundeskanzler_label = tk.Label(self, text="", font=("Arial", 16, "bold"), bg="white", fg="black")
        self.bundeskanzler_label.pack(pady=10)

        self.kandidaten_image_label = tk.Label(self, bg="white")
        self.kandidaten_image_label.pack(pady=20)

        self.collaboration_matrix = {}

        self.set_collaboration_score("CDU/CSU", "AfD", random.uniform(0.5, 0.7))
        self.set_collaboration_score("CDU/CSU", "Grüne", random.uniform(0.5, 0.7))
        self.set_collaboration_score("CDU/CSU", "SPD", random.uniform(0.6, 0.8))
        self.set_collaboration_score("CDU/CSU", "FDP", random.uniform(0.8, 1))
        self.set_collaboration_score("CDU/CSU", "Linke", random.uniform(0.3, 0.5))
        self.set_collaboration_score("CDU/CSU", "BSW", random.uniform(0.3, 0.5))

        self.set_collaboration_score("AfD", "Grüne", random.uniform(0.2, 0.4))
        self.set_collaboration_score("AfD", "SPD", random.uniform(0.2, 0.4))
        self.set_collaboration_score("AfD", "FDP", random.uniform(0.4, 0.6))
        self.set_collaboration_score("AfD", "Linke", random.uniform(0.1, 0.3))
        self.set_collaboration_score("AfD", "BSW", random.uniform(0.3, 0.5))

        self.set_collaboration_score("Grüne", "SPD", random.uniform(0.8, 1))
        self.set_collaboration_score("Grüne", "FDP", random.uniform(0.5, 0.7))
        self.set_collaboration_score("Grüne", "Linke", random.uniform(0.6, 0.8))
        self.set_collaboration_score("Grüne", "BSW", random.uniform(0.5, 0.7))

        self.set_collaboration_score("SPD", "FDP", random.uniform(0.5, 0.7))
        self.set_collaboration_score("SPD", "Linke", random.uniform(0.5, 0.7))
        self.set_collaboration_score("SPD", "BSW", random.uniform(0.5, 0.7))

        self.set_collaboration_score("FDP", "Linke", random.uniform(0.1, 0.3))
        self.set_collaboration_score("FDP", "BSW", random.uniform(0.1, 0.2))

        self.set_collaboration_score("Linke", "BSW", random.uniform(0.6, 0.8))

    def set_collaboration_score(self, party1, party2, score):
        """Setzt den Zusammenarbeitsscore für zwei Parteien."""
        if party1 not in self.collaboration_matrix:
            self.collaboration_matrix[party1] = {}
        if party2 not in self.collaboration_matrix:
            self.collaboration_matrix[party2] = {}
        self.collaboration_matrix[party1][party2] = score
        self.collaboration_matrix[party2][party1] = score

    def berechne_koalitionsbewertung(self, koalition, seat_distribution):
        """Berechnet die Bewertung einer Koalition basierend auf den Sitzen und Zusammenarbeitsscores."""
        gesamt_sitze = sum(seat_distribution[party] for party in koalition)
        zusammenarbeit_score = 0
        anzahl_koalitionspaare = 0
        
        # Berechne den Durchschnitt der Zusammenarbeitsscores für alle Paarungen innerhalb der Koalition
        for i in range(len(koalition)):
            for j in range(i + 1, len(koalition)):
                party1, party2 = koalition[i], koalition[j]
                zusammenarbeit_score += self.collaboration_matrix.get(party1, {}).get(party2, 0)
                anzahl_koalitionspaare += 1

        # Normierung des Zusammenarbeitsscores basierend auf der Koalitionsgröße (Zwei- oder Dreierbündnis)
        if anzahl_koalitionspaare > 0:
            durchschnitt_zusammenarbeit = zusammenarbeit_score / anzahl_koalitionspaare
        else:
            durchschnitt_zusammenarbeit = 1  # Falls keine Paare existieren, also bei einer Einzelpartei

        # Gesamtbewertung der Koalition
        bewertung = (gesamt_sitze * durchschnitt_zusammenarbeit)
        return bewertung

    def bestimme_best_koalition(self, possible_coalitions, seat_distribution):
        """Bestimmt die Koalition mit der besten Bewertung."""
        koalition_bewertungen = []

        for coalition in possible_coalitions:
            bewertung = self.berechne_koalitionsbewertung(coalition, seat_distribution)
            koalition_bewertungen.append((coalition, bewertung))

        # Sortiere Koalitionen nach ihrer Bewertung (höchste Bewertung zuerst)
        koalition_bewertungen.sort(key=lambda x: x[1], reverse=True)
        
        # Rückgabe der besten Koalition (erste in der sortierten Liste)
        return koalition_bewertungen[0][0] if koalition_bewertungen else None

    def zeige_endscreen(self, polls):
        """Zeigt die Endumfragen als Halbkreis-Diagramm an."""
        self.polls_canvas.delete("all")  # Vorherigen Inhalt löschen

        # Parteien mit >= 5% filtern
        visible_polls = {party: value for party, value in polls.items() if value >= 5 and party != "Sonstige"}
        total_votes = sum(visible_polls.values())

        # Define the desired order of the parties
        party_order = ["BSW", "Linke", "SPD", "Grüne", "FDP", "CDU/CSU", "AfD"]

        # Sort the visible_polls dictionary based on the party_order
        visible_polls = {party: visible_polls[party] for party in party_order if party in visible_polls}

        # Berechne Halbkreis-Werte
        start_angle = 180  # Halbkreis beginnt bei 180° (links)
        for party, value in visible_polls.items():
            extent = (value / total_votes) * 180  # Anteil des Halbkreises
            self.polls_canvas.create_arc(50, 50, 350, 350, start=start_angle, extent=-extent, fill=self.get_color(party))
            start_angle -= extent

        # Beschriftungen hinzufügen (alle Parteien, auch unter 5%)
        y_offset = 250
        for party, value in polls.items():
            self.polls_canvas.create_text(200, y_offset, text=f"{party}: {value:.1f}%", fill="black", font=("Arial", 12))
            y_offset += 20

        # Sitzverteilung berechnen
        total_seats = 650
        seat_distribution = {
            party: round((value / total_votes) * total_seats)
            for party, value in visible_polls.items()
        }

        # Sitzverteilung anzeigen
        y_offset += 20
        self.polls_canvas.create_text(200, y_offset, text="Sitzverteilung:", fill="black", font=("Arial", 12, "bold"))
        y_offset += 20
        for party, seats in seat_distribution.items():
            self.polls_canvas.create_text(200, y_offset, text=f"{party}: {seats} Sitze", fill="black", font=("Arial", 12))
            y_offset += 20

        # Mögliche Koalitionen berechnen
        majority_threshold = total_seats / 2  # Mehrheitsgrenze
        possible_coalitions = []

        # Zweier- und Dreier-Kombinationen prüfen
        parties = list(visible_polls.keys())
        for r in (1,2,3):  # Kombinationen aus 2 oder 3 Parteien
            for combination in itertools.combinations(parties, r):
                total_seats_combination = sum(seat_distribution[party] for party in combination)
                
                if r == 2:
                    # Prüfe alle Zweier-Kombinationen innerhalb der Dreier-Koalition
                    for subcombination in itertools.combinations(combination, 1):
                        total_seats_subcombination = sum(seat_distribution[party] for party in subcombination)
                        if total_seats_subcombination > majority_threshold:
                            break  # Überspringe diese 2er-Koalition
                    else:
                        # Nur hinzufügen, wenn keine 1-Parteien-Koalition die Mehrheit hat
                        if total_seats_combination > majority_threshold:
                            sorted_combination = sorted(combination, key=lambda party: seat_distribution[party], reverse=True)
                            possible_coalitions.append((sorted_combination, total_seats_combination))
                
                # Wenn es eine Dreier-Koalition ist und 2 Parteien bereits eine Mehrheit haben
                if r == 3:
                    # Prüfe alle Zweier-Kombinationen innerhalb der Dreier-Koalition
                    for subcombination in itertools.combinations(combination, 2):
                        total_seats_subcombination = sum(seat_distribution[party] for party in subcombination)
                        if total_seats_subcombination > majority_threshold:
                            break  # Überspringe diese 3er-Koalition
                    else:
                        # Nur hinzufügen, wenn keine 2-Parteien-Koalition die Mehrheit hat
                        if total_seats_combination > majority_threshold:
                            sorted_combination = sorted(combination, key=lambda party: seat_distribution[party], reverse=True)
                            possible_coalitions.append((sorted_combination, total_seats_combination))
                
                elif total_seats_combination > majority_threshold:
                    # Für 2-Parteien-Kombinationen direkt hinzufügen
                    sorted_combination = sorted(combination, key=lambda party: seat_distribution[party], reverse=True)
                    possible_coalitions.append((sorted_combination, total_seats_combination))

        # Bestimme die Koalition mit der höchsten Bewertung
        beste_koalition = self.bestimme_best_koalition([coalition for coalition, _ in possible_coalitions], seat_distribution)

        # Koalitionen anzeigen (auf der rechten Seite)
        x_offset = 400
        y_offset = 50
        self.polls_canvas.create_text(x_offset, y_offset, text="Mögliche Koalitionen:", fill="black", font=("Arial", 12, "bold"), anchor="w")
        y_offset += 20
        for coalition, seats in possible_coalitions:
            coalition_text = " + ".join(coalition)
            self.polls_canvas.create_text(x_offset, y_offset, text=f"{coalition_text}: {seats} Sitze", fill="black", font=("Arial", 12), anchor="w")
            y_offset += 20

        # "Gewinner"-Koalition anzeigen
        x_offset = 400
        y_offset = 340
        self.polls_canvas.create_text(x_offset, y_offset, text="Gewinner Koalition:", fill="black", font=("Arial", 12, "bold"), anchor="w")
        y_offset += 20
        if beste_koalition:
            coalition_text = " + ".join(beste_koalition)
            self.polls_canvas.create_text(x_offset, y_offset, text=f"{coalition_text}", fill="black", font=("Arial", 12), anchor="w")
            y_offset += 40

            # Label und Bild des Kandidaten der größten Partei in der Koalition unten rechts im Canvas anzeigen
            self.polls_canvas.create_text(400, 400, text="Und der neue deutsche Bundeskanzler ist:", fill="black", font=("Arial", 12, "bold"), anchor="w")
            
            largest_party = beste_koalition[0]  # Partei mit den meisten Sitzen
            kandidat = kandidaten.get(largest_party)
            if kandidat and os.path.exists(kandidat["bild"]):
                image = Image.open(kandidat["bild"]).resize((150, 150), Image.Resampling.LANCZOS)
                self.kandidat_image = ImageTk.PhotoImage(image)
                self.polls_canvas.create_image(400, 500, image=self.kandidat_image, anchor="w")
            else:
                self.polls_canvas.create_text(400, 500, text="Bild nicht verfügbar", fill="red", font=("Arial", 14), anchor="w")

    def get_color(self, party):
        """Gibt Farben für Parteien zurück."""
        colors = {
            "CDU/CSU": "black",
            "SPD": "red",
            "Grüne": "green",
            "FDP": "yellow",
            "AfD": "blue",
            "Linke": "purple",
            "BSW": "darkorchid"
        }
        return colors.get(party, "gray")