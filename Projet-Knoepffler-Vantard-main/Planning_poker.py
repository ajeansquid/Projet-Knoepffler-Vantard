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
        self.root.geometry("600x400")

        # Sections principales
        self.create_widgets()

        # Lancer la boucle principale de l'interface
        self.root.mainloop()

    def create_widgets(self):
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
        start_round_button = tk.Button(self.root, text="Démarrer Round", command=self.start_round)
        start_round_button.pack(pady=20)

        # Section pour afficher le résultat du round
        self.result_label = tk.Label(self.root, text="Résultat du round: N/A", font=("Arial", 14))
        self.result_label.pack(pady=10)

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

# Lancement de l'application
if __name__ == "__main__":
    PlanningPoker()