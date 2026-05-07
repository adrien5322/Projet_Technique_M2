# 05 - Modèle TAM/SAM/SOM (bottom-up)

## Formule de travail

Par segment :

`SOM_segment = N_org × t_need × t_fit × t_access × ACV`

Avec :

- `N_org` : nombre d'organisations
- `t_need` : part avec besoin cyber réseau prioritaire
- `t_fit` : part techniquement/organisationnellement compatible
- `t_access` : part atteignable commercialement à 24-36 mois
- `ACV` : valeur annuelle moyenne contrat

Cette approche bottom-up est préférée à une estimation purement macroéconomique, car elle oblige à expliciter les hypothèses de conversion, d'accès commercial et de valeur annuelle moyenne.

## Décomposition des niveaux de marché

| Niveau | Formule | Rôle |
|---|---|---|
| Base segment | `N_org` | Nombre d'organisations dans le périmètre ciblé |
| Marché servable | `N_org × t_need × t_fit` | Organisations ayant un besoin et un fit réalistes |
| SAM en valeur | `N_org × t_need × t_fit × ACV` | Valeur annuelle servable sous hypothèse de prix |
| SOM en valeur | `SAM × t_access` | Part atteignable à 24-36 mois |

Le modèle évite de confondre taille théorique du marché et part réellement accessible. La variable `t_access` est volontairement restrictive, car le produit devra encore construire sa notoriété, ses références et ses canaux.

## Hypothèses retenues

- Besoin valide par signaux FR/BE/CH.
- Pression compliance durable (NIS2).
- Tension talents cyber persistante.
- Bande ACV de travail : 9k à 24k EUR/an selon segment.

## Justification des coefficients

| Coefficient | Valeur PME | Valeur ETI | Valeur secteurs sensibles | Justification |
|---|---:|---:|---:|---|
| `t_need` | 0,22 | 0,35 | 0,42 | Besoin plus élevé quand la complexité SI et la pression conformité augmentent |
| `t_fit` | 0,32 | 0,48 | 0,44 | Fit plus fort si l'organisation a assez de maturité pour exploiter une solution B2B |
| `t_access` | 0,018 | 0,025 | 0,022 | Accès commercial prudent sur 24-36 mois, avant références fortes |
| `ACV` | 9 000 EUR | 24 000 EUR | 18 000 EUR | Alignement avec capacité de paiement et complexité du besoin |

Ces valeurs ne sont pas des certitudes statistiques. Elles forment un scénario central documenté, conçu pour comparer les segments et alimenter les hypothèses du business model.

## Résultat central consolidé

| Segment | SAM estimé | SOM estimé | Lecture décisionnelle |
|---|---:|---:|---|
| PME 50-249 | 76,0 MEUR | 1,37 MEUR | Volume important, ACV plus faible, bon segment d'entrée |
| ETI 250-1000 | 72,6 MEUR | 1,81 MEUR | Meilleur compromis valeur / fit / capacité de paiement |
| Secteurs sensibles | 46,6 MEUR | 1,02 MEUR | Besoin fort, mais vente plus complexe et plus cadrée |
| Total | 195,2 MEUR | 4,21 MEUR | Potentiel atteignable crédible sous hypothèses prudentes |

## Lecture décisionnelle

- Le résultat est surtout sensible à `t_access`, `ACV` et churn.
- Le modèle est utile pour prioriser les segments avant accélération commerciale.
- L'ETI et les organisations sensibles justifient de conserver une offre Enterprise sur devis.
- Le business model retient néanmoins un ACV moyen plus accessible de 5 900 EUR afin d'accélérer l'adoption PME et de réduire la friction commerciale.
- Le segment PME devient plus central dans le volume client, tandis que Professional et Enterprise préservent la marge.

Le modèle doit être lu comme un outil d'aide à la décision et non comme une prévision certaine. Sa valeur réside dans la comparaison des segments, l'identification des variables sensibles et la préparation du [business model](../../03_business_model/rendu_principal.md).

## Usage attendu

- Alimenter le futur business model avec hypothèses tracées.
- Mettre à jour les coefficients après retours POC/relation terrain.

Les annexes chiffrées associées sont conservées dans le dossier [annexes de l'étude](../annexes/).

Annexes principales :

- [TAM / SAM / SOM par pays et segment](../annexes/tam_sam_som_by_country_segment.csv)
- [Scénarios TAM / SAM / SOM](../annexes/tam_sam_som_scenarios.csv)
- [Passerelle marché vers business model](../annexes/market_to_business_model_bridge.csv)
