# 03 - Segmentation, ciblage, positionnement

## Segments considérés

- PME de 50 à 249 employés.
- ETI de 250 à 1000 employés.
- Organisations sensibles : santé, éducation, public local, services numériques.

## Critère de priorisation

- exposition cyber élevée,
- contrainte de conformité,
- manque de ressources SOC internes,
- capacité budgétaire compatible avec une offre SaaS/B2B.

La priorisation combine donc l'intensité du besoin et la faisabilité commerciale. Un segment exposé mais inaccessible commercialement ne constitue pas une cible prioritaire ; inversement, un segment accessible mais peu mature risque de ne pas percevoir suffisamment la valeur du produit.

## Cibles prioritaires recommandées

1. PME/ETI avec SI hétérogène et faible capacité de supervision interne.
2. Organisations qui doivent produire des preuves de suivi sécurité (audit, reporting).

## Score de priorisation des segments

| Segment | Besoin cyber | Accessibilité commerciale | Capacité de paiement | Fit produit | Score / 20 | Décision |
|---|---:|---:|---:|---:|---:|---|
| PME 50-249 | 4 | 4 | 3 | 4 | 15 | Cible d'entrée, offre Essential |
| ETI 250-1000 | 5 | 3 | 5 | 4 | 17 | Cœur de valeur, offre Professional |
| Santé / éducation / public local | 5 | 3 | 3 | 5 | 16 | Cible sensible, approche POC cadrée |
| Grandes entreprises SOC mature | 4 | 2 | 5 | 2 | 13 | Non prioritaire au MVP |
| TPE < 50 employés | 3 | 4 | 1 | 2 | 10 | Hors cible initiale |

Lecture : le score ne mesure pas seulement l'intensité du besoin. Il combine aussi la capacité à vendre, déployer et soutenir la solution avec un effort compatible avec la phase de lancement.

## Positionnement proposé

> Supervision cyber réseau pragmatique pour équipes réduites, avec alertes actionnables et preuves exportables, sans complexité SIEM enterprise.

Ce positionnement est volontairement resserré. Il permet d'éviter une promesse trop large et de concentrer le discours sur la valeur observable : visibilité, priorisation, preuve et simplicité d'exploitation.

## Promesse de valeur

- Time-to-value rapide (mise en place en quelques semaines).
- Pilotage opérationnel simple pour analystes/junior SOC.
- Traçabilité native via exports JSON/CSV pour preuve et gouvernance.

## Ce que le positionnement évite

- La guerre frontale de fonctionnalités contre les SIEM/XDR enterprise.
- Le bricolage open-source non industrialisé en production.

Cette clarification est essentielle pour maintenir une cohérence entre stratégie de marché, business model et périmètre MVP.

## Implications pour la suite du projet

- Le business model doit privilégier une offre annuelle lisible plutôt qu'un pricing complexe au volume.
- Le cahier des charges doit prioriser alertes, corrélation lisible, audit et exports.
- Le business plan doit prévoir des POC cadrés avec critères de succès mesurables.
- La stratégie commerciale doit éviter une dispersion trop rapide vers les grands comptes très matures.
