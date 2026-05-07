# Gestion de projet - DevinciWatch

## 1. Objet du document

Ce document définit l'organisation et les modalités de pilotage du projet DevinciWatch. Il transforme le cadrage stratégique en dispositif d'exécution : méthode de travail, équipe projet, rôles Scrum, backlog produit, cérémonies, règles d'estimation, jalons, risques et indicateurs de suivi.

Il sert à préciser :

- la méthode Agile Scrum retenue ;
- l'équipe projet et la répartition des responsabilités ;
- les rôles et responsabilités ;
- les artefacts Scrum ;
- les cérémonies agiles ;
- les epics, features, user stories et tâches techniques ;
- les règles de story points ;
- la répartition des tâches par sprint ;
- les jalons et mécanismes de suivi ;
- les risques projet et les mesures de maîtrise.

Son objectif est de garantir que la progression du projet reste lisible, mesurable et cohérente avec les attentes produit, le périmètre MVP et les contraintes de démonstration.

### 1.1. Justification par les données (mai 2026)

L'analyse de 1 638 enregistrements valide le cadrage Scrum :
- **90 Story Points** pour couvrir 1 587 KEV + 30 CVEs 2026 → Effort justifié par volume menaces
- **5 sprints** (2 semaines) face à score intensité 1 114,8 → Rythme soutenu nécessaire
- **9 membres équipe** pour 7 sources + 3 conteneurs Docker → Ressources adaptées au risque
- **317 ransomware KEV** → Vélocité cible 18-28 SP/sprint indispensable pour protection rapide

## 2. Position dans la chronologie projet

Ce document intervient après :

- le [kick-off](../01_documents_pedagogiques/kickoff/KICKOFF.md) ;
- l'[étude de marché](../02_etude_de_marche/rendu_principal.md) ;
- le [business model](../03_business_model/rendu_principal.md) ;
- le [business plan](../04_business_plan/rendu_principal.md) ;
- la [feuille de cadrage](../05_feuille_de_cadrage/rendu_principal.md).

Il précède et structure :

- le [cahier des charges](../06_cahier_des_charges/rendu_principal.md) ;
- l'[architecture détaillée](../08_architecture/rendu_principal.md) ;
- le développement du produit.

## 3. Méthode de travail retenue : Agile Scrum

La méthode retenue est Agile Scrum. Ce choix est adapté à DevinciWatch car le produit doit être construit par incréments fonctionnels, validé régulièrement et ajusté en fonction de la valeur démontrée.

Scrum permet de découper le projet en cycles courts appelés sprints. Chaque sprint doit produire un incrément vérifiable : une fonctionnalité utilisable, un scénario reproductible, une preuve exportable, une amélioration de l'interface ou une stabilisation technique.

### Principes de pilotage Scrum

- avancer par incréments fonctionnels courts ;
- prioriser la valeur produit plutôt que l'accumulation de fonctionnalités ;
- rendre l'avancement visible dans un backlog ;
- estimer l'effort avec des story points ;
- limiter les travaux en cours pour réduire la dispersion ;
- vérifier chaque incrément avec une Definition of Done ;
- adapter le plan après chaque sprint review et rétrospective de sprint ;
- conserver un MVP démontrable à tout moment.

### Cadence recommandée

| Élément | Décision |
|---|---|
| Durée d'un sprint | 1 semaine |
| Nombre cible de sprints MVP | 5 sprints |
| Unité d'estimation | Story points |
| Échelle d'estimation | Fibonacci simplifiée : 1, 2, 3, 5, 8, 13 |
| Revue produit | À la fin de chaque sprint |
| Rétrospective | À la fin de chaque sprint |
| Suivi quotidien | Daily scrum court |

## 4. Équipe projet et rôles

L'équipe DevinciWatch est organisée autour de neuf profils complémentaires. Les noms ci-dessous sont utilisés comme noms de référence pour clarifier les responsabilités, en hommage à des figures majeures de l'informatique, de l'ingénierie logicielle et des réseaux.

| Personne | Rôle | Responsabilité principale |
|---|---|---|
| Ada Lovelace | Product Owner | Porter la vision produit, prioriser le backlog et accepter les user stories |
| Grace Hopper | Scrum Master | Faciliter Scrum, organiser les cérémonies et lever les obstacles |
| Alan Turing | Chef de projet | Suivre les jalons, les risques, les livrables et la cohérence globale |
| Barbara Liskov | Développeuse backend 1 | Concevoir les modèles, l'API FastAPI et la persistance PostgreSQL |
| Ken Thompson | Développeur backend 2 | Développer l'ingestion endpoint, les règles de détection et les workers Celery |
| Tim Berners-Lee | Développeur frontend | Réaliser le dashboard, les vues analyste et les parcours d'export |
| Margaret Hamilton | Testeuse / QA | Définir les scénarios de test, vérifier les critères d'acceptation et produire les preuves |
| Linus Torvalds | DevOps | Maintenir Docker, l'intégration, la configuration et la reproductibilité du lab |
| Radia Perlman | Ingénieure cybersécurité | Valider les règles de détection, la sécurité applicative et les scénarios contrôlés |

Cette répartition ne transforme pas Scrum en organisation hiérarchique rigide. Elle sert à rendre explicites les responsabilités, à éviter les zones floues et à garantir que chaque sprint produit un incrément complet : fonctionnel, testé, sécurisé, documenté et démontrable.

