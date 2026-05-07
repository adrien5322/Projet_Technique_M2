# Cahier des charges - DevinciWatch

## 1. Objet du document

Le présent cahier des charges formalise les besoins, le périmètre, les contraintes, les exigences fonctionnelles et non fonctionnelles ainsi que les critères de validation du projet DevinciWatch.

Il a une fonction contractuelle au sein du projet : il transforme les orientations de cadrage en exigences vérifiables, suffisamment précises pour guider le développement et suffisamment lisibles pour être défendues lors d'une revue projet. Il constitue également une base de dialogue entre les dimensions produit, projet et technique.

Ce document s'appuie sur :

- le [kick-off projet (01)](../01_documents_pedagogiques/kickoff/KICKOFF.md) ;
- l'[étude de marché (02)](../02_etude_de_marche/rendu_principal.md) ;
- le [business model (03)](../03_business_model/rendu_principal.md) ;
- le [business plan (04)](../04_business_plan/rendu_principal.md) ;
- la [feuille de cadrage (05)](../05_feuille_de_cadrage/rendu_principal.md) ;
- la [gestion de projet (07)](../07_gestion_de_projet/rendu_principal.md) ;
- l'[architecture produit retenue (08)](../08_architecture/rendu_principal.md).

### 1.1. Contexte quantifié (mai 2026)

Les données collectées valident les exigences du cahier des charges :
- **1 587 vulnérabilités connues et exploitées** (CISA KEV) → Exigence de couverture étendue
- **317 cas de ransomware identifiés** (20 % des KEV) → Exigence de détection proactive obligatoire
- **Score d'intensité 1 114,8** (Élevé) → Exigence de performance < 5 min détection
- **30 CVEs récents 2026** (7 Critiques, 6 Élevés) → Exigence de support CVSS v3.1 complet

Ces chiffres justifient le périmètre MVP et les fonctionnalités demandées.

## 2. Fiche documentaire

| Élément | Valeur |
|---|---|
| Projet | DevinciWatch |
| Document | Cahier des charges fonctionnel et technique |
| Version | 1.2 |
| Statut | Version détaillée du cahier des charges MVP |
| Périmètre | Produit MVP démontrable en environnement Docker |
| Public visé | Équipe projet, parties prenantes, contributeurs techniques, responsables de validation |
| Document précédent | [Gestion de projet (07)](../07_gestion_de_projet/rendu_principal.md) |
| Document suivant | [Architecture produit (08)](../08_architecture/rendu_principal.md) |

### Historique des versions

| Version | Objet | Statut |
|---|---|---|
| 1.0 | Formalisation initiale du périmètre, des exigences et des critères d'acceptation | Référence initiale |
| 1.1 | Enrichissement professionnel : exigences numérotées, sécurité, données, recette et traçabilité | Version consolidée |
| 1.2 | Précision des règles métier, contrats API, permissions, formats de données, critères mesurables et scénarios de recette | Version détaillée MVP |

## 3. Résumé exécutif

DevinciWatch est une solution de cybersurveillance réseau orientée SOC. Le produit vise à superviser un environnement de démonstration, collecter de la télémétrie depuis un endpoint, identifier des actifs, détecter des comportements suspects, corréler des signaux répétés, produire des alertes et générer des preuves exploitables sous forme d'historique, de journaux et d'exports.

Le cahier des charges retient une logique de MVP démontrable. L'objectif n'est pas de reproduire toute la complexité d'un SIEM enterprise, mais de prouver une chaîne fonctionnelle complète : observation réseau, ingestion, persistance, détection, corrélation, visualisation, audit et export de preuve.

La réussite du produit sera évaluée sur sa capacité à être lancé dans un lab Docker reproductible, à produire des résultats observables et à expliquer clairement les choix techniques réalisés.

## 4. Contexte et problématique

Le projet répond à deux niveaux d'attente :

- un besoin de démonstration produit, défini par le périmètre MVP et les critères de validation ;
- un besoin de valorisation produit, défini par les études réalisées, le positionnement retenu et l'opportunité identifiée sur le marché.

Les organisations ciblées doivent pouvoir :

- identifier les équipements présents sur leur réseau ;
- observer le trafic et les événements pertinents ;
- détecter des comportements suspects ;
- comprendre la répétition ou la corrélation d'attaques ;
- générer des alertes actionnables ;
- produire des preuves exploitables via journalisation, historique et exports.

La problématique peut être formulée ainsi : comment produire une visibilité cyber suffisamment riche pour être utile, tout en conservant une architecture simple, testable et compatible avec un environnement de démonstration contrôlé ?

## 5. Objectifs du produit

### Objectif général

Concevoir une application web de supervision cyber réseau capable de démontrer une chaîne SOC minimale, depuis la collecte endpoint jusqu'à la production de preuves exportables.

### Objectifs opérationnels

