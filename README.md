# Projet d'analyse de risques multi-agents sur chantier

Ce projet utilise un système multi-agent pour analyser des images de chantier et générer des rapports de risques.

## Prérequis
- Docker

## Lancement
1.  Clonez ce dépôt.
2.  Remplissez vos clés API dans le fichier `.env`
3.  Construisez l'image Docker :
    ```bash
    docker build -t risk-analysis-agent .
    ```
4.  Lancez le conteneur :
    ```bash
    docker run --rm --env-file .env risk-analysis-agent
    ```
Le rapport s'affichera dans la console.

## Avantages de la solution

1. Pertinence des risques : Le système identifie correctement les risques les plus critiques, comme le non-port des EPI et le risque de collision homme-machine, qui sont des préoccupations majeures sur les chantiers.

2. Corrélation des données : Il démontre sa capacité à croiser des sources de données distinctes (détections JSON + météo JSON) pour enrichir l'analyse. Par exemple, il ne se contente pas de dire "personne sans casque", mais "personne sans casque à proximité d'une grue", ce qui est bien plus puissant.

3. Ancrage réglementaire : L'intégration d'une recherche web pour citer des sources comme l'INRS ou Legifrance ancre l'analyse dans un contexte professionnel et crédible.

4. Modularité et clarté : Le rapport final est structuré, facile à lire et sépare bien le contexte (données brutes) de l'analyse (risques identifiés), le rendant directement utilisable.

## Limites actuelles

1. Analyse visuelle limitée : Le système dépend entièrement des métadonnées JSON. Il ne "voit" pas l'image. Il ne peut donc pas identifier des risques qui ne sont pas pré-détectés, comme un trou non sécurisé, un mauvais stockage de matériaux ou un risque d'ensevelissement.

2. Manque de contexte spatial : Les détections sont des listes d'objets. Le système ne comprend pas la disposition spatiale de ces objets. Il sait qu'il y a une personne et un camion, mais ne sait pas si la personne est en train de traverser juste devant le camion ou si elle se trouve à 20 mètres en toute sécurité.

3. Dépendance à la qualité des détections : Si le modèle de détection initial commet une erreur (ex: ne pas voir une personne), le risque associé est totalement ignoré. Le système n'a aucun moyen de remettre en question ses données d'entrée.

## Propositions d'améliorations

1. Passer à une analyse visuelle par un VLM (GPT-4o Ou LlaVa) pour décrire la scène précisément -> Plus de précision

2. RAG pour faire des recherches dans une base de données vérifiée et éviter les fausses informations sur internet
