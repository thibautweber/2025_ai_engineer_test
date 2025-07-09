# Système multi-agent d'analyse des risques sur le lieu de travail

## Description
Ce projet propose un squelette minimal pour développer un système multi-agent d'analyse des risques à partir de données multi-modales (images, détections, météo, réglementation).

## Structure du projet
- `src/main.py` : point d'entrée du projet
- `requirements.txt` : dépendances Python
- `Dockerfile` : conteneurisation du projet
- `rapport.md` : template de livrable markdown, à adapter, peut aussi être une page HTML statique

## Utilisation

### Lancer en local
```bash
python src/main.py
```

### Construire et lancer avec Docker
```bash
docker build -t risk-analyzer .
docker run --rm risk-analyzer
```

## À compléter
- Ajouter les modules d'analyse d'image, de récupération de réglementation, de génération de rapport, etc.
- Compléter le fichier `requirements.txt` selon les besoins.
- Adapter le Dockerfile si besoin (doit être fonctionnel le jour du debrief, le code sera testé dans cet environnement).