| ID | Objectif | Résultat attendu |
|---|---|---|
| OBJ-001 | Collecter de la télémétrie depuis un endpoint supervisé | `heartbeat` et `events` reçus, persistés et consultables |
| OBJ-002 | Découvrir le périmètre réseau observable | Actifs, ports et services identifiés dans le lab |
| OBJ-003 | Détecter des comportements suspects | Alertes générées à partir de règles simples |
| OBJ-004 | Corréler des signaux répétés | Regroupement d'événements liés à une IP, une cible ou une fenêtre temporelle |
| OBJ-005 | Restituer l'information à un analyste | Dashboard, vues d'alertes, actifs, événements et corrélations |
| OBJ-006 | Produire une preuve exploitable | Export CSV ou JSON généré pendant la démonstration |
| OBJ-007 | Soutenir une démonstration reproductible | Lab Docker en 3 conteneurs opérationnel |

## 6. Périmètre du MVP

### 6.1. Fonctions incluses

- authentification utilisateur ;
- gestion des `roles` ;
- collecte de `heartbeat` ;
- collecte d'événements ;
- découverte réseau ;
- scan IP ;
- détection de ports ouverts ;
- collecte d'informations de services ;
- observation de trafic réseau ;
- analyse de logs ;
- génération d'alertes ;
- corrélation de signaux répétés ;
- consultation d'actifs, d'événements et d'alertes ;
- historisation et journalisation ;
- métriques de supervision ;
- exports CSV et JSON ;
- affichage des IP attaquantes ;
- visualisation géographique des attaques en extension P3.

### 6.2. Fonctions hors périmètre initial

- réponse automatique avancée ;
- orchestration SOAR ;
- multi-tenant complet ;
- couverture SIEM exhaustive ;
- moteur de détection enterprise complexe ;
- déploiement distribué de production ;
- supervision de réseaux externes au lab Docker ;
- traitement de charges offensives destructrices ou malware réel.

Cette exclusion constitue un choix de maîtrise. Le périmètre initial se concentre sur les fonctionnalités qui démontrent le mieux la valeur du projet dans le temps disponible.

### 6.3. Règles de priorisation

| Priorité | Signification | Règle de décision |
|---|---|---|
| P1 | Indispensable MVP | Doit être livré pour considérer la chaîne produit conforme |
| P2 | Fortement souhaitable | Peut être livré si les fonctions P1 sont stables, sans bloquer la conformité MVP |
| P3 | Extension | Peut être reporté sans remettre en cause la conformité MVP |

La corrélation minimale par IP source est considérée comme P1, car elle matérialise la valeur de DevinciWatch au-delà d'une simple liste d'alertes. Les corrélations temporelles avancées, l'enrichissement géographique et l'export XML restent P2 ou P3 selon leur apport démonstratif.

## 7. Parties prenantes et utilisateurs

### 7.1. Parties prenantes

| Partie prenante | Rôle dans le projet | Attentes principales |
|---|---|---|
| Équipe projet | Conception, développement, documentation et démonstration | Périmètre clair, architecture défendable, livrables cohérents |
| Responsables de validation | Évaluation de la conformité du produit aux exigences | Traçabilité, cohérence, résultats observables |
| Parties prenantes métier | Appréciation de la valeur opérationnelle | Démonstration fluide, preuves exploitables, lisibilité produit |
| Futurs utilisateurs métier | Référence de valorisation produit | Lisibilité, simplicité, valeur opérationnelle |

### 7.2. Utilisateurs cibles

| Profil | Description | Besoins principaux |
|---|---|---|
| Administrateur | Utilisateur responsable de la configuration minimale et des accès | Authentifier, gérer les `roles`, consulter l'état du système |
| Analyste | Utilisateur chargé de l'investigation et de la qualification des alertes | Voir les actifs, événements, alertes, corrélations et exports |
| Responsable validation | Utilisateur observant les scénarios de recette | Comprendre la chaîne fonctionnelle et vérifier les preuves |

### 7.3. Alignement avec l'équipe projet

Le cahier des charges est exploité par l'équipe définie dans la [gestion de projet (07)](../07_gestion_de_projet/rendu_principal.md). Les responsabilités de validation sont réparties ainsi :

| Rôle projet | Contribution au cahier des charges |
|---|---|
| Product Owner | Valide la priorité, la valeur produit et l'acceptation des exigences |
| Scrum Master | Vérifie que les exigences sont prêtes à être intégrées au backlog |
| Chef de projet | Suit la cohérence des exigences avec les jalons et les livrables |
| Développeurs backend | Traduisent les exigences en modèles, API, services et traitements |
| Développeur frontend | Traduit les exigences en parcours utilisateur et vues analyste |
| Testeuse / QA | Convertit les critères d'acceptation en scénarios de recette |
| DevOps | Vérifie la faisabilité Docker, la configuration et la reproductibilité |
| Ingénieure cybersécurité | Vérifie les exigences de sécurité, de détection et de scénarios contrôlés |

### 7.4. Matrice des permissions MVP

| Fonction | `admin` | `analyst` | Non authentifié | Agent authentifié |
|---|---:|---:|---:|---:|
| Se connecter à l'interface | Oui | Oui | Non | Non |
| Consulter le dashboard | Oui | Oui | Non | Non |
| Consulter actifs, événements, alertes | Oui | Oui | Non | Non |
| Qualifier une alerte ou changer son statut | Oui | Oui | Non | Non |
| Consulter les corrélations | Oui | Oui | Non | Non |
| Générer un export CSV/JSON | Oui | Oui | Non | Non |
| Consulter les journaux d'audit | Oui | Non | Non | Non |
| Administrer les utilisateurs ou `roles` | Oui | Non | Non | Non |
| Envoyer un `heartbeat` | Non | Non | Non | Oui |
| Envoyer des `events` | Non | Non | Non | Oui |

