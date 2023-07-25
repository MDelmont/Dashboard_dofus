# wsgi.py

from index import server  # Assurez-vous d'importer l'application Dash correctement depuis index.py
from gunicorn.app.base import BaseApplication

class StandaloneApplication(BaseApplication):
    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        for key, value in self.options.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application

if __name__ == "__main__":
    options = {
        "bind": "0.0.0.0:3002",  # Adaptez l'adresse et le port selon vos besoins
        "workers": 4,              # Adaptez le nombre de travailleurs selon vos besoins
    }
    StandaloneApplication(server, options).run()