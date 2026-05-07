# 07 - Risques, KPI et preuves attendues

## Risques majeurs

- Conversion POC -> production insuffisante.
- Churn élevé après déploiement initial.
- Coût d'acquisition supérieur à la capacité de financement.
- Positionnement trop flou face aux alternatives.

Ces risques sont interdépendants. Un positionnement flou peut dégrader la conversion POC, augmenter le coût d'acquisition et fragiliser la rétention, même si le produit est techniquement correct.

## Matrice risques / KPI / preuve

| Risque | KPI de surveillance | Seuil d'alerte | Preuve ou action attendue |
|---|---|---|---|
| Conversion démo ou POC vers abonnement insuffisante | `Demo_or_POC_to_Paid` | < 20 % | Revoir critères de qualification et critères de succès démo/POC |
| Churn élevé après déploiement | `Logo_Churn`, `Revenue_Churn` | > 15 % annuel | Renforcer onboarding, support et métriques d'adoption |
| CAC supérieur aux hypothèses | `CAC`, `CAC_Payback` | CAC > 15 000 EUR | Rééquilibrer canaux, playbook commercial et ciblage |
| Positionnement trop flou | Taux de conversion SQL -> POC | Baisse continue sur 2 trimestres | Clarifier message et verticales prioritaires |
| Produit trop large trop tôt | Taux de stories P1 terminées, délai POC | Retard P1 ou POC > 8 semaines | Recentrer MVP sur alertes, preuve, export, audit |

## Garde-fous proposés

- Critères de succès POC contractualisés.
- Onboarding et runbooks standardisés.
- Priorisation géographie/secteurs avant extension.
- Message unique centré sur "résultat opérationnel + preuve".

Les garde-fous doivent être intégrés dès la phase MVP : ils concernent autant la conception produit que le discours commercial et la préparation de la démonstration.

## KPI de pilotage recommandés

- MTTD et MTTR (avant/après déploiement).
- Taux de faux positifs.
- Couverture actifs supervisés.
- Taux conversion POC -> abonnement.
- Churn client à 6 et 12 mois.
- Délai moyen de mise en production.
- CAC payback.
- LTV/CAC.
- Taux d'activation des exports de preuve.
- Couverture des actifs supervisés.

Ces KPI doivent être suivis comme des indicateurs de décision. Ils permettent de savoir si la proposition de valeur est comprise, si le produit est exploitable et si le modèle économique reste soutenable.

## Preuves attendues en validation produit

- Cas d'usage de détection observable.
- Alertes générées et traitées.
- Exports JSON/CSV exploitables.
- Cohérence entre besoin initial, solution technique et valeur business.

La validation produit doit montrer une chaîne complète : besoin identifié, scénario exécuté, événement observé, alerte produite, preuve exportée et valeur expliquée.

## Transmission vers le business model

Les KPI de cette étude ne servent pas seulement à suivre le marché. Ils deviennent les hypothèses de pilotage du [business model](../../03_business_model/rendu_principal.md) : ACV, conversion POC, CAC, churn, marge brute et adoption produit. Toute dérive observée pendant les premiers POC doit donc entraîner une mise à jour des hypothèses financières.