Toute route non explicitement publique doit refuser les accès non authentifiés. Toute route agent doit être séparée des routes utilisateur et refuser une requête sans secret ou clé agent valide.

## 8. Glossaire

| Terme | Définition |
|---|---|
| Actif | Équipement, hôte ou ressource réseau observable par le système |
| Alerte | Signal produit par une règle de détection ou par une corrélation |
| Audit log | Journal retraçant une action sensible ou significative |
| Corrélation | Regroupement de plusieurs événements liés par une IP, une cible, une fenêtre temporelle ou un comportement |
| Endpoint | Hôte supervisé qui produit de la télémétrie |
| Event | Événement technique remonté par l'endpoint |
| Heartbeat | Signal périodique indiquant qu'un endpoint est actif |
| MVP | Minimum Viable Product, version minimale démontrable du produit |
| SIEM | Security Information and Event Management |
| SOC | Security Operations Center |
| `serveur-soc` | Conteneur central embarquant interface web, API, base, Redis et worker pour le MVP |
| `serveur-endpoint` | Conteneur représentant l'hôte supervisé |
| `serveur-attacker` | Conteneur générant des scénarios de test contrôlés |

## 9. Hypothèses, contraintes et dépendances

### 9.1. Hypothèses

- Le projet est réalisé dans un cadre de validation produit avec une démonstration attendue.
- Le MVP doit être suffisamment complet pour montrer une chaîne fonctionnelle de supervision et de preuve.
- L'environnement Docker constitue le périmètre officiel de démonstration.
- Les scénarios offensifs restent contrôlés, non destructeurs et limités au réseau de lab.
- Les exports CSV et JSON sont prioritaires ; XML reste une extension P3 non bloquante pour le MVP.

### 9.2. Contraintes

- backend Python / FastAPI imposé ;
- frontend web cohérent avec la démonstration ;
- dépôt structuré et documenté ;
- architecture défendable techniquement ;
- lab Docker reproductible ;
- livrables exploitables en revue projet ;
- cohérence obligatoire avec l'[architecture produit (08)](../08_architecture/rendu_principal.md).

### 9.3. Dépendances documentaires

- [Kick-off projet (01)](../01_documents_pedagogiques/kickoff/KICKOFF.md)
- [Étude de marché (02)](../02_etude_de_marche/rendu_principal.md)
- [Business model (03)](../03_business_model/rendu_principal.md)
- [Business plan (04)](../04_business_plan/rendu_principal.md)
- [Feuille de cadrage (05)](../05_feuille_de_cadrage/rendu_principal.md)
- [Gestion de projet (06)](../07_gestion_de_projet/rendu_principal.md)
- [Architecture produit (08)](../08_architecture/rendu_principal.md)

## 10. Exigences fonctionnelles

Les exigences fonctionnelles décrivent ce que le produit doit faire. Elles sont numérotées afin de faciliter la traçabilité avec les critères d'acceptation et les scénarios de recette.

### 10.1. Règles métier MVP

| ID | Règle | Description | Critère de vérification |
|---|---|---|---|
| RM-001 | Authentification utilisateur | Un utilisateur doit disposer d'un identifiant, d'un mot de passe stocké sous forme hachée et d'un `role`. | Un accès sans session valide est refusé. |
| RM-002 | Authentification agent | Le `serveur-endpoint` doit présenter une clé ou un secret agent pour envoyer de la télémétrie. | Une requête agent sans secret valide retourne une erreur contrôlée. |
| RM-003 | Scan borné | Toute découverte réseau doit être limitée au réseau Docker de lab configuré. | Un scan hors plage autorisée est refusé ou ignoré. |
| RM-004 | Détection scan de ports | Au moins trois ports observés sur une même cible pendant un scénario contrôlé doivent pouvoir produire un événement suspect ou une alerte. | Le scénario de scan contrôlé génère une alerte. |
| RM-005 | Détection répétition | Au moins trois événements similaires issus d'une même IP source dans une fenêtre configurable doivent être corrélés. | Un groupe de corrélation est créé. |
| RM-006 | Fenêtre de corrélation MVP | La fenêtre de corrélation par défaut est de 10 minutes pour le MVP. | Les événements hors fenêtre ne sont pas regroupés dans le même groupe. |
| RM-007 | Statuts d'alerte | Une alerte MVP doit au minimum supporter `new`, `in_review` et `closed`. | Le statut est visible et modifiable par un utilisateur autorisé. |
| RM-008 | Preuve exportable | Un export doit contenir les données du scénario, une date de génération, un format et un identifiant de demande. | Le fichier CSV/JSON permet de retrouver le scénario joué. |
| RM-009 | Audit obligatoire | Connexion, export, changement de statut d'alerte et action d'administration doivent produire une entrée d'audit. | Chaque action sensible apparaît dans `audit_logs`. |
| RM-010 | Scénarios offensifs contrôlés | Le `serveur-attacker` ne doit générer que des comportements non destructeurs et prévisibles. | Le scénario est documenté et limité au réseau Docker. |

