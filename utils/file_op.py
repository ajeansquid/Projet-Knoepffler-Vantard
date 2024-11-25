import json

def load_features(filename):
    try:
        with open(filename, 'r') as files:
            return json.load(files)
    except FileNotFoundError:
        print(f"Le fichier {filename} n'a pas été trouvé.")
        return []
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans le fichier {filename}.")
        return []

def save_session(filename, session_data):
    try:
        with open(filename, 'w') as files:
            json.dump(session_data, files)
    except IOError:
        print(f"Erreur lors de la sauvegarde de la session dans le fichier {filename}.")

def load_session(filename):
    try:
        with open(filename, 'r') as files:
            return json.load(files)
    except FileNotFoundError:
        print(f"Le fichier {filename} n'a pas été trouvé.")
        return {}
    except json.JSONDecodeError:
        print(f"Erreur de décodage JSON dans le fichier {filename}.")
        return {}