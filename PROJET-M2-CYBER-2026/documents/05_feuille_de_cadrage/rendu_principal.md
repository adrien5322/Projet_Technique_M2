# Feuille de cadrage - DevinciWatch

## 1. Identité du projet

- **Nom du projet** : DevinciWatch
- **Nature** : projet de cybersurveillance réseau orienté SOC
- **Finalité** : concevoir un produit démontrable de supervision, détection, corrélation et preuve

## 2. Contexte

Le projet s'inscrit dans un cadre de conception produit en cybersécurité avec des attendus techniques, méthodologiques et de valorisation. Il doit démontrer la capacité à transformer un besoin de supervision réseau en produit structuré, défendable et démontrable.

La feuille de cadrage joue ici un rôle de document-pivot. Elle traduit les enseignements issus de l'[étude de marché](../02_etude_de_marche/rendu_principal.md), du [business model](../03_business_model/rendu_principal.md) et du [business plan](../04_business_plan/rendu_principal.md) en décisions de périmètre, de priorisation et d'exécution. Elle permet également de préparer le passage vers le [cahier des charges](../06_cahier_des_charges/rendu_principal.md) et l'[architecture](../08_architecture/rendu_principal.md).

### 3.1. Validation par les données (mai 2026)

L'analyse de 1 638 enregistrements confirme le cadrage :
- **Score d'intensité 1 114,8** (Élevé) → Produit doit couvrir 1 587 vulnérabilités KEV + 30 CVEs 2026
- **317 cas de ransomware** (20 % des KEV) → Priorité sur détection et alertes automatiques
- **Top 5 fournisseurs critiques** (Microsoft 370, Apple 93, Cisco 89...) → Périmètre MVP doit supporter ces sources
- **30 CVEs récents 2026** (23 % Critique, 20 % Élevé) → Architecture doit traiter flux temps-réel < 5 min

## 3. Besoin principal

Mettre à disposition une solution capable de :

- superviser un environnement réseau ;
- identifier des actifs et des services ;
- observer le trafic et les journaux ;
- détecter et corréler des comportements suspects ;
- produire des alertes, des historiques et des exports ;
- fournir des éléments de preuve en démonstration.

## 4. Problème adressé

Les structures ciblées ont besoin de visibilité, de simplicité d'exploitation et de preuve, sans recourir à une plateforme trop lourde ou difficile à opérer. Le problème adressé n'est donc pas seulement l'absence d'information technique ; il concerne aussi la capacité à qualifier cette information, à la présenter clairement et à la transformer en éléments exploitables pour une décision ou une revue produit.

## 5. Objectifs projet

### Objectifs fonctionnels

- collecte endpoint ;
- découverte réseau ;
- alertes ;
- corrélation ;
- interface web ;
- métriques ;
- exports ;
- journalisation ;
- cartographie des attaques.

### Objectifs de validation

- démontrer une architecture cohérente ;
- produire un dépôt clair ;
- soutenir un raisonnement de conception ;
- présenter une solution techniquement et fonctionnellement maîtrisée.

## 6. Périmètre

### Inclus

- `serveur-soc`
- `serveur-endpoint`
- `serveur-attacker`
- lab Docker de démonstration
- backend FastAPI
- frontend intégré au serveur SOC pour le MVP

### Exclu du premier périmètre

- réponse automatique avancée ;
- architecture d'exploitation distribuée complète ;
- multi-tenant ;
- SIEM enterprise complet.

## 7. Utilisateurs cibles

- analyste SOC junior ou intermédiaire ;
- administrateur ;
- responsable de validation / référent produit.

## 8. Proposition de valeur projet

DevinciWatch propose une supervision cyber réseau pragmatique, démontrable et exploitable, combinant visibilité, alertes, corrélation, historique et preuve dans une architecture simple à expliquer et à mettre en œuvre.

La valeur du projet repose sur une articulation entre rigueur technique et lisibilité opérationnelle : l'utilisateur doit pouvoir comprendre ce qui est observé, pourquoi une alerte est produite, comment les événements sont reliés entre eux et quelles preuves peuvent être exportées.