### 10.2. Authentification et contrôle d'accès

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-AUTH-001 | Le système doit permettre l'authentification sécurisée des utilisateurs. | P1 | Un utilisateur valide accède au dashboard après connexion. |
| F-AUTH-002 | Le système doit distinguer les `roles` `admin` et `analyst`. | P1 | Les permissions diffèrent selon le `role`. |
| F-AUTH-003 | Le système doit restreindre les actions sensibles selon le `role`. | P1 | Un analyste ne peut pas exécuter une action réservée à l'administration. |

### 10.3. Collecte endpoint

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-TEL-001 | Le `serveur-endpoint` doit émettre un `heartbeat`. | P1 | Le dernier `heartbeat` est visible côté `serveur-soc`. |
| F-TEL-002 | Le `serveur-endpoint` doit remonter des événements. | P1 | Des `events` sont persistés et consultables. |
| F-TEL-003 | Le système doit collecter des journaux utiles à la détection. | P2 | Au moins une entrée de log est transformée en événement exploitable. |
| F-TEL-004 | Le système doit remonter des indicateurs de comportements suspects. | P1 | Un scénario contrôlé produit un événement suspect. |

### 10.4. Découverte réseau et actifs

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-DISC-001 | Le système doit scanner une plage IP définie dans le lab. | P1 | Une plage IP configurée est analysée. |
| F-DISC-002 | Le système doit identifier des équipements observables. | P1 | Au moins un actif est créé ou mis à jour. |
| F-DISC-003 | Le système doit détecter les ports ouverts quand ils sont observables. | P1 | Les ports détectés sont associés à un actif. |
| F-DISC-004 | Le système doit récupérer des informations de services quand elles sont disponibles. | P2 | Les services observés apparaissent dans le détail d'un actif. |
| F-ASSET-001 | Le système doit maintenir un inventaire d'actifs. | P1 | L'interface affiche les actifs connus. |

### 10.5. Détection et alerting

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-ALERT-001 | Le système doit produire des alertes issues de règles simples. | P1 | Un événement suspect génère une alerte. |
| F-ALERT-002 | Le système doit proposer une vue de liste des alertes. | P1 | Les alertes sont consultables dans l'interface. |
| F-ALERT-003 | Le système doit proposer une vue de détail d'une alerte. | P1 | Une alerte affiche son contexte, sa source et son horodatage. |
| F-ALERT-004 | Le système doit gérer un cycle de vie minimal des alertes. | P1 | Une alerte peut changer de statut ou être qualifiée. |

### 10.6. Corrélation

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-COR-001 | Le système doit corréler plusieurs événements provenant d'une même IP. | P1 | Plusieurs événements sont regroupés dans une corrélation. |
| F-COR-002 | Le système doit corréler des répétitions dans une fenêtre temporelle. | P2 | Une répétition produit un groupe de corrélation. |
| F-COR-003 | Le système doit associer une corrélation à une ou plusieurs alertes. | P2 | Une alerte enrichie référence un groupe de corrélation. |
| F-COR-004 | Le système doit afficher les corrélations dans l'interface. | P1 | L'analyste consulte les corrélations détectées. |

### 10.7. Interface web

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-UI-001 | L'interface doit proposer un dashboard de synthèse. | P1 | Le dashboard affiche des métriques utiles à la démonstration. |
| F-UI-002 | L'interface doit permettre la consultation des actifs. | P1 | La liste et le détail des actifs sont accessibles. |
| F-UI-003 | L'interface doit permettre la consultation des événements. | P1 | Les événements collectés sont visibles. |
| F-UI-004 | L'interface doit permettre la consultation des alertes. | P1 | Les alertes générées sont visibles. |
| F-UI-005 | L'interface doit permettre la consultation des journaux d'audit. | P2 | Les actions sensibles journalisées sont consultables. |
| F-UI-006 | L'interface peut afficher une carte géographique des attaques. | P3 | Une vue géographique apparaît si l'enrichissement est réalisé. |

### 10.8. Reporting et exports

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-EXP-001 | Le système doit produire un export CSV. | P1 | Un fichier CSV est généré avec les colonnes obligatoires définies en section 13.2. |
| F-EXP-002 | Le système doit produire un export JSON. | P1 | Un fichier JSON est généré avec les métadonnées obligatoires définies en section 13.2. |
| F-EXP-003 | Le système peut produire un export XML en extension P3. | P3 | Un export XML est disponible sans remplacer CSV/JSON. |
| F-EXP-004 | Les exports doivent pouvoir servir de preuve opérationnelle. | P1 | L'export contient des données cohérentes avec le scénario joué. |

### 10.9. Audit et journalisation

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| F-AUD-001 | Le système doit journaliser les authentifications. | P1 | Une connexion génère une entrée d'audit. |
| F-AUD-002 | Le système doit journaliser les exports. | P1 | Un export génère une entrée d'audit. |
| F-AUD-003 | Le système doit journaliser les actions sensibles d'administration. | P1 | Une action sensible est traçable. |
| F-AUD-004 | Les journaux doivent être consultables par un profil autorisé. | P2 | Un utilisateur autorisé consulte les logs d'audit. |