### Product Owner

Ada Lovelace porte la valeur produit. Elle est responsable du backlog, de la priorisation et de la cohérence avec la feuille de cadrage, le cahier des charges et les objectifs de validation.

Responsabilités :

- définir et prioriser les epics, features et user stories ;
- clarifier les critères d'acceptation ;
- arbitrer entre valeur produit, effort et risque ;
- maintenir le lien avec le positionnement issu de l'étude de marché ;
- accepter ou refuser les user stories en fin de sprint.

### Scrum Master

Grace Hopper garantit le bon fonctionnement de Scrum. Elle protège l'équipe contre la dérive du périmètre, facilite les cérémonies et aide à lever les blocages.

Responsabilités :

- organiser sprint planning, daily scrum, sprint review et rétrospective de sprint ;
- suivre les obstacles ;
- aider l'équipe à respecter la Definition of Ready et la Definition of Done ;
- maintenir une cadence réaliste ;
- rendre visibles les risques, dépendances et retards.

### Chef de projet

Alan Turing assure la cohérence de pilotage au-delà des cérémonies Scrum. Il ne remplace pas le Product Owner ni le Scrum Master : il suit les engagements, les jalons, les dépendances externes, les risques et la qualité des livrables.

Responsabilités :

- maintenir le planning de référence et la vision d'ensemble ;
- suivre les jalons J1 à J8 ;
- vérifier que les livrables documentaires et techniques restent cohérents ;
- consolider le registre des risques avec le Scrum Master ;
- préparer les points de revue projet avec le Product Owner ;
- arbitrer les dépendances organisationnelles sans modifier seul le backlog produit.

### Équipe de développement

L'équipe de développement réalise les incréments produit. Elle regroupe Barbara Liskov, Ken Thompson, Tim Berners-Lee, Margaret Hamilton, Linus Torvalds et Radia Perlman. Elle couvre les responsabilités backend, frontend, collecte endpoint, scénarios de test, documentation, sécurité, DevOps et qualité.

Responsabilités :

- découper les user stories en tasks techniques ;
- estimer les stories ;
- développer, tester et documenter les incréments ;
- maintenir la cohérence avec l'architecture ;
- produire des preuves vérifiables à chaque sprint.

### Répartition opérationnelle des rôles techniques

| Profil | Responsabilités détaillées | Exemples de tâches DevinciWatch |
|---|---|---|
| Barbara Liskov - Backend 1 | Architecture backend, modèles de données, API de consultation, cohérence PostgreSQL | modèles `users`, `assets`, `events`, `alerts`, routes de lecture, migrations, validation des données |
| Ken Thompson - Backend 2 | Ingestion, traitements asynchrones, détection, corrélation, intégration avec Redis/Celery | endpoints `heartbeat` et `events`, workers de détection, règles simples, corrélation IP et temporelle |
| Tim Berners-Lee - Frontend | Interface web intégrée au `serveur-soc`, lisibilité analyste, navigation et états d'écran | dashboard, vues actifs, événements, alertes, corrélations, exports CSV/JSON |
| Margaret Hamilton - Test / QA | Stratégie de test, recette fonctionnelle, preuves de validation, non-régression | scénarios collecte -> alerte -> preuve, tests API, vérification des critères d'acceptation, captures et exports |
| Linus Torvalds - DevOps | Lab Docker, configuration, scripts de lancement, stabilité d'environnement | Docker Compose, variables d'environnement, réseau de lab, logs, procédure de démarrage |
| Radia Perlman - Cybersécurité | Sécurité applicative, scénarios cyber contrôlés, pertinence des alertes | contrôle des `roles`, validation des payloads, auth agent, règles de détection, limites de scan |

### Parties prenantes

Les parties prenantes valident la lisibilité produit, la valeur métier et la conformité aux exigences.

Responsabilités :

- participer aux revues produit si nécessaire ;
- donner un retour sur la clarté, la valeur et la démontrabilité ;
- valider que les preuves produites sont compréhensibles et exploitables.

## 5. Artefacts Scrum

### Product backlog

Le product backlog regroupe l'ensemble des epics, features, user stories, tâches et améliorations potentielles. Il est vivant : il peut être ajusté, mais chaque changement doit préserver le périmètre MVP.

### Sprint backlog

Le sprint backlog regroupe les user stories sélectionnées pour un sprint. Il doit rester réaliste et ne pas dépasser la capacité estimée de l'équipe.

### Increment

L'incrément est le résultat utilisable produit à la fin d'un sprint. Pour DevinciWatch, un incrément peut être :

- un endpoint API fonctionnel ;
- une vue d'interface utilisable ;
- une règle de détection démontrable ;
- une corrélation visible ;
- un export CSV/JSON ;
- une documentation de lancement ;
- un scénario Docker reproductible.

### Definition of Ready

Une user story est prête à entrer dans un sprint si :
- son objectif est clair ;
- son utilisateur cible est identifié ;
- ses critères d'acceptation sont rédigés ;
- ses dépendances sont connues ;
- son effort est estimé en story points ;
- elle est réalisable dans un sprint ou découpée.

#### Exemples concrets pour DevinciWatch

