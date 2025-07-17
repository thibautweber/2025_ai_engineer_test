# Système multi-agent d'analyse des risques sur le lieu de travail

## Description
Ce projet propose un squelette minimal pour développer un système multi-agent d'analyse des risques. C'est un test technique qui s'inscrit dans le processus de recrutement enlaps pour le poste "Ingénieur IA".

## Structure du projet
- `src/main.py` : point d'entrée du projet
- `requirements.txt` : dépendances Python
- `Dockerfile` : conteneurisation du projet
- `rapport.md` : template de livrable markdown, à adapter, peut aussi être une page HTML statique
- `assets` : un dossier où placer les éléments mis à disposition sur le Drive qui vous aura été transmis par mail. 

Vous êtes libre d'utiliser ou non cette structure initiale. Le `rapport.md` est là pour proposer une source d'inspiration et non un format ou un contenu à respecter strictement.

### Assets

Des assets vous ont été transmis par mail (lien Google Drive). Ils contiennent des données qui ne doivent pas être intégrées à un repo git ni diffusée.

Ces données sont issues de deux caméras sur un même chantier et des données météo pour les jours de capture.

**REMARQUE** : les fichiers `metadata.json` proposent des metadatas associées aux images. Certaines images disposent de plus d'informations que les autres (champ `other`).

**REMARQUE** : Si vous ne souhaitez utiliser qu'une des deux cameras comme source de donnée, choisissez "EST-1" qui est plus riche.

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

Ce sont ces commandes qui seront utilisées lors de l'évaluation pour juger du résultat.

## Instructions pour le test

### Attendus

Il vous est demandé de développer un système multi-agent d'analyse des risques sur un chantier à partir de données multi-modales. Certaines vous sont fournies (images, détections, météo, ...), d'autres pourront être ajoutée à partir de sources publiques si vous le jugez pertinent (éléments de réglementation par exemple).

Spécifiquement:
- Développer un système capable de générer du langage naturel formatté dans un rapport à partir de données multi modales.
- Évaluer la performance du système et savoir proposer des améliorations.
- Présenter les résultats et expliquer les choix techniques.

**IMPORTANT** : Le sujet est volontairement vaste pour vous laisser la liberté d'approfondir certaines parties plus que d'autres. L'entretien technique qui aura lieu à la suite de ça sera l'occasion de discuter vos choix et vos idées pour les parties que vous n'auriez pas traitées. Il est possible de travailler des mois sur un tel sujet, faites attention à maitriser le temps que vous y passez et les aspects techniques que vous souhaitez mettre en avant.

### Stack technique

- Python + librairies : `langchain` pour le système d'agents, toute autre lib à votre convenance (attention à la taille de celles-ci toutefois svp)
- Docker pour livraison et exécution
- Historique git 
  
Si vous le jugez pertinent d'autres technos peuvent être utilisées en plus.

L'utilisation de LLM/Agents d'aide au code est autorisée.

### Instruction de rendu

Ce répo doit être fork sur votre espace perso (gitlab/github) et vous nous soumettrez un PR ou un lien vers votre répo au maximum la veille de l'entretien.

Possibilité en outre de nous fournir un lien vers une image Docker.

L'évaluation se fera avec la construction et l'exécution de l'image Docker.