## 11. Exigences non fonctionnelles

| ID | Catégorie | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|---|
| NF-QUAL-001 | Qualité | Le code doit être structuré par domaines fonctionnels. | P1 | La structure suit les modules définis dans l'architecture. |
| NF-QUAL-002 | Qualité | Les données d'entrée doivent être validées. | P1 | Un payload invalide est rejeté proprement. |
| NF-PERF-001 | Performance | Les parcours de démonstration doivent rester fluides. | P1 | Le dashboard et les vues principales répondent en moins de 2 secondes sur un jeu de données MVP. |
| NF-PERF-002 | Performance | Les traitements lourds doivent être différés. | P2 | Les tâches de détection ou d'export peuvent passer par Redis/Celery. |
| NF-PERF-003 | Performance | Un export CSV ou JSON doit rester compatible avec la démonstration. | P1 | Un export de 100 lignes est généré en moins de 5 secondes. |
| NF-OBS-001 | Observabilité | Le système doit exposer un endpoint de santé. | P1 | `GET /health` retourne un statut API et worker consultable. |
| NF-OBS-002 | Observabilité | Le système doit produire des logs applicatifs exploitables. | P1 | Les erreurs, ingestions, exports et actions sensibles sont visibles dans les logs. |
| NF-DEP-001 | Déployabilité | Le projet doit être lançable dans un environnement Docker reproductible. | P1 | Les trois conteneurs démarrent avec une commande documentée et rejoignent le même réseau Docker. |
| NF-DEP-002 | Déployabilité | Le lab doit être vérifiable après démarrage. | P1 | Les conteneurs `serveur-soc`, `serveur-endpoint` et `serveur-attacker` sont actifs et `GET /health` répond. |
| NF-MAINT-001 | Maintenabilité | Les conventions de nommage doivent rester cohérentes. | P1 | Les noms de modules, entités et conteneurs sont homogènes. |
| NF-TEST-001 | Testabilité | Chaque exigence P1 doit être reliée à au moins un scénario de recette. | P1 | La matrice de traçabilité couvre les exigences P1. |

## 12. Exigences de sécurité

Les exigences de sécurité s'inspirent de bonnes pratiques applicatives telles que l'OWASP ASVS, adaptées au niveau MVP du projet.

| ID | Exigence | Priorité | Critère d'acceptation |
|---|---|---|---|
| SEC-001 | L'accès à l'interface doit nécessiter une authentification. | P1 | Une page protégée n'est pas accessible sans session valide. |
| SEC-002 | Les actions sensibles doivent être contrôlées par `role`. | P1 | Un `analyst` ne peut pas effectuer une action réservée à `admin`. |
| SEC-003 | Les routes d'ingestion agent doivent être séparées des routes utilisateur. | P1 | Les endpoints agent sont identifiables et isolés fonctionnellement. |
| SEC-004 | Le `serveur-endpoint` doit s'authentifier auprès de l'API. | P1 | Une requête agent non autorisée est refusée. |
| SEC-005 | Les payloads entrants doivent être validés strictement. | P1 | Un payload mal formé produit une erreur contrôlée. |
| SEC-006 | Les secrets ne doivent pas être exposés dans le dépôt. | P1 | Aucun secret réel n'est versionné. |
| SEC-007 | Les actions sensibles doivent produire une entrée d'audit. | P1 | Les connexions, exports et actions d'administration sont tracés. |
| SEC-008 | Les scénarios offensifs doivent rester bornés au lab Docker. | P1 | Aucun test ne cible un réseau externe au lab. |
| SEC-009 | Les exports doivent être accessibles uniquement à des utilisateurs autorisés. | P1 | Un utilisateur non autorisé ne peut pas générer ou consulter un export. |

## 13. Données manipulées

| Donnée | Description | Source | Usage | Sensibilité |
|---|---|---|---|---|
| `users` | Comptes utilisateurs de l'application | Interface / initialisation | Authentification et contrôle d'accès | Élevée |
| `roles` | Rôles applicatifs (`admin`, `analyst`) | Configuration applicative | Autorisations | Élevée |
| `assets` | Actifs réseau observés | Découverte réseau / événements | Inventaire et analyse | Moyenne |
| `events` | Événements remontés par endpoint | `serveur-endpoint` | Détection, historique, corrélation | Moyenne |
| `network_findings` | Résultats de scan et observation réseau | Module découverte | Actifs, ports, services | Moyenne |
| `alerts` | Alertes générées par règles ou corrélations | Backend / worker | Investigation analyste | Moyenne |
| `correlation_groups` | Groupes d'événements liés | Worker de corrélation | Enrichissement des alertes | Moyenne |
| `attacker_profiles` | Profils d'IP ou sources attaquantes | Corrélation / enrichissement | Analyse et visualisation | Moyenne |
| `audit_logs` | Traces d'actions sensibles | API | Traçabilité et preuve | Élevée |
| `exports` | Fichiers ou métadonnées d'exports | Module reporting | Preuve et reporting | Moyenne |

