# 04 - Benchmark concurrence

## Familles de concurrence

Le benchmark ne vise pas à établir un classement exhaustif des solutions de cybersécurité. Il sert à identifier les alternatives réellement comparables du point de vue d'une PME, d'une ETI ou d'une organisation à capacité SOC limitée.

## 1) SIEM/XDR cloud enterprise

- Atouts : couverture large, écosystème mature.
- Limites cible PME/ETI : coût variable, complexité d'opération, besoin expertise.

## 2) Stacks open-source SOC

- Atouts : coût licence faible, contrôle technique.
- Limites : coût caché fort (maintenance, tuning, faux positifs, exploitation quotidienne).

## 3) EDR/NDR spécialisés

- Atouts : profondeur technique sur un axe.
- Limites : vision partielle si non orchestration multi-outils.

## 4) MSSP/SOC externalisé

- Atouts : accélération par externalisation des compétences.
- Limites : dépendance fournisseur, contrôle moindre, coût récurrent.

## Lecture pricing observable (exemples)

- Wazuh Cloud : paliers agents (100/250/500).
- Datadog Cloud SIEM : pricing base volume d'événements.
- Datadog Workload Protection : pricing par host.

Conclusion pricing : la prédictibilité de coût est un avantage compétitif fort sur PME/ETI. Une offre dont le prix augmente fortement avec le volume d'événements peut devenir difficile à piloter pour une organisation qui cherche justement à reprendre le contrôle de sa supervision.

## Scorecard concurrentielle pondérée

| Famille | Coût lisible | Simplicité d'exploitation | Couverture SOC | Time-to-value | Preuve/export | Lecture DevinciWatch |
|---|---:|---:|---:|---:|---:|---|
| SIEM/XDR enterprise | 2 | 2 | 5 | 3 | 4 | Très puissant, mais souvent lourd pour PME/ETI |
| Stack open source SOC | 4 | 2 | 4 | 2 | 3 | Coût licence faible, coût d'exploitation élevé |
| EDR/NDR spécialisé | 3 | 3 | 3 | 4 | 3 | Bon sur un axe, vision plus partielle |
| MSSP / SOC externalisé | 3 | 4 | 4 | 4 | 3 | Rapide, mais dépendance fournisseur et contrôle moindre |
| DevinciWatch | 4 | 4 | 3 | 4 | 5 | Position intermédiaire : lisibilité, action, preuve |

Cette lecture ne cherche pas à prouver que DevinciWatch est supérieur aux solutions établies sur tous les critères. Elle montre plutôt qu'un positionnement défendable existe si le produit reste concentré sur la simplicité, la preuve et la valeur opérationnelle rapide.

## Espace de différenciation défendable

- Offre intermédiaire entre enterprise complexe et open-source exigeant.
- Focalisation sur résultat opérationnel et preuve, pas sur accumulation de features.

DevinciWatch doit donc se différencier par la lisibilité de son usage : une installation compréhensible, des alertes interprétables, des exports exploitables et une démonstration de valeur rapide.

## Conséquences produit

- Ne pas imiter la profondeur fonctionnelle d'un SIEM enterprise.
- Éviter une dépendance excessive à un paramétrage expert.
- Rendre la preuve exportable native dans le produit.
- Maintenir un pricing compréhensible et compatible avec les budgets PME/ETI.
