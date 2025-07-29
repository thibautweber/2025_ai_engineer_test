# Projet d'analyse de risques multi-agents sur chantier

Ce projet utilise un système multi-agent pour analyser des images de chantier et générer des rapports de risques.

## Prérequis
- Docker

## Lancement
1.  Clonez ce dépôt.
2.  Créez un fichier `.env` à partir du fichier `.env.template` et remplissez vos clés API.
3.  Construisez l'image Docker :
    ```bash
    docker build -t risk-analysis-agent .
    ```
4.  Lancez le conteneur :
    ```bash
    docker run --rm --env-file .env risk-analysis-agent
    ```
Le rapport s'affichera dans la console.