### 13.1. Champs minimaux attendus

| Entité | Champs minimaux MVP |
|---|---|
| `users` | `id`, `username`, `password_hash`, `role`, `created_at`, `last_login_at`, `is_active` |
| `assets` | `id`, `ip_address`, `hostname`, `first_seen_at`, `last_seen_at`, `status` |
| `events` | `id`, `source_ip`, `target_ip`, `event_type`, `severity`, `message`, `raw_payload`, `created_at`, `asset_id` |
| `network_findings` | `id`, `asset_id`, `ip_address`, `port`, `protocol`, `service_name`, `observed_at` |
| `alerts` | `id`, `title`, `severity`, `status`, `source_ip`, `target_ip`, `description`, `created_at`, `updated_at` |
| `correlation_groups` | `id`, `correlation_type`, `source_ip`, `window_start`, `window_end`, `event_count`, `created_at` |
| `attacker_profiles` | `id`, `source_ip`, `event_count`, `last_seen_at`, `geo_label`, `risk_level` |
| `audit_logs` | `id`, `user_id`, `role`, `action`, `target_type`, `target_id`, `result`, `created_at` |
| `exports` | `id`, `format`, `requested_by`, `scope`, `file_path`, `created_at`, `row_count` |

### 13.2. Formats de données MVP

#### `heartbeat`

```json
{
  "agent_id": "serveur-endpoint",
  "hostname": "serveur-endpoint",
  "ip_address": "172.20.0.3",
  "status": "alive",
  "sent_at": "2026-05-03T10:00:00Z"
}
```

#### `event`

```json
{
  "agent_id": "serveur-endpoint",
  "source_ip": "172.20.0.4",
  "target_ip": "172.20.0.3",
  "event_type": "port_scan",
  "severity": "medium",
  "message": "Scan de ports contrôlé détecté",
  "observed_at": "2026-05-03T10:01:00Z"
}
```

#### Export CSV minimal

Colonnes obligatoires : `export_id`, `generated_at`, `type`, `id`, `source_ip`, `target_ip`, `severity`, `status`, `created_at`, `description`.

#### Export JSON minimal

```json
{
  "export_id": "exp_001",
  "generated_at": "2026-05-03T10:05:00Z",
  "format": "json",
  "scope": "alerts",
  "items": []
}
```

## 14. Interfaces, API et flux

### 14.1. Flux principaux

| Flux | Source | Destination | Description |
|---|---|---|---|
| FLUX-001 | `serveur-endpoint` | `serveur-soc` | Envoi de `heartbeat` |
| FLUX-002 | `serveur-endpoint` | `serveur-soc` | Envoi d'événements et observations |
| FLUX-003 | Interface web | API FastAPI | Consultation des actifs, événements, alertes, exports |
| FLUX-004 | API FastAPI | PostgreSQL | Persistance et lecture des données |
| FLUX-005 | API FastAPI | Redis / Celery | Planification de traitements différés |
| FLUX-006 | Celery Worker | PostgreSQL | Création ou mise à jour d'alertes, corrélations et exports |

### 14.2. Contrat API MVP

| Méthode | Endpoint MVP | Usage | Accès | Priorité | Réponse attendue |
|---|---|---|---|---|---|
| `POST` | `/auth/login` | Authentification utilisateur | Public | P1 | Token/session et informations utilisateur |
| `GET` | `/auth/me` | Informations utilisateur courant | `admin`, `analyst` | P1 | `id`, `username`, `role` |
| `GET` | `/health` | Santé applicative | Public sans donnée sensible | P1 | État API, base, worker |
| `POST` | `/telemetry/heartbeat` | Réception d'un `heartbeat` endpoint | Agent authentifié | P1 | Accusé de réception et horodatage |
| `POST` | `/telemetry/events` | Réception d'événements endpoint | Agent authentifié | P1 | Nombre d'événements acceptés et rejetés |
| `GET` | `/assets` | Liste des actifs | `admin`, `analyst` | P1 | Liste paginable d'actifs |
| `GET` | `/assets/{id}` | Détail d'un actif | `admin`, `analyst` | P1 | Actif, ports, dernière observation |
| `GET` | `/events` | Liste des événements | `admin`, `analyst` | P1 | Liste filtrable par IP, type, sévérité |
| `GET` | `/alerts` | Liste des alertes | `admin`, `analyst` | P1 | Liste filtrable par statut et sévérité |
| `GET` | `/alerts/{id}` | Détail d'une alerte | `admin`, `analyst` | P1 | Alerte, événements liés, corrélation éventuelle |
| `PATCH` | `/alerts/{id}` | Qualification ou changement de statut | `admin`, `analyst` | P2 | Statut mis à jour et entrée d'audit |
| `GET` | `/correlations` | Liste des corrélations | `admin`, `analyst` | P1 | Groupes de corrélation par IP source |
| `POST` | `/exports` | Génération d'un export CSV/JSON | `admin`, `analyst` | P1 | Métadonnées d'export et chemin/fichier généré |
| `GET` | `/audit-logs` | Consultation des journaux d'audit | `admin` | P2 | Liste des actions sensibles |