## 9. Architecture de référence retenue

Le produit s'appuie sur :

- Python ;
- FastAPI ;
- PostgreSQL ;
- Redis ;
- Celery ;
- lab Docker de démonstration en 3 conteneurs.

Référence : [Architecture produit (08)](../08_architecture/rendu_principal.md)

## 10. Livrables attendus

- produit fonctionnel démontrable ;
- dépôt GitHub structuré ;
- documentation claire ;
- exports de preuve ;
- support de présentation ;
- démonstration de validation.

## 11. Critères de succès

Le projet sera jugé réussi si :

- la chaîne complète collecte -> détection -> corrélation -> alerte -> preuve fonctionne ;
- l'interface web permet une lecture claire de la situation ;
- les scénarios de démonstration sont reproductibles ;
- le dépôt permet de comprendre et défendre l'architecture ;
- les livrables sont cohérents entre eux.

## 12. Risques principaux

Les risques ci-dessous consolident les enseignements de l'[étude de marché](../02_etude_de_marche/rendu_principal.md), du [business model](../03_business_model/rendu_principal.md), du [business plan](../04_business_plan/rendu_principal.md), de la [gestion de projet](../07_gestion_de_projet/rendu_principal.md), du [cahier des charges](../06_cahier_des_charges/rendu_principal.md) et de l'[architecture](../08_architecture/rendu_principal.md).

| Risque | Origine | Impact potentiel | Niveau |
|---|---|---|---|
| Dilution du positionnement produit | Étude de marché / business model | Perte de lisibilité face aux SIEM enterprise, XDR, stacks open source et MSSP ; difficulté à expliquer la valeur spécifique de DevinciWatch | Élevé |
| Dérive du périmètre MVP | Feuille de cadrage / gestion de projet / cahier des charges | Ajout de fonctions non indispensables, retard sur la chaîne cœur collecte -> détection -> corrélation -> preuve | Élevé |
| Sous-estimation de la corrélation | Architecture / cahier des charges | Alertes peu explicables, corrélations non démontrables, valeur SOC affaiblie | Élevé |
| Complexité excessive de l'interface | Cahier des charges / architecture | Temps consommé sur l'esthétique au détriment de la lisibilité analyste, des tests et des preuves | Moyen |
| Fragilité du lab Docker de démonstration | Architecture / gestion de projet | Difficulté à reproduire le scénario complet, instabilité des conteneurs, validation moins convaincante | Élevé |
| Surcharge du conteneur `serveur-soc` | Architecture | Risque opérationnel lié au regroupement API, frontend, PostgreSQL, Redis et Celery dans un packaging MVP compact | Moyen |
| Sécurité applicative insuffisamment formalisée | Cahier des charges / architecture | Authentification, contrôle des `roles`, validation des payloads ou audit incomplets ; perte de crédibilité pour un produit cyber | Élevé |
| Données et preuves insuffisamment exploitables | Cahier des charges / étude de marché | Exports incomplets, journaux peu lisibles, difficulté à démontrer la traçabilité et la valeur opérationnelle | Moyen |
| Retard sur tests, stabilisation et documentation | Gestion de projet | Produit fonctionnel mais difficile à vérifier, maintenir ou présenter dans une revue produit | Élevé |
| Hypothèses business trop optimistes | Business model / business plan | Conversion POC, CAC, churn ou marge non réalistes si le produit ne démontre pas rapidement sa valeur | Moyen |
| Adoption limitée par les utilisateurs cibles | Étude de marché / business model | Solution perçue comme trop technique ou insuffisamment actionnable pour une équipe réduite | Moyen |

## 13. Mesures de maîtrise

