# PROJ942 - Projet technique traitement de l'information

Dans le cadre de notre formation d’ingénieur en spécialité Instrumentation, Automatique et Informatique (IAI), nous avons un projet technique basé sur le traitement de l’information.
Ce dernier a pour but de mettre en application les compétences acquises précedemment.

Les domaines de compétence qui à mobiliser sont les suivants :
- Traitement de l'information (et plus particulièrement en traitement d'images et vision)
- Conception et programmation
- Traitement réparti
- Gestion de projet

L'objectif du projet est de mettre en oeuvre une application de reconnaissance de visage sur une des tablette de l'école.
Dans ce rapport, nous présenteront l'architecture du projet, les sous-parties de celui-ci, l'organisation du temps de travail et enfin les résultats qui ont étaient obtenus.

## Cahier des charges

L'application de reconnaissance de visage doit mettre en oeuvre diverses parties qui vont lui permettre de garantir un fonctionnement correct.
Nous allons ainsi nous servir d’une application tablette pour prendre une photo et l’envoyer au serveur.
Ensuite, un traitement sera réalisé sur l’image et annoncera le nom de la personne sur la photo.
L'identification se fera par comparaison avec les photos présentes dans la base de données que nous créerons plus tôt.

Application Android :
- Réalisation des interfaces graphiques
- Capture de photographies
- Paramétrage des options pour la connection au serveur
- Envoi et réception des données (images et textes) avec le serveur

Communication :
- Client permettant la communication entre l’application tablette et le serveur
- Serveur permettant la communication entre la tablette, le programme de reconnaissance et la base de données
