# Projet Cybersécurité : Supervision et analyse réseau

![Visuel kick-off](assets/kickoff-image.png)

## Document source

- Document Word original : `1-Kick-off _ Projet Cybersécurité _ Supervision et analyse réseau.docx`

Ce document constitue la référence initiale du projet. Il fixe le besoin minimal, les contraintes techniques imposées et les critères de validation attendus lors de la présentation finale. Les documents suivants du dossier `documents/` déclinent cette consigne en analyse de marché, modèle économique, cadrage fonctionnel, gestion de projet, cahier des charges et architecture technique.

## Consigne initiale

Dans le cadre de ce projet, vous devez concevoir et réaliser un outil de supervision et d'analyse réseau dont vous êtes libres de choisir le nom. L'outil doit permettre d'observer et d'analyser un réseau informatique, d'en établir une cartographie exploitable, de détecter les événements suspects, de générer des alertes et d'exporter des rapports.

La consigne impose donc une approche complète : il ne s'agit pas uniquement de produire un scanner réseau, mais de construire une chaîne cohérente allant de l'observation technique à la restitution de preuves compréhensibles par un analyste ou un responsable de validation.

## Objectif du projet

L'objectif est de développer un outil capable de :

- détecter les équipements connectés au réseau ;
- scanner une plage d'adresses IP ;
- identifier les ports ouverts ;
- récupérer des informations sur les services réseau ;
- observer le trafic réseau ;
- détecter des comportements suspects ou malveillants ;
- générer des alertes ;
- produire des rapports exportables en JSON ou CSV.

Ces objectifs sont repris et enrichis dans le [cahier des charges](../../06_cahier_des_charges/rendu_principal.md) et dans l'[architecture technique](../../08_architecture/rendu_principal.md), afin de garantir une continuité entre la demande initiale et les choix de conception retenus.

## Contraintes techniques

- Backend : Python, avec FastAPI et les bibliothèques nécessaires au cœur fonctionnel de l'outil.
- Frontend : HTML, CSS, JavaScript, avec utilisation possible de Bootstrap ou Tailwind CSS.

## Ce que le projet doit démontrer

Le projet devra montrer votre capacité à :

- concevoir une solution technique cohérente ;
- développer un outil orienté cybersécurité ;
- travailler en équipe ;
- organiser un projet de manière professionnelle ;
- présenter et défendre votre solution.

## Livrables attendus

- Dépôt GitHub propre et structuré contenant l'intégralité du code source du projet, avec un versioning clair, des commits réguliers et explicites, ainsi qu'un README présentant l'outil et précisant l'installation et l'utilisation de la solution.
- Une release GitHub correspondant à la version finale, fonctionnelle et facilement testable du projet.
- Support de présentation au format PPT ou PDF, clair, structuré et paginé, accompagné d'une présentation finale avec démonstration.

La validation repose sur les éléments présentés et constatés pendant la présentation orale, tels qu'ils sont détaillés dans la grille de critères ci-dessous.

## Grille de critères - Projet cybersécurité

**Score final : /20**

| Bloc de compétences | Compétences validées | Sous-total |
|---|---|---|
| Bloc 1 - Cadrage du projet et compréhension du besoin | Présenter clairement le projet en indiquant son nom, son contexte et son objectif. (/0,5)<br>Définir de manière cohérente le besoin auquel il répond ainsi que son périmètre. (/0,75)<br>Justifier l'intérêt du projet et l'utilité de la solution proposée. (/0,75) | /2 |
| Bloc 2 - Gestion de projet et organisation d'équipe | Expliquer la méthode de travail utilisée pour organiser et gérer le projet, calendrier prévisionnel (Gantt), Kanban..(/0,5)<br>Présenter clairement l'organisation de l'équipe, les rôles attribués et la répartition des tâches. (/0,75)<br>Montrer le suivi de l'avancement et le pilotage du projet. (/0,5)<br>Identifier les risques du projet et expliquer la manière dont ils ont été gérés. (/0,75) | /2,5 |
| Bloc 3 - Architecture, conception et choix techniques | Présenter l'architecture globale de la solution de manière claire. (/1)<br>Justifier les choix techniques réalisés dans le projet. (/0,75)<br>Fournir des schémas clairs, lisibles et compréhensibles. (/0,5)<br>Architecturer la solution de manière cohérente et logique. (/0,75) | /3 |
| Bloc 4 - Réalisation technique de la solution | Développer une base applicative fonctionnelle. (/1)<br>Implémenter les principales fonctionnalités réseau attendues. (/1,25)<br>Implémenter les fonctionnalités d'analyse orientées cybersécurité. (/1,5)<br>Produire des résultats exploitables sous forme d'alertes, de logs et d'exports. (/0,75)<br>Développer une interface web cohérente avec l'ensemble de la solution. (/0,5) | /5 |
| Bloc 5 - Sécurité, qualité, tests et déploiement | Prendre en compte la sécurité de l'application dans sa conception et sa réalisation. (/0,75)<br>Montrer une démarche qualité dans le développement du projet. (/0,75)<br>Tester la solution de manière cohérente avant le déploiement et présenter les tests réalisés. (/0,75)<br>Expliquer la faisabilité du déploiement de la solution. (/0,75) | /3 |
| Bloc 6 - Démonstration, résultats et preuves | Réaliser une démonstration fluide et maîtrisée. (/0,75)<br>Montrer des résultats observables, cohérents et crédibles. (/0,75)<br>Relier clairement la démonstration au besoin initial du projet. (/0,5) | /2 |
| Bloc 7 - GitHub, versioning et traçabilité | Présenter un dépôt GitHub propre, structuré et permettant de retracer l'évolution du projet grâce à des commits réguliers. (/0,5)<br>Rédiger des messages de commit clairs et compréhensibles. (/0,25)<br>Maintenir une organisation de branches propre, avec un découpage par fonctionnalité. (/0,25) | /1 |
| Bloc 8 - Communication, présentation et valorisation | Fournir un support de présentation clair, paginé et mettant en valeur l'ensemble des éléments du projet. (/0,5)<br>Présenter le projet avec clarté, aisance et fluidité. (/0,5)<br>Défendre le projet, le valoriser et présenter ses perspectives d'évolution. (/0,5) | /1,5 |
| TOTAL GÉNÉRAL |  | /20 |

## Note de transcription

Ce fichier Markdown reprend intégralement le contenu du document Word de kick-off conservé dans ce même dossier, afin de faciliter la lecture, la citation et la traçabilité dans le dépôt.

Pour la suite du projet, ce kick-off doit être lu comme le socle de validation. Les choix fonctionnels, organisationnels et techniques doivent pouvoir être justifiés au regard de cette grille, notamment sur la clarté du besoin, la qualité de l'architecture, la capacité de démonstration, la traçabilité GitHub et la valeur professionnelle de la présentation finale.