Les noms d'endpoints peuvent évoluer pendant la conception technique uniquement si la couverture fonctionnelle, les accès, les priorités et les critères d'acceptation restent équivalents.

## 15. Architecture de démonstration retenue

L'environnement de démonstration doit comporter :

- `serveur-soc` ;
- `serveur-endpoint` ;
- `serveur-attacker`.

Le `serveur-soc` embarque pour le MVP :

- frontend web ;
- backend FastAPI ;
- PostgreSQL ;
- Redis ;
- Celery.

Cette architecture compacte est retenue pour faciliter le lancement, la validation et la reproductibilité de la démonstration. Elle ne remet pas en cause la séparation logique entre interface, API, base de données, file de tâches et worker.

### 15.1. Conditions minimales de lancement

| Élément | Condition attendue |
|---|---|
| Réseau Docker | Un réseau dédié au lab, par exemple `devinciwatch_net` |
| `serveur-soc` | Interface web, API, PostgreSQL, Redis et worker disponibles |
| `serveur-endpoint` | Agent démarré, authentifié et capable d'envoyer un `heartbeat` |
| `serveur-attacker` | Scénario contrôlé disponible sans charge destructive |
| Santé applicative | `GET /health` vérifie au minimum API, base de données et worker |
| Données de démonstration | Un compte `admin`, un compte `analyst` et un scénario de test reproductible |

### 15.2. Limites de sécurité du lab

- les scans doivent rester limités au réseau Docker de démonstration ;
- aucun malware réel, exploit destructeur ou trafic visant un réseau externe ne doit être intégré ;
- les secrets utilisés dans le lab doivent être des valeurs de démonstration et ne doivent pas être exposés comme secrets réels ;
- toute capacité réseau particulière du `serveur-endpoint` doit être documentée et justifiée ;
- le `serveur-attacker` sert uniquement à générer des signaux observables et contrôlés.

## 16. Scénarios de recette et critères d'acceptation

### 16.1. Critères d'acceptation globaux

Le produit sera considéré comme conforme si les points suivants sont démontrés :

1. un endpoint remonte correctement `heartbeat` et `events` ;
2. le système détecte des actifs, ports ou services ;
3. des comportements suspects sont observés depuis le `serveur-endpoint` ;
4. des alertes sont générées ;
5. au moins une logique de corrélation fonctionne ;
6. l'interface permet la consultation des données clés ;
7. l'historique et la journalisation sont visibles ;
8. un export exploitable est produit ;
9. la démonstration fonctionne dans le lab Docker prévu.

### 16.2. Scénarios de recette

| ID | Scénario | Préconditions | Étapes | Résultat attendu | Preuve attendue |
|---|---|---|---|---|---|
| REC-001 | Connexion utilisateur | `serveur-soc` démarré, compte `admin` et compte `analyst` créés | Se connecter avec un compte valide puis tenter une page protégée sans session | Connexion valide acceptée, accès sans session refusé | Capture dashboard, réponse de refus, entrée `audit_logs` |
| REC-002 | Contrôle des permissions | Compte `analyst` connecté | Tenter d'accéder aux journaux d'audit ou à une action réservée `admin` | Accès refusé pour `analyst`, accès autorisé pour `admin` | Réponse API ou capture interface |
| REC-003 | Heartbeat endpoint | `serveur-endpoint` démarré avec secret agent valide | Envoyer le payload `heartbeat` minimal | Heartbeat reçu, horodaté, persisté et visible côté `serveur-soc` | Vue interface, ligne PostgreSQL ou log applicatif |
| REC-004 | Rejet agent non autorisé | Secret agent absent ou invalide | Envoyer un `heartbeat` ou un `event` sans secret valide | Requête refusée proprement, aucune donnée persistée | Réponse d'erreur contrôlée et log applicatif |
| REC-005 | Découverte réseau bornée | Lab Docker actif sur réseau autorisé | Lancer ou observer un scan limité au réseau de lab | Actif, port ou service détecté sans sortir du réseau autorisé | Vue actif, résultat de scan, configuration Docker |
| REC-006 | Détection suspecte | `serveur-attacker` prêt, règle de scan activée | Générer un scan contrôlé vers `serveur-endpoint` | Événement suspect puis alerte créée | Vue alerte, événement source, log worker |
| REC-007 | Corrélation IP source | Au moins trois événements similaires depuis la même IP en moins de 10 minutes | Rejouer trois événements contrôlés | Groupe de corrélation créé avec `event_count >= 3` | Vue corrélation ou ligne `correlation_groups` |
| REC-008 | Cycle de vie alerte | Alerte existante, utilisateur autorisé connecté | Passer l'alerte de `new` à `in_review`, puis `closed` | Statut mis à jour et action auditée | Vue alerte et entrée `audit_logs` |
| REC-009 | Export preuve CSV/JSON | Alertes ou événements présents | Générer un export CSV puis JSON depuis l'interface ou l'API | Fichier généré avec métadonnées et données cohérentes | Fichier exporté et entrée `audit_logs` |
| REC-010 | Santé et reproductibilité Docker | Trois conteneurs démarrés | Vérifier les conteneurs, appeler `GET /health`, rejouer le scénario complet | API, base, worker et agent opérationnels | Sortie Docker, réponse `/health`, démonstration complète |
| REC-011 | Démonstration complète | REC-001 à REC-010 réalisables | Jouer collecte -> découverte -> détection -> corrélation -> alerte -> export | Chaîne complète visible et explicable | Captures, logs, export CSV/JSON, support de validation |

