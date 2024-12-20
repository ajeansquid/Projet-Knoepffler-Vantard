# @author tvantard & Knoepffler

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

from models.user import User
from models.round import Round
from models.game import Game

# Classe qui vas faire écran entre les classes et l'interface visuelle

class PlanningPoker:
    def __init__(self):
        self.id = 1
        self.game = Game()
        self.current_player_index = 0
        self.current_round_index = 0
        self.current_round = None

        # Créer la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Planning Poker")
        self.root.geometry("1200x800")

        # Sections principales
        self.create_mainMenu()

        # Lancer la boucle principale de l'interface
        self.root.mainloop()

    def create_mainMenu(self):
        # Efface l'écran
        for widget in self.root.winfo_children():
            widget.destroy()

        # Titre
        tk.Label(self.root, text="Planning Poker", font=("Arial", 24)).pack(pady=20)

        # Boutons
        tk.Button(self.root, text="Commencer une partie", font=("Arial", 16), command=self.create_gameCreatingMenu).pack(pady=10)
        tk.Button(self.root, text="Charger une session", font=("Arial", 16), command=self.create_loadMenu).pack(pady=10)
        tk.Button(self.root, text="Quitter", font=("Arial", 16), command=self.root.quit).pack(pady=10)

    def create_gameCreatingMenu(self):
        # Efface l'écran
        for widget in self.root.winfo_children():
            widget.destroy()

        """Créer les éléments de l'interface graphique."""
        # Section pour ajouter un joueur
        add_user_frame = tk.Frame(self.root)
        add_user_frame.pack(pady=10)

        tk.Label(add_user_frame, text="Nom du joueur:").grid(row=0, column=0, padx=5)
        self.user_name_entry = tk.Entry(add_user_frame)
        self.user_name_entry.grid(row=0, column=1, padx=5)

        add_user_button = tk.Button(add_user_frame, text="Ajouter joueur", command=self.add_user)
        add_user_button.grid(row=0, column=2, padx=5)

        # Liste des joueurs
        self.players_listbox = tk.Listbox(self.root, height=8, width=40)
        self.players_listbox.pack(pady=10)

        # Section pour choisir la règle
        rule_frame = tk.Frame(self.root)
        rule_frame.pack(pady=10)

        tk.Label(rule_frame, text="Règle du round:").grid(row=0, column=0, padx=5)
        self.rule_combobox = ttk.Combobox(rule_frame, values=["strict", "mediane", "moyenne", "majorite"], state="readonly")
        self.rule_combobox.grid(row=0, column=1, padx=5)
        self.rule_combobox.set("strict")

        set_rule_button = tk.Button(rule_frame, text="Définir règle", command=self.set_rule)
        set_rule_button.grid(row=0, column=2, padx=5)

        # Section pour ajouter des fonctionnalités
        feature_frame = tk.Frame(self.root)
        feature_frame.pack(pady=10)

        tk.Label(feature_frame, text="Nom de la fonctionnalité:").grid(row=0, column=0, padx=5)
        self.feature_entry = tk.Entry(feature_frame)
        self.feature_entry.grid(row=0, column=1, padx=5)

        add_feature_button = tk.Button(feature_frame, text="Ajouter fonctionnalité", command=self.add_feature)
        add_feature_button.grid(row=0, column=2, padx=5)

        self.features_listbox = tk.Listbox(self.root, height=8, width=40)
        self.features_listbox.pack(pady=10)

        # Boutons pour charger et sauvegarder les fonctionnalités
        tk.Button(self.root, text="Charger fonctionnalités", command=self.load_features).pack(pady=5)
        tk.Button(self.root, text="Sauvegarder fonctionnalités", command=self.save_features).pack(pady=5)

        # Bouton pour créer la partie
        start_game_button = tk.Button(self.root, text="Créer Partie", command=self.create_gameMenu)
        start_game_button.pack(pady=20)

    def create_loadMenu(self):
        # Efface l'écran
        for widget in self.root.winfo_children():
            widget.destroy()

        load_session_frame = tk.Frame(self.root)
        load_session_frame.pack(pady=10)

        tk.Label(load_session_frame, text="Nom de la session.json :").grid(row=0, column=0, padx=5)
        self.session_name_entry = tk.Entry(load_session_frame)
        self.session_name_entry.grid(row=0, column=1, padx=5)

        load_session_button = tk.Button(load_session_frame, text="Enter", command=self.load_session)
        load_session_button.grid(row=0, column=2, padx=5)

    def create_gameMenu(self):
        # Définir la règle avant de détruire les widgets
        if hasattr(self, 'rule_combobox'):
            self.set_rule()

        # Efface l'écran
        for widget in self.root.winfo_children():
            widget.destroy()
        add_user_frame = tk.Frame(self.root)
        add_user_frame.pack(pady=10)

        # Liste des joueurs
        self.players_listbox = tk.Listbox(self.root, height=8, width=40)
        self.players_listbox.pack(pady=10)
        for player in self.game.get_users():
            self.players_listbox.insert(tk.END, player.get_name())

        # La règle
        rule_frame = tk.Frame(self.root)
        rule_frame.pack(pady=10)

        tk.Label(rule_frame, text="Règle du round:").grid(row=0, column=0, padx=5)
        self.rule_label = tk.Label(rule_frame, text=self.game.get_rule())
        self.rule_label.grid(row=0, column=1, padx=5)

        # Section pour afficher la fonctionnalité en cours de vote
        self.feature_label = tk.Label(self.root, text="Fonctionnalité: N/A", font=("Arial", 14))
        self.feature_label.pack(pady=10)

        # Section pour afficher le résultat du round
        self.result_label = tk.Label(self.root, text="Résultat du round: N/A", font=("Arial", 14))
        self.result_label.pack(pady=10)

        # Section pour les cartes à jouer
        self.card_buttons_frame = tk.Frame(self.root)
        self.card_buttons_frame.pack(pady=10)

        self.create_card_buttons()

        # Section pour afficher le plateau
        self.plateau_frame = tk.Frame(self.root)
        self.plateau_frame.pack(pady=10)

        # Démarrer le round
        self.start_round()

    def create_card_buttons(self):
        """Créer des boutons pour les cartes à jouer."""
        cards = ["0", "0.5", "1", "2", "3", "5", "8", "13", "20", "40", "100", "café", "?"]
        for card in cards:
            button = tk.Button(self.card_buttons_frame, text=card, command=lambda c=card: self.play_card(c))
            button.pack(side=tk.LEFT, padx=5)

    def play_card(self, card):
        """Jouer une carte."""
        if self.current_round is None:
            messagebox.showwarning("Erreur", "Le round n'a pas été initialisé.")
            return

        if self.current_player_index >= len(self.game.joueurs):
            messagebox.showwarning("Erreur", "Index du joueur actuel hors limites.")
            return

        current_player = self.game.joueurs[self.current_player_index]
        if self.game.joueurs[self.current_player_index].jouer(card, self.current_round, self.game.rule):
            messagebox.showwarning("Carte invalide", "Veuillez choisir une carte valide.")
        else:
            self.update_plateau()
            self.current_player_index += 1
            if self.current_player_index >= len(self.game.joueurs):
                # Tous les joueurs ont joué, vérifier le résultat
                result = self.current_round.ruleSplitter(self.game.rule)
                if result == "café":
                    self.save_session()  # Sauvegarder l'état du jeu
                    messagebox.showinfo("Fin de la partie", "Tous les joueurs ont voté 'café'. La session a été sauvegardée.")
                    self.create_mainMenu()  # Retourner au menu principal
                    return
                elif result == True:
                    self.end_round()
                elif isinstance(result, str):
                    messagebox.showinfo("Subround", result)
                    self.current_round_index = 0
                    self.update_plateau()
                    self.current_round.plateau = []  # Vider le plateau après le message

    def update_plateau(self):
        """Mettre à jour l'affichage du plateau."""
        for widget in self.plateau_frame.winfo_children():
            widget.destroy()
        for card in self.current_round.plateau:
            player_name = self.game.joueurs[card[0]].get_name()
            tk.Label(self.plateau_frame, text=f"{player_name}: {card[1]}").pack(side=tk.LEFT, padx=5)

    def check_round_end(self):
        """Vérifier si le round est terminé selon la règle."""
        result = self.current_round.ruleSplitter(self.game.rule)
        if result == "café":
            self.save_session()
            messagebox.showinfo("Session sauvegardée", "Tous les joueurs ont joué 'café'. La session a été sauvegardée.")
            self.create_mainMenu()
        elif result == True:
            self.end_round()
        elif isinstance(result, str):
            messagebox.showinfo("Subround", result)
            self.current_round_index = 0
            self.update_plateau()
            self.current_round.plateau = []  # Clear the plateau after showing the message

    def end_round(self):
        """Terminer le round et afficher le résultat."""
        resultat = self.current_round.getResultat()
        self.result_label.config(text=f"Résultat du round: {resultat}")
        self.current_round_index = 0
        self.current_player_index = 0
        self.current_round = Round(len(self.game.rounds) + 1, len(self.game.joueurs))
        self.game.rounds.append(self.current_round)
        if len(self.game.features) > len(self.game.rounds) - 1:
            self.current_round.defFeature(self.game.features[len(self.game.rounds) - 1])
        else:
            self.game.save_final_results()
            messagebox.showinfo("Fin des fonctionnalités", "Toutes les fonctionnalités ont été votées et sauvegardées.")
            self.create_mainMenu()
            return
        self.update_plateau()
        self.update_feature()

    def update_feature(self):
        """Mettre à jour l'affichage de la fonctionnalité en cours de vote."""
        if self.current_round and self.current_round.feature:
            self.feature_label.config(text=f"Fonctionnalité: {self.current_round.feature}")
        else:
            self.feature_label.config(text="Fonctionnalité: N/A")

    # Fonctions complémentaires

    def load_session(self):
        name = self.session_name_entry.get().strip()
        if name:
            self.game.load_sessionP(name)
            self.create_gameMenu()

    def add_user(self):
        """Ajouter un joueur à la liste."""
        name = self.user_name_entry.get().strip()
        if name:
            self.game.add_user(name)
            self.players_listbox.insert(tk.END, name)
            self.user_name_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrée invalide", "Veuillez entrer un nom de joueur.")

    def set_rule(self):
        """Définir la règle du jeu."""
        selected_rule = self.rule_combobox.get()
        if not selected_rule:
            selected_rule = "strict"
        self.game.set_rule(selected_rule)
        messagebox.showinfo("Règle définie", f"Règle choisie: {selected_rule}")

    def add_feature(self):
        """Ajouter une fonctionnalité à la liste."""
        feature = self.feature_entry.get().strip()
        if feature:
            self.game.features.append(feature)
            self.features_listbox.insert(tk.END, feature)
            self.feature_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrée invalide", "Veuillez entrer une fonctionnalité.")

    def load_features(self):
        """Charger les fonctionnalités depuis un fichier JSON."""
        filename = simpledialog.askstring("Charger fonctionnalités", "Nom du fichier JSON:")
        if filename:
            features = self.game.load_featuresP(filename)
            self.game.features = features
            self.features_listbox.delete(0, tk.END)
            for feature in features:
                self.features_listbox.insert(tk.END, feature)

    def save_features(self):
        """Sauvegarder les fonctionnalités dans un fichier JSON."""
        filename = simpledialog.askstring("Sauvegarder fonctionnalités", "Nom du fichier JSON:")
        if filename:
            features = self.game.features
            with open(filename, 'w') as file:
                json.dump(features, file)
            messagebox.showinfo("Sauvegarde réussie", f"Les fonctionnalités ont été sauvegardées dans {filename}.")

    def save_session(self):
        """Sauvegarder l'état de la session dans un fichier JSON."""
        filename = simpledialog.askstring("Sauvegarder session", "Nom du fichier JSON:")
        if filename:
            self.game.save_sessionP(filename)
            messagebox.showinfo("Sauvegarde réussie", f"La session a été sauvegardée dans {filename}.")
            self.create_mainMenu()

    def start_round(self):
        """Démarrer un round et afficher le résultat."""
        if len(self.game.joueurs) < 2:
            messagebox.showwarning("Nombre insuffisant de joueurs", "Ajoutez au moins deux joueurs avant de commencer un round.")
            self.create_gameCreatingMenu()
            return

        if not self.game.features:
            self.game.add_features(["Tâche 1", "Tâche 2", "Tâche 3"])  # Exemple de tâches

        self.current_round = Round(len(self.game.rounds) + 1, len(self.game.joueurs))
        self.game.rounds.append(self.current_round)
        self.current_round.defFeature(self.game.features[len(self.game.rounds) - 1])

        self.current_player_index = 0
        self.current_round_index = 0
        self.update_plateau()
        self.update_feature()