| Risque couvert | Mesure de maîtrise |
|---|---|
| Dilution du positionnement produit | Maintenir la promesse centrale : supervision cyber pragmatique, alertes actionnables, preuves exportables, sans complexité SIEM enterprise |
| Dérive du périmètre MVP | Appliquer strictement les priorités P1/P2/P3 définies dans le [cahier des charges](../06_cahier_des_charges/rendu_principal.md) |
| Sous-estimation de la corrélation | Limiter la première version à une corrélation lisible : IP source, cible, fenêtre temporelle et répétition observable |
| Complexité excessive de l'interface | Prioriser les écrans utiles à l'analyse : dashboard, actifs, événements, alertes, corrélations, audit et exports |
| Fragilité du lab Docker | Stabiliser tôt le scénario `serveur-soc` / `serveur-endpoint` / `serveur-attacker` et documenter la procédure de lancement |
| Surcharge du conteneur `serveur-soc` | Conserver une séparation logique claire entre API, frontend, base, file de tâches et worker malgré le packaging compact |
| Sécurité applicative insuffisante | Reprendre les exigences de sécurité du cahier des charges : authentification, `roles`, validation des payloads, audit, secrets non exposés |
| Données et preuves insuffisantes | Définir les exports CSV/JSON comme livrables de preuve prioritaires et vérifier leur cohérence avec les scénarios joués |
| Retard sur tests et documentation | Associer chaque jalon à une preuve vérifiable : scénario reproductible, capture, export, log ou document mis à jour |
| Hypothèses business trop optimistes | Utiliser le MVP comme preuve de valeur avant toute extension fonctionnelle ou projection commerciale ambitieuse |
| Adoption limitée | Concevoir les fonctionnalités autour d'un analyste ou administrateur à équipe réduite : lisibilité, simplicité, actionnabilité |

## 14. Décisions structurantes déjà prises

- architecture produit de référence rédigée ;
- frontend intégré au même conteneur que le backend pour le MVP ;
- démonstration en 3 conteneurs ;
- focus sur supervision, corrélation, historique, preuves et exports ;
- orientation produit cohérente avec les études réalisées.

Ces décisions doivent rester stables pendant la phase MVP. Toute extension fonctionnelle devra être évaluée au regard de son apport démonstratif, de sa faisabilité dans le calendrier et de son impact sur la simplicité de l'architecture.

## 15. Dépendances documentaires

- [Kick-off projet (01)](../01_documents_pedagogiques/kickoff/KICKOFF.md)
- [Étude de marché (02)](../02_etude_de_marche/rendu_principal.md)
- [Business model (03)](../03_business_model/rendu_principal.md)
- [Business plan (04)](../04_business_plan/rendu_principal.md)
- [Gestion de projet (06)](../07_gestion_de_projet/rendu_principal.md)
- [Cahier des charges (07)](../06_cahier_des_charges/rendu_principal.md)
- [Architecture produit (08)](../08_architecture/rendu_principal.md)

## 16. Feuille de route courte

Cette feuille de route est volontairement synthétique. Son exécution détaillée est pilotée dans la [gestion de projet (07)](../07_gestion_de_projet/rendu_principal.md) au moyen d'un backlog Scrum, de sprints, de story points et de critères d'acceptation.

1. Phase 1 - Cadrage : consolider le cadrage, finaliser la gestion de projet, le cahier des charges et l'architecture ;
2. Phase 2 - Sprint socle : mettre en place le backend FastAPI, la base de données, le lab Docker et la collecte endpoint minimale ;
3. Phase 3 - Sprints cœur produit : intégrer la découverte réseau, les actifs, les événements, les alertes et l'audit ;
4. Phase 4 - Sprints enrichissement analyste : ajouter la corrélation, les métriques, l'historique, les exports et la visualisation ;
5. Phase 5 - Sprint de stabilisation : stabiliser la démonstration, la documentation finale et le support.

## 17. Conclusion

Cette feuille de cadrage fixe une vision opérationnelle commune du projet. Elle permet de relier le besoin, la valeur, l'architecture, les livrables et les priorités d'exécution dans une même base de pilotage. Elle prépare directement le [cahier des charges (06)](../06_cahier_des_charges/rendu_principal.md) et l'[architecture détaillée (08)](../08_architecture/rendu_principal.md), en cohérence avec la [gestion de projet (07)](../07_gestion_de_projet/rendu_principal.md).
