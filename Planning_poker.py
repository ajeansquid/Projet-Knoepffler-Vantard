# @author tvantard & Knoepffler

import tkinter as tk
from tkinter import ttk, messagebox

from models.user import User
from models.round import Round
from models.game import Game

# Classe qui vas faire écran entre les classes et l'interface visuelle

class PlanningPoker:
    def __init__(self):
        self.id= 1
        self.game= Game()
                
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

        # Bouton pour démarrer un round
        start_round_button = tk.Button(self.root, text="Créer Partie", command=self.create_gameMenu)
        start_round_button.pack(pady=20)

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
        self.rule_combobox = ttk.Combobox(rule_frame, values=["strict", "mediane", "moyenne", "majorite"], state="readonly")
        self.rule_combobox.grid(row=0, column=1, padx=5)
        self.rule_combobox.set(self.game.get_rule)

        set_rule_button = tk.Button(rule_frame, text="Définir règle", command=self.set_rule)
        set_rule_button.grid(row=0, column=2, padx=5)

        # Bouton pour démarrer un round
        start_round_button = tk.Button(self.root, text="Démarrer Round", command=self.start_round)
        start_round_button.pack(pady=20)


        
        # Section pour afficher le résultat du round
        self.result_label = tk.Label(self.root, text="Résultat du round: N/A", font=("Arial", 14))
        self.result_label.pack(pady=10)

    # Fonctions complémentaires
    
    def load_session(self):
        name = self.session_name_entry.get().strip()
        if name :
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
        self.game.set_rule(selected_rule)
        messagebox.showinfo("Règle définie", f"Règle choisie: {selected_rule}")

    def start_round(self):
        """Démarrer un round et afficher le résultat."""
        if not self.game.joueurs:
            messagebox.showwarning("Aucun joueur", "Ajoutez des joueurs avant de commencer un round.")
            return

        if not self.game.features:
            self.game.add_features(["Tâche 1", "Tâche 2", "Tâche 3"])  # Exemple de tâches

        resultat = self.game.start_round()
        self.result_label.config(text=f"Résultat du round: {resultat}")