## 17. Priorisation

### Priorité 1 - indispensable

- authentification ;
- collecte endpoint ;
- découverte réseau minimale ;
- alertes ;
- corrélation minimale par IP source ;
- historique ;
- audit minimal ;
- export CSV et JSON ;
- démonstration Docker.

### Priorité 2 - fortement souhaitable

- corrélation par fenêtre temporelle et enrichissement avancé ;
- métriques SOC ;
- consultation des journaux d'audit ;
- visualisation des IP attaquantes.

### Priorité 3 - extension si temps disponible

- export XML ;
- enrichissement géographique ;
- corrélation plus poussée ;
- raffinements visuels supplémentaires.

## 18. Matrice de traçabilité

| Besoin initial | Exigences associées | Epic / stories Scrum | Recette | Preuve attendue |
|---|---|---|---|---|
| Sécuriser l'accès | F-AUTH-001, F-AUTH-002, F-AUTH-003, SEC-001, SEC-002 | EPIC-01 / US-01.1, US-01.2 | REC-001, REC-002 | Test connexion, refus d'accès, audit log |
| Collecter la télémétrie endpoint | F-TEL-001, F-TEL-002, SEC-004 | EPIC-02 / US-02.1, US-02.2, US-02.3 | REC-003, REC-004 | Heartbeat, event persisté, rejet agent invalide |
| Identifier les équipements réseau | F-DISC-001, F-DISC-002, F-ASSET-001 | EPIC-03 / US-03.1, US-03.2, US-03.3 | REC-005 | Vue actifs, résultat de scan, base PostgreSQL |
| Détecter des comportements suspects | F-ALERT-001, F-ALERT-002, F-ALERT-003 | EPIC-04 / US-04.1, US-04.2 | REC-006 | Vue alerte, événement source, log worker |
| Comprendre les répétitions | F-COR-001, F-COR-002, F-COR-004 | EPIC-05 / US-05.1, US-05.2, US-05.3 | REC-007 | Vue corrélation, groupe `correlation_groups` |
| Qualifier les alertes | F-ALERT-004, F-AUD-003 | EPIC-04 / US-04.2, US-04.3 | REC-008 | Statut alerte et audit log |
| Produire des preuves | F-EXP-001, F-EXP-002, F-EXP-004, F-AUD-002 | EPIC-07 / US-07.1, US-07.2, US-07.3 | REC-009 | Fichier CSV/JSON, métadonnées export, audit log |
| Démontrer le produit | NF-DEP-001, NF-DEP-002, SEC-008 | EPIC-08 / US-08.1, US-08.2, US-08.3 | REC-010, REC-011 | Lab Docker, `/health`, chaîne complète |

## 19. Livrables attendus

| Livrable | Description | Critère de validation |
|---|---|---|
| Application DevinciWatch MVP | Application web de supervision cyber | Chaîne fonctionnelle démontrable |
| Lab Docker | Environnement `serveur-soc`, `serveur-endpoint`, `serveur-attacker` | Démarrage reproductible |
| Documentation technique | Instructions et architecture | Cohérence avec les documents `07` et `08` |
| Exports de preuve | Fichiers CSV ou JSON | Exploitables en revue produit |
| Support de présentation | Support de présentation produit | Clair, structuré, défendable |
| Dépôt GitHub | Code, documentation et historique | Dépôt propre et traçable |

## 20. Références de cadrage

- [Kick-off projet (01)](../01_documents_pedagogiques/kickoff/KICKOFF.md)
- [Étude de marché (02)](../02_etude_de_marche/rendu_principal.md)
- [Business model (03)](../03_business_model/rendu_principal.md)
- [Business plan (04)](../04_business_plan/rendu_principal.md)
- [Feuille de cadrage (05)](../05_feuille_de_cadrage/rendu_principal.md)
- [Gestion de projet (06)](../07_gestion_de_projet/rendu_principal.md)
- [Architecture produit (08)](../08_architecture/rendu_principal.md)
- [OWASP ASVS](https://owasp.org/www-project-application-security-verification-standard/)
- [NIST Cybersecurity Framework](https://www.nist.gov/cyberframework)

## 21. Conclusion

Ce cahier des charges fixe un périmètre clair, vérifiable et cohérent avec le positionnement produit, la gestion de projet et l'architecture retenue. Il constitue la base opérationnelle du développement de DevinciWatch.

La version détaillée renforce la dimension professionnelle du document en introduisant des exigences numérotées, des critères d'acceptation, une matrice de permissions, des règles métier, des contrats API, des formats de données, une matrice de traçabilité, des scénarios de recette et des exigences de sécurité adaptées au contexte cyber. Elle permet ainsi de relier explicitement le besoin initial, la conception technique, la démonstration et les preuves attendues en validation produit.