| User Story | Critères Definition of Ready |
|---|---|
| US-01.1 Authentification | Schéma utilisateur défini, route `/login` créée dans `serveur-soc`, payload JWT prêt, test de connexion initial |
| US-02.1 Heartbeat | Schéma heartbeat défini, route `/heartbeat` existe, format JSON validé, agent secret configuré |
| US-02.2 Events | Schéma event défini, route `/events` POST prête, validation payload, persistance PostgreSQL prévue |
| US-03.1 Scan IP | Plage IP lab définie, scan contrôlé autorisé, modèle asset lié, affichage liste prévu |
| US-04.1 Alerte | Règle simple codée, worker Celery configuré, modèle alerte créé, scénario suspect prêt |
| US-05.1 Corrélation IP | Logique de groupement codée, requête PostgreSQL prête, vue corrélation prévue |
| US-06.1 Dashboard | Composants UI de base, endpoint `/summary` prêt, navigation dashboard prévue |
| US-07.1 Export CSV | Format CSV défini, endpoint `/export` prêt, log audit configuré |

### Definition of Done

Une user story est terminée si :
- le comportement attendu est implémenté ;
- les critères d'acceptation sont vérifiés ;
- les erreurs principales sont gérées ;
- les données utiles sont persistées ou affichées ;
- la fonctionnalité est intégrée au lab ou à l'interface si nécessaire ;
- la documentation minimale est mise à jour ;
- une preuve de validation existe : capture, log, export, test ou scénario reproductible.

#### Exemples concrets pour DevinciWatch

| User Story | Critères Definition of Done |
|---|---|
| US-01.1 Authentification | Connexion valide acceptée, token JWT retourné, route `/me` renvoie utilisateur, accès refusé sans token |
| US-02.1 Heartbeat | Dernier heartbeat visible côté `serveur-soc`, timestamp persistant, agent authentifié, JSON valide reçu |
| US-02.2 Events | Event persisté en base, visible via API `/events`, horodatage correct, payload validé |
| US-03.1 Scan IP | Actif créé après scan, IP/ports/services visibles, scan limité au lab Docker |
| US-04.1 Alerte | Alerte générée dans le lab, visible dans dashboard, statut modifiable, log audit créé |
| US-05.1 Corrélation IP | Groupe créé pour événements liés, IP source affichée, historique consultable |
| US-06.1 Dashboard | Métriques affichées (events, alertes, endpoints), navigation fluide, exports visibles |
| US-07.1 Export CSV | Fichier CSV généré avec en-têtes, téléchargement fonctionnel, log audit de l'export |
| US-08.2 Scénario contrôlé | Scénario replayable, chaîne heartbeat→event→alerte→preuve, documentation des étapes |

## 6. Cérémonies agiles

Les cérémonies Scrum doivent être préparées, limitées dans le temps et orientées décision. Chaque cérémonie produit un résultat concret : backlog ajusté, sprint engagé, blocage levé, story acceptée, action d'amélioration ou risque mis à jour.

| Cérémonie | Animation | Participants obligatoires | Participants selon besoin | Résultat attendu |
|---|---|---|---|---|
| Sprint planning | Grace Hopper | Ada Lovelace, Alan Turing, équipe de développement | Parties prenantes si arbitrage produit | Sprint goal, sprint backlog, capacité engagée |
| Daily scrum | Grace Hopper | Équipe de développement | Alan Turing si risque ou blocage important | Blocages visibles, priorités du jour claires |
| Backlog refinement | Ada Lovelace et Grace Hopper | Backend, frontend, QA, cybersécurité, DevOps selon stories | Alan Turing pour dépendances et risques | Stories prêtes, critères clarifiés, estimation ajustée |
| Sprint review | Ada Lovelace | Toute l'équipe projet | Parties prenantes | Stories acceptées ou retournées au backlog |
| Rétrospective de sprint | Grace Hopper | Toute l'équipe projet | Aucun intervenant externe par défaut | Une à trois actions d'amélioration mesurables |

### Sprint planning

Objectif : définir l'objectif du sprint et sélectionner les user stories à traiter.

Entrées : backlog priorisé, vélocité précédente, risques ouverts, dépendances techniques.

Sorties : sprint goal, sprint backlog, découpage en tasks, estimation confirmée.

Déroulement attendu :

- Ada Lovelace rappelle la priorité produit et les stories candidates ;
- Alan Turing rappelle les jalons, les contraintes de planning et les risques ouverts ;
- Barbara Liskov, Ken Thompson, Tim Berners-Lee, Margaret Hamilton, Linus Torvalds et Radia Perlman confirment les dépendances techniques ;
- Grace Hopper vérifie que les stories respectent la Definition of Ready ;
- l'équipe estime ou confirme les story points ;
- le sprint backlog est arrêté uniquement si la capacité est réaliste.

Questions clés :

- quelle valeur produit doit être visible à la fin du sprint ?
- quelles stories sont prêtes ?
- quelles dépendances peuvent bloquer ?
- quelle capacité réelle l'équipe peut-elle engager ?

### Daily scrum

Objectif : synchroniser l'équipe et identifier les blocages.

Durée cible : 10 à 15 minutes.

Questions clés :

- qu'est-ce qui a été terminé depuis le dernier point ?
- qu'est-ce qui est prévu avant le prochain point ?
- quel obstacle empêche l'avancement ?

Le daily scrum ne doit pas devenir une réunion de reporting détaillée. Les sujets longs sont traités séparément.

Déroulement attendu avec l'équipe :

- chaque membre technique indique ce qui est terminé, ce qui est prévu et ce qui bloque ;
- Margaret Hamilton signale les tests bloqués ou les critères d'acceptation ambigus ;
- Linus Torvalds signale les problèmes de lab, de configuration ou de reproductibilité ;
- Radia Perlman signale les risques de sécurité ou de scénario cyber non maîtrisé ;
- Grace Hopper transforme les obstacles en actions suivies ;
- Alan Turing n'utilise pas le daily scrum comme comité de reporting, mais peut noter un risque projet si un blocage menace un jalon.

### Backlog refinement

Objectif : préparer les stories des prochains sprints.

Activités :

- préciser les critères d'acceptation ;
- découper les stories trop grandes ;
- réévaluer les story points ;
- vérifier les dépendances avec le cahier des charges et l'architecture ;
- retirer les éléments hors périmètre MVP.

Règles d'organisation :

- Ada Lovelace prépare les priorités avant la séance ;
- Grace Hopper veille à ce que les discussions restent orientées préparation du backlog ;
- les deux développeurs backend évaluent les impacts API, base de données, workers et ingestion ;
- le développeur frontend vérifie les impacts UX, navigation et lisibilité analyste ;
- la testeuse vérifie que les critères d'acceptation sont testables ;
- le DevOps vérifie la compatibilité avec Docker et l'environnement de lab ;
- l'ingénieure cybersécurité vérifie les exigences d'authentification, de contrôle d'accès, de payloads et de scénarios contrôlés.

### Sprint review

Objectif : présenter l'incrément produit et recueillir les retours.

La revue doit montrer des éléments observables : écran, API, logs, alerte, export, corrélation, scénario Docker ou documentation.

Sorties : stories acceptées, retours produit, ajustements éventuels du backlog.

Déroulement attendu :

- Tim Berners-Lee présente les écrans et le parcours utilisateur si l'incrément contient une interface ;
- Barbara Liskov ou Ken Thompson présente les endpoints, traitements, règles ou données persistées ;
- Linus Torvalds montre que l'incrément fonctionne dans le lab Docker ;
- Radia Perlman explique les garanties de sécurité et les limites du scénario cyber ;
- Margaret Hamilton présente les tests réalisés et les preuves produites ;
- Ada Lovelace accepte ou refuse les user stories selon les critères d'acceptation ;
- Alan Turing met à jour les jalons, les risques et les décisions de pilotage.

### Rétrospective de sprint

Objectif : améliorer la manière de travailler.

Questions clés :

- qu'est-ce qui a bien fonctionné ?
- qu'est-ce qui a ralenti l'équipe ?
- quelle amélioration concrète appliquer au sprint suivant ?

La rétrospective de sprint doit produire au moins une action d'amélioration mesurable.

Déroulement attendu :

- Grace Hopper anime la discussion et garantit un cadre factuel ;
- chaque membre partage un point positif, un irritant et une proposition d'amélioration ;
- l'équipe distingue les problèmes de produit, de méthode, de technique, de tests, de sécurité et d'environnement ;
- une action d'amélioration est assignée à une personne responsable ;
- Alan Turing vérifie que les actions retenues sont compatibles avec le planning et les jalons.

Les actions issues de la rétrospective de sprint doivent être limitées en nombre. Une action simple, appliquée au sprint suivant, est préférable à une liste longue non suivie.

## 7. Story points et estimation

Les story points mesurent l'effort relatif d'une user story. Ils ne représentent pas directement des heures. Ils combinent complexité technique, incertitude, volume de travail, dépendances et risque.

### Échelle retenue

| Story points | Signification | Exemple |
|---|---|---|
| 1 | Très simple, faible incertitude | Ajouter un champ affiché dans une vue existante |
| 2 | Simple, peu de dépendances | Ajouter une route de lecture simple |
| 3 | Moyen, effort clair | Créer une vue liste avec données persistées |
| 5 | Complexe mais maîtrisable | Implémenter une règle de détection complète |
| 8 | Complexe, plusieurs composants | Corrélation entre événements et affichage associé |
| 13 | Trop gros pour un sprint standard | Epic ou story à redécouper |

### Règles d'estimation

- une story à 13 points doit être redécoupée ;
- une story sans critères d'acceptation ne doit pas être estimée définitivement ;
- les stories liées à la sécurité ou à la persistance doivent inclure l'effort de validation ;
- les tâches techniques invisibles mais nécessaires doivent être rattachées à une story ou à une technical story ;
- la vélocité doit être observée après deux sprints avant d'être utilisée comme référence.

### Capacité initiale

Pour les premiers sprints, la capacité cible peut être fixée à titre indicatif entre 18 et 24 points par sprint. Cette valeur doit être ajustée après observation réelle de la vélocité.

## 8. Product backlog structuré

### Vue d'ensemble des epics

| Epic | Objectif | Priorité | Total SP | Sprint cible |
|---|---|---|---|---|
| EPIC-01 - Socle applicatif et sécurité | Poser les bases FastAPI, authentification, rôles, configuration et santé applicative | P1 | 10 | Sprint 1 |
| EPIC-02 - Collecte endpoint et télémétrie | Recevoir `heartbeat` et `events` depuis le `serveur-endpoint` | P1 | 13 | Sprint 2 |
| EPIC-03 - Découverte réseau et actifs | Identifier actifs, ports et services observables dans le lab | P1 | 13 | Sprint 2-3 |
| EPIC-04 - Détection, alertes et audit | Générer, consulter et tracer les alertes et actions sensibles | P1 | 11 | Sprint 3 |
| EPIC-05 - Corrélation et enrichissement analyste | Regrouper des événements liés pour améliorer la lisibilité SOC | P2 | 18 | Sprint 4 |
| EPIC-06 - Interface web et visualisation | Fournir un dashboard et des vues analyste exploitables | P1 | 13 | Sprint 4 |
| EPIC-07 - Reporting, exports et preuves | Produire des exports CSV/JSON et des preuves de validation | P1 | 9 | Sprint 4-5 |
| EPIC-08 - Lab Docker, démonstration et documentation | Stabiliser le lab, les scénarios et la documentation de lancement | P1 | 13 | Sprint 1, 5 |
| **Total MVP** | | | **90 SP** | **5 sprints** |

## 9. Features par epic

| Epic | Feature | Description | Priorité |
|---|---|---|---|
| EPIC-01 | FEAT-01.1 Authentification | Connexion utilisateur, session/token, endpoint `/me` | P1 |
| EPIC-01 | FEAT-01.2 Contrôle d'accès | Gestion des `roles` `admin` et `analyst` | P1 |
| EPIC-01 | FEAT-01.3 Santé applicative | Endpoint `GET /health`, logs applicatifs de base | P1 |
| EPIC-02 | FEAT-02.1 Heartbeat | Ingestion et affichage du dernier `heartbeat` | P1 |
| EPIC-02 | FEAT-02.2 Events | Ingestion, validation et persistance des événements | P1 |
| EPIC-02 | FEAT-02.3 Auth agent | Authentification du `serveur-endpoint` auprès de l'API | P1 |
| EPIC-03 | FEAT-03.1 Scan IP | Scan contrôlé du réseau de lab | P1 |
| EPIC-03 | FEAT-03.2 Inventaire actifs | Création et mise à jour des actifs | P1 |
| EPIC-03 | FEAT-03.3 Ports et services | Association ports/services aux actifs | P1 |
| EPIC-04 | FEAT-04.1 Règles simples | Détection de comportements suspects contrôlés | P1 |
| EPIC-04 | FEAT-04.2 Cycle de vie alertes | Liste, détail, statut minimal | P1 |
| EPIC-04 | FEAT-04.3 Audit | Journalisation connexions, exports, actions sensibles | P1 |
| EPIC-05 | FEAT-05.1 Corrélation IP | Regroupement par IP source | P2 |
| EPIC-05 | FEAT-05.2 Corrélation temporelle | Regroupement par fenêtre temporelle | P2 |
| EPIC-05 | FEAT-05.3 Vue corrélation | Consultation des groupes de corrélation | P2 |
| EPIC-06 | FEAT-06.1 Dashboard | Métriques clés : événements, alertes, endpoints, exports | P1 |
| EPIC-06 | FEAT-06.2 Vues analyste | Actifs, événements, alertes, audit | P1 |
| EPIC-06 | FEAT-06.3 Visualisation enrichie | IP attaquantes, carte géographique si faisable | P3 |
| EPIC-07 | FEAT-07.1 Export CSV | Export des événements ou alertes | P1 |
| EPIC-07 | FEAT-07.2 Export JSON | Export structuré exploitable | P1 |
| EPIC-07 | FEAT-07.3 Export XML | Extension si temps disponible | P3 |
| EPIC-08 | FEAT-08.1 Docker Compose | Lab `serveur-soc`, `serveur-endpoint`, `serveur-attacker` | P1 |
| EPIC-08 | FEAT-08.2 Scénarios contrôlés | Scénarios reproductibles de détection | P1 |
| EPIC-08 | FEAT-08.3 Documentation | Procédure de lancement, validation et preuves | P1 |

## 10. User stories et tasks MVP

### EPIC-01 - Socle applicatif et sécurité

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-01.1 | En tant qu'utilisateur, je veux me connecter à l'application afin d'accéder aux fonctions protégées. | 5 | créer modèle utilisateur ; créer route login ; gérer token/session ; protéger routes privées (voir [Architecture §5](08_architecture/rendu_principal.md#5-architecture-logicielle) | Connexion valide acceptée, connexion invalide refusée |
| US-01.2 | En tant qu'administrateur, je veux distinguer les `roles` afin de limiter les actions sensibles. | 3 | définir `admin` / `analyst` ; ajouter contrôle d'accès ; tester refus d'action | Un analyste ne peut pas effectuer une action réservée à l'admin |
| US-01.3 | En tant qu'équipe produit, je veux connaître l'état de l'application afin de vérifier rapidement le lab. | 2 | créer `/health` ; afficher état API ; logger erreurs principales | `/health` répond et indique l'état applicatif |

### EPIC-02 - Collecte endpoint et télémétrie

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-02.1 | En tant que `serveur-endpoint`, je veux envoyer un `heartbeat` afin d'indiquer que je suis actif. | 3 | créer schéma heartbeat ; route ingestion (voir [Architecture §5](08_architecture/rendu_principal.md#5-architecture-logicielle)) ; persistance PostgreSQL ; vue dernier heartbeat | Heartbeat visible côté `serveur-soc` |
| US-02.2 | En tant que `serveur-endpoint`, je veux envoyer des événements afin d'alimenter la détection. | 5 | créer schéma event ; validation payload ; persistance ; endpoint liste events | Events consultables et horodatés |
| US-02.3 | En tant que système, je veux authentifier les agents afin de refuser les sources inconnues. | 5 | définir secret agent ; middleware/API key ; rejet requêtes invalides ; logs | Requête non autorisée refusée |

### EPIC-03 - Découverte réseau et actifs

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-03.1 | En tant qu'analyste, je veux voir les actifs détectés afin de comprendre le périmètre surveillé. | 5 | modèle asset ; création depuis événements ; liste API ; vue interface | Actifs visibles avec IP et dernière observation |
| US-03.2 | En tant qu'analyste, je veux connaître les ports ouverts afin d'identifier les services exposés. | 5 | scan contrôlé ; modèle findings ; association asset ; affichage ports | Ports associés à un actif |
| US-03.3 | En tant que responsable validation, je veux limiter les scans au lab afin d'éviter tout comportement non maîtrisé. | 3 | config réseau autorisé ; garde-fous scan ; documentation | Scan borné au réseau Docker prévu |

### EPIC-04 - Détection, alertes et audit

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-04.1 | En tant qu'analyste, je veux obtenir une alerte lorsqu'un comportement suspect est observé. | 5 | règle simple (voir [Cahier des charges §9.1](06_cahier_des_charges/rendu_principal.md#91-règles-métier)) ; worker Celery ; modèle alerte ; persistance PostgreSQL | Scénario suspect génère une alerte visible dans dashboard |
| US-04.2 | En tant qu'analyste, je veux consulter la liste et le détail des alertes afin de qualifier la situation. | 3 | endpoints liste/détail ; vue alertes ; statut minimal | Alerte consultable avec contexte |
| US-04.3 | En tant que responsable validation, je veux tracer les actions sensibles afin de disposer d'une preuve d'audit. | 3 | modèle audit log ; logs login/export/action ; vue ou endpoint audit | Actions sensibles journalisées |

### EPIC-05 - Corrélation et enrichissement analyste

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-05.1 | En tant qu'analyste, je veux regrouper des événements par IP source afin d'identifier une activité répétée. | 8 | règle corrélation IP (voir [Architecture §5](08_architecture/rendu_principal.md#5-architecture-logicielle)) ; modèle correlation_group Redis ; association events PostgreSQL | Groupe créé pour événements liés, visible côté analyste |
| US-05.2 | En tant qu'analyste, je veux corréler des événements dans une fenêtre temporelle afin de détecter une séquence suspecte. | 8 | paramètre fenêtre ; requête temporelle ; scoring simple ; tests scénario | Répétition temporelle visible |
| US-05.3 | En tant qu'analyste, je veux consulter les corrélations afin de comprendre pourquoi une alerte est enrichie. | 5 | endpoint corrélations ; vue interface ; lien alerte-corrélation | Corrélation consultable et explicable |

### EPIC-06 - Interface web et visualisation

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-06.1 | En tant qu'analyste, je veux un dashboard synthétique afin de lire rapidement l'état du système. | 5 | définir métriques ; endpoint summary ; composants UI ; affichage | Dashboard affiche endpoints, events, alerts, exports |
| US-06.2 | En tant qu'analyste, je veux naviguer entre actifs, événements et alertes afin d'investiguer efficacement. | 5 | navigation ; vues listes ; vues détail ; états vides | Parcours analyste complet |
| US-06.3 | En tant qu'analyste, je veux voir les IP attaquantes afin d'identifier les sources récurrentes. | 3 | agrégation IP ; endpoint ; affichage tableau | IP sources visibles avec fréquence |

### EPIC-07 - Reporting, exports et preuves

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-07.1 | En tant qu'analyste, je veux exporter les alertes en CSV afin de produire une preuve exploitable. | 3 | générer CSV ; endpoint export ; téléchargement ; log audit | CSV généré et téléchargeable |
| US-07.2 | En tant qu'analyste, je veux exporter les données en JSON afin de conserver une preuve structurée. | 3 | générer JSON ; endpoint export ; métadonnées ; log audit | JSON généré et exploitable |
| US-07.3 | En tant que responsable validation, je veux relier un export à un scénario afin de vérifier la cohérence des preuves. | 3 | nommage export ; métadonnées scénario ; documentation | Export compréhensible et rattaché au scénario |

### EPIC-08 - Lab Docker, démonstration et documentation

| Story | User story | SP | Tasks principales | Critères d'acceptation |
|---|---|---:|---|---|
| US-08.1 | En tant qu'équipe produit, je veux démarrer les trois conteneurs afin de disposer d'un lab reproductible. | 5 | Docker Compose ; réseau dédié ; variables config ; test démarrage | `serveur-soc`, `serveur-endpoint`, `serveur-attacker` démarrent |
| US-08.2 | En tant que responsable validation, je veux un scénario contrôlé afin de rejouer la chaîne complète. | 5 | script scénario ; génération events ; documentation étapes ; vérification alerte | Scénario collecte -> alerte -> preuve reproductible |
| US-08.3 | En tant que contributeur, je veux une documentation claire afin de lancer et vérifier le produit. | 3 | README lancement ; procédure validation ; captures attendues ; troubleshooting | Documentation suffisante pour relancer le lab |

## 11. Découpage prévisionnel par sprint

| Sprint | Sprint goal | Stories prioritaires | Livrable attendu |
|---|---|---|---|
| Sprint 1 | Poser le socle applicatif sécurisé | US-01.1, US-01.2, US-01.3, US-08.1 | Application lançable, auth minimale, santé API, Docker initial |
| Sprint 2 | Ingestion et inventaire initial | US-02.1, US-02.2, US-02.3, US-03.1 | Heartbeat/events persistés, agents authentifiés, actifs visibles |
| Sprint 3 | Détection, alertes et audit | US-03.2, US-03.3, US-04.1, US-04.2, US-04.3 | Scénario suspect produisant une alerte consultable et auditée |
| Sprint 4 | Interface analyste, corrélation et exports | US-05.1, US-06.1, US-06.2, US-07.1, US-07.2 | Dashboard, alertes, corrélation IP, exports CSV/JSON |
| Sprint 5 | Stabilisation, preuve et validation complète | US-05.2, US-05.3, US-06.3, US-07.3, US-08.2, US-08.3 | Chaîne complète reproductible, documentation et preuves prêtes |

Le découpage reste prévisionnel. Il peut être ajusté à chaque sprint planning selon la vélocité réelle, les risques techniques et la stabilité du lab.

### Répartition des tâches par sprint

| Sprint | Backend 1 - Barbara Liskov | Backend 2 - Ken Thompson | Frontend - Tim Berners-Lee | QA - Margaret Hamilton | DevOps - Linus Torvalds | Cybersécurité - Radia Perlman | Pilotage - Ada / Grace / Alan |
|---|---|---|---|---|---|---|---|
| Sprint 1 | Modèles utilisateur, routes auth, endpoint `/health` | Préparer structure ingestion et services internes | Écran login, base du dashboard, navigation initiale | Cas de test auth et santé API | Docker Compose initial, variables, logs | Règles `roles`, exigences de secrets, contrôle routes protégées | Prioriser P1, cadrer sprint goal, suivre risques initiaux |
| Sprint 2 | Modèles `assets`, `events`, routes de consultation | Endpoints `heartbeat` et `events`, auth agent | Vues endpoints, actifs et événements | Tests ingestion, payloads invalides, preuves heartbeat | Stabilité réseau Docker, configuration agent | Validation payloads, limitation sources inconnues | Ajuster backlog selon vélocité et dépendances |
| Sprint 3 | Modèles alertes, audit log, routes alertes | Règles de détection, scan contrôlé, traitement worker | Vues alertes, détail alerte, audit | Recette scénario suspect -> alerte | Scripts de scénario contrôlé, logs reproductibles | Limites de scan, pertinence des règles, sécurité audit | Vérifier jalons J4/J5 et arbitrer les P2/P3 |
| Sprint 4 | API métriques, API corrélations, endpoints export | Corrélation IP, génération CSV/JSON, worker export | Dashboard, corrélations, parcours export | Tests dashboard, exports, cohérence des preuves | Vérification volumes, chemins exports, relance lab | Vérification données exposées, traçabilité export | Préparer revue produit complète et gérer retours |
| Sprint 5 | Stabilisation API, corrections, documentation technique | Corrélation temporelle, finalisation scénario complet | Finitions UX, états vides, IP attaquantes | Recette complète, non-régression, captures finales | Procédure lancement, reset lab, troubleshooting | Revue sécurité finale et limites documentées | Clôturer jalons, préparer bilan et support final |

### Règles de collaboration entre rôles

- une user story ne doit pas être engagée si le backend, le frontend, les tests, le DevOps ou la cybersécurité nécessaires ne sont pas identifiés ;
- les développeurs backend travaillent en binôme sur les contrats API avant que le frontend ne consomme les endpoints ;
- le frontend peut utiliser des données simulées uniquement si le contrat API est validé et suivi dans le sprint backlog ;
- la testeuse définit les cas de recette avant la fin du développement pour éviter une validation tardive ;
- le DevOps vérifie à chaque sprint que l'incrément fonctionne dans Docker, pas seulement en environnement local ;
- l'ingénieure cybersécurité valide les règles de détection, les contrôles d'accès et les limites des scénarios offensifs ;
- le Product Owner décide de la valeur et de l'acceptation, mais ne modifie pas seul la capacité engagée pendant le sprint ;
- le Scrum Master protège le sprint contre les ajouts non arbitrés ;
- le chef de projet suit les risques, jalons et livrables sans transformer le daily scrum en reporting hiérarchique.

### Responsabilités RACI simplifiées

| Activité | Responsable | Appui | Validation |
|---|---|---|---|
| Priorisation backlog | Ada Lovelace | Alan Turing, Grace Hopper | Ada Lovelace |
| Animation Scrum | Grace Hopper | Alan Turing | Grace Hopper |
| Suivi planning et jalons | Alan Turing | Grace Hopper, Ada Lovelace | Alan Turing |
| API et modèles backend | Barbara Liskov | Ken Thompson | Margaret Hamilton |
| Ingestion, workers et détection | Ken Thompson | Barbara Liskov, Radia Perlman | Margaret Hamilton |
| Interface web | Tim Berners-Lee | Barbara Liskov, Ken Thompson | Ada Lovelace |
| Tests et recette | Margaret Hamilton | Toute l'équipe de développement | Ada Lovelace |
| Lab Docker et configuration | Linus Torvalds | Ken Thompson | Margaret Hamilton |
| Sécurité et scénarios cyber | Radia Perlman | Ken Thompson, Linus Torvalds | Ada Lovelace |
| Documentation de lancement | Linus Torvalds | Margaret Hamilton, Alan Turing | Alan Turing |

## 12. Jalons projet

| Jalon | Description | Preuve attendue |
|---|---|---|
| J1 | Cadrage validé | Feuille de cadrage, gestion de projet, cahier des charges, architecture |
| J2 | Socle technique opérationnel | Application démarrée, auth minimale, endpoint santé |
| J3 | Collecte endpoint fonctionnelle | Heartbeat et events persistés |
| J4 | Découverte et actifs visibles | Actifs, ports ou services consultables |
| J5 | Détection et alertes opérationnelles | Alerte générée depuis un scénario contrôlé |
| J6 | Corrélation visible | Groupe de corrélation consultable |
| J7 | Exports et audit prêts | CSV/JSON produits et journalisés |
| J8 | Démonstration finale stabilisée | Chaîne complète rejouable dans Docker |

## 13. Risques projet

| Risque | Impact | Mesure de maîtrise | Responsable | Métrique | Statut |
|---|---|---|---|---|---|
| Dérive du périmètre | Retard sur le MVP | Prioriser P1, reporter P3, arbitrer en sprint planning | Alan Turing | SP engagés vs capacité | Ouvert |
| Sous-estimation de la corrélation | Valeur SOC affaiblie | Commencer par IP source et fenêtre temporelle simple | Ken Thompson | Nombre corrélations visibles | Ouvert |
| Instabilité du lab Docker | Démonstration difficile à reproduire | Stabiliser Docker dès Sprint 1 et tester à chaque sprint | Linus Torvalds | Taux réussite démarrage lab | Mitigé |
| Complexité excessive du frontend | Perte de temps sur le visuel | Prioriser lisibilité analyste et parcours de preuve | Tim Berners-Lee | Temps parcours analyste | Ouvert |
| Sécurité insuffisante | Produit cyber peu crédible | Intégrer auth, `roles`, auth agent, validation payloads et audit dès le MVP | Radia Perlman | Nombre tests sécurité validés | Ouvert |
| Données de test non maîtrisées | Scénarios peu réalistes | Limiter aux IP lab, documenter, simuler sans destructivité | Margaret Hamilton | Nombre scénarios reproductibles | Mitigé |
| Documentation tardive | Produit difficile à relancer | Mettre à jour la documentation dans la Definition of Done |

## 14. Indicateurs de suivi Scrum

### Tableau de bord de vélocité

| Sprint | SP planifiés | SP terminés | Vélocité | Taux réussite |
|---|---|---|---|---|
| Sprint 1 | 18 | 16 | 16 | 89 % |
| Sprint 2 | 22 | 20 | 20 | 91 % |
| Sprint 3 | 24 | 22 | 22 | 92 % |
| Sprint 4 | 26 | 24 | 24 | 92 % |
| Sprint 5 | 28 | 26 | 26 | 93 % |
| **Moyenne** | **24** | **22** | **22** | **91 %** |

### Indicateurs détaillés

| Indicateur | Usage | Cible |
|---|---|---|
| Vélocité par sprint | Mesurer la capacité réelle de l'équipe | 20-24 SP/sprint |
| Story points terminés / engagés | Détecter la surcharge ou la sous-estimation | > 90 % |
| Nombre de stories P1 terminées | Vérifier la couverture MVP | 100 % P1 done |
| Nombre de blockers ouverts | Suivre les obstacles critiques | 0 blocker en fin de sprint |
| Taux de stories respectant la Definition of Done | Suivre la qualité réelle des incréments | 100 % |
| Stabilité du lab Docker | Vérifier la reproductibilité de la démonstration | 100 % démarrage réussi |
| Nombre de preuves produites | Relier développement, validation et démonstration | 1 preuve par story |

## 15. Livrables de pilotage

- product backlog structuré ;
- sprint backlog à chaque sprint ;
- tableau d'avancement Scrum ;
- suivi des story points ;
- registre des risques ;
- compte rendu de sprint review ;
- actions issues des rétrospectives de sprint ;
- documentation de lancement et de validation.

## 16. Dépendances documentaires

- [Feuille de cadrage](../05_feuille_de_cadrage/rendu_principal.md)
- [Cahier des charges](../06_cahier_des_charges/rendu_principal.md)
- [Architecture](../08_architecture/rendu_principal.md)
- [Business plan](../04_business_plan/rendu_principal.md)

## 17. Conclusion

La gestion de projet de DevinciWatch repose sur Agile Scrum afin de maintenir une exécution itérative, mesurable et orientée valeur. Le découpage en epics, features, user stories et tasks permet de relier directement le pilotage projet aux exigences du cahier des charges et aux choix d'architecture.

Les cérémonies Scrum, les story points, la Definition of Ready et la Definition of Done doivent être utilisés comme des mécanismes de maîtrise : ils rendent l'avancement visible, limitent la dérive du périmètre et garantissent que chaque incrément produit une preuve exploitable.
