# Business Model - DevinciWatch

## 1. Objet du document

Le présent document formalise le modèle économique de DevinciWatch à partir des conclusions de l'[étude de marché](../02_etude_de_marche/rendu_principal.md). Il précise la logique de création de valeur, les segments visés, la structure d'offre, les hypothèses financières de travail et les indicateurs de pilotage qui permettront de suivre la viabilité du projet.

Ce business model n'a pas vocation à figer définitivement les paramètres économiques. Il constitue une version de référence, argumentée et exploitable, destinée à guider les choix produit, commerciaux et financiers.

L'approche retenue distingue la valeur fonctionnelle, la valeur économique et la valeur de gouvernance. Cette distinction permet d'éviter une lecture trop exclusivement technique du produit : DevinciWatch doit être capable de générer des résultats mesurables pour l'utilisateur, mais aussi de soutenir une logique de revenus, de coûts et de pilotage compatible avec une offre B2B.

## 2. Rappel du positionnement

DevinciWatch se positionne comme une solution B2B de supervision cyber réseau pragmatique, destinée aux organisations qui ont besoin de visibilité, d'alertes actionnables et de reporting exploitable, sans supporter la lourdeur opérationnelle et économique d'une plateforme SIEM enterprise complète.

Le positionnement économique découle directement de l'étude de marché : la valeur perçue repose moins sur la quantité de fonctionnalités que sur la combinaison suivante :

- rapidité de mise en œuvre ;
- simplicité d'exploitation ;
- réduction du temps de détection et de qualification ;
- capacité native à produire de la preuve et du reporting.

## 3. Segments clients retenus

Le modèle cible en priorité trois familles d'organisations :

1. les PME de 50 à 249 employés ;
2. les ETI de 250 à 1 000 employés ;
3. les organisations sensibles soumises à des contraintes de sécurité, d'audit ou de conformité.

Le cœur de cible correspond néanmoins aux organisations intermédiaires qui ont déjà une réalité réseau et des enjeux cyber sérieux, mais qui ne disposent ni des moyens ni de l'intérêt économique immédiat pour exploiter une architecture SOC trop lourde. Ce choix de ciblage est central : il évite la dispersion commerciale et permet d'aligner la proposition de valeur sur des besoins observables, comme la visibilité réseau, la qualification d'alertes et la production de preuves.

## 4. Proposition de valeur

La proposition de valeur peut être formulée ainsi :

> DevinciWatch permet à une organisation de superviser son exposition réseau, de détecter plus vite les signaux critiques, de prioriser les alertes et de produire des éléments de preuve, avec un modèle de coût lisible et une charge d'exploitation maîtrisée.

Cette proposition de valeur repose sur quatre bénéfices clients :

- une meilleure visibilité sur les actifs et événements réseau ;
- une amélioration opérationnelle mesurable, notamment sur le MTTD et le MTTR ;
- une réduction du risque de dérive économique lié au volume d'événements ;
- un support plus direct aux obligations de gouvernance et de traçabilité.

La valeur attendue ne se limite donc pas à la détection d'un événement isolé. Elle réside dans la capacité à rendre l'information exploitable : contextualisation, priorisation, historique, export et compréhension par un utilisateur non expert d'un SIEM enterprise.

## 5. Architecture de l'offre

### 5.1. Principes de conception de l'offre

L'offre doit rester suffisamment simple pour être lisible commercialement, tout en permettant un upsell cohérent selon la maturité des clients. La grille tarifaire conservée en annexe propose une structure à trois niveaux, complétée par des options et des services.

### 5.2. Plans proposés

#### Starter

Le plan Starter est proposé à 20 EUR par mois, soit 240 EUR par an [Annexe BM-2]. Il constitue une offre d'appel destinée aux très petites structures, aux environnements de test, aux labs et aux premiers usages de découverte. Il ne porte pas seul l'économie du projet ; son rôle principal est de réduire la friction d'adoption, d'élargir le haut de funnel et de faire découvrir la valeur du produit.

#### Essential

Le plan Essential est proposé à 200 EUR par mois, soit 2 400 EUR par an [Annexe BM-2]. Il cible principalement les PME mono-site qui veulent structurer une première capacité de supervision cyber réseau avec alertes, historique et exports de preuve.

#### Professional

Le plan Professional représente le cœur de l'offre. Il est proposé à 740 EUR par mois, soit 8 880 EUR par an [Annexe BM-2]. Il vise les PME matures, les PME multi-sites, les ETI légères et les organisations sensibles qui ont besoin d'une couverture plus large, d'une meilleure traçabilité, d'une corrélation exploitable et d'un niveau de reporting plus complet.

#### Enterprise

Le plan Enterprise reste proposé sur devis. Il s'adresse aux structures plus exigeantes en matière de gouvernance, de rétention de preuves, de complexité d'environnement, d'accompagnement ou de support renforcé. L'annexe de pricing conserve une valeur de référence de 18 000 EUR par an pour les calculs, sans en faire un prix public obligatoire.

### 5.3. Add-ons et services

Le modèle prévoit également des revenus additionnels :

- support premium : 1 200 EUR par an ;
- rétention longue : 900 EUR par an ;
- onboarding standard : 800 EUR ;
- onboarding avancé : 2 500 EUR [Annexe BM-2].

Ces briques complémentaires ont une double utilité : améliorer la marge et adapter l'offre à la complexité réelle des comptes.

## 6. Logique de revenus

Le business model repose sur trois sources de revenus :

1. l'abonnement annuel récurrent ;
2. les frais de mise en service et d'onboarding ;
3. les services et options complémentaires.

L'hypothèse de travail consolidée retient désormais un ACV moyen de 5 900 EUR par an [Annexe BM-1]. Cette valeur est une moyenne pondérée des plans : Starter (240 EUR/an), Essential (2 400 EUR/an), Professional (8 880 EUR/an) et Enterprise (18 000 EUR/an), ajustée selon la répartition cible des clients. Cette moyenne reflète un modèle plus accessible, soutenu par un volume client plus élevé.

### Analyse de marché intégrée (mai 2026)

Les données collectées (NVD 30 CVEs récents, CISA KEV 1 587 entrées) confirment la pertinence du positionnement :
- **Score d'intensité** : 1 114,8 (niveau Élevé)
- **Top 5 fournisseurs critiques** : Microsoft (370), Apple (93), Cisco (89), Adobe (78), Google (71)
- **Ransomware identifié** : 317 cas (20 % des KEV)
- **Répartition CVE 2026** : 23 % Critique, 20 % Élevé, 57 % Moyen

Cette concentration des risques valide l'ACV moyen de 5 900 EUR : les organisations ont besoin d'une solutionaccessible comme DevinciWatch (20€/200€/740€/mois) pour surveiller ces menaces croissantes.

## 7. Logique de coûts

La structure de coûts se répartit en quatre blocs principaux :

- produit : développement, maintenance, qualité, sécurité ;
- infrastructure : stockage, traitement, supervision, hébergement ;
- go-to-market : acquisition, avant-vente, partenariats ;
- customer success : onboarding, support, adoption et rétention.

Cette structure est importante, car elle conditionne la marge brute et le délai de récupération du coût d'acquisition.

## 8. Hypothèses économiques de référence

Les hypothèses consolidées du modèle sont les suivantes [Annexe BM-1] :

- ACV moyen : 5 900 EUR par an ;
- conversion démo ou POC vers abonnement : 28 % ;
- CAC moyen : 1 800 EUR par client ;
- churn logo : 12 % en année 2 puis 10 % en année 3 ;
- marge brute : 72 % en année 1, 76 % en année 2, 79 % en année 3 ;
- mix nouveaux logos : 75/25 direct/partenaire en année 1, 61/39 en année 2, 46/54 en année 3.

Ces hypothèses doivent être lues comme un scénario directeur raisonnable, et non comme une certitude. Elles servent à piloter les arbitrages.

## 9. Scénarios d'évolution

Le modèle prévoit trois scénarios : prudent, base et ambitieux [Annexe BM-4].

### 9.1. Scénario prudent

Le scénario prudent suppose un ACV moyen de 3 000 EUR, un CAC de 2 200 EUR, une conversion démo ou POC vers abonnement de 18 % et un churn plus élevé. Il conduit à une ARR de 360 000 EUR en année 1, 885 000 EUR en année 2 et 1 550 000 EUR en année 3.

### 9.2. Scénario de base

Le scénario de base est le scénario recommandé pour le pilotage. Il retient un ACV moyen de 5 900 EUR, un CAC de 1 800 EUR et un taux de conversion démo ou POC vers abonnement de 28 %. Il conduit à une ARR de 708 000 EUR en année 1, 1 685 040 EUR en année 2 et 3 050 536 EUR en année 3.

### 9.3. Scénario ambitieux

Le scénario ambitieux suppose une meilleure exécution commerciale, un mix plus fort sur Professional/Enterprise et une accélération du canal partenaire. Il projette une ARR de 1 170 000 EUR en année 1, 2 850 000 EUR en année 2 et 5 300 000 EUR en année 3.

## 10. Mécanique commerciale et canaux

Le modèle repose sur un lancement hybride, combinant vente directe et partenariats. Cette approche répond à deux impératifs :

- conserver une boucle d'apprentissage rapide avec les premiers clients ;
- préparer une montée en échelle plus efficace grâce au canal partenaire.

Le mix de nouveaux logos prévu reflète cette logique de transition progressive [Annexe BM-1].

## 11. Indicateurs de pilotage

Les KPI cibles à suivre sont les suivants [Annexe BM-5] :

- taux de conversion démo ou POC vers abonnement : 24 % en année 1, 28 % en année 2, 31 % en année 3 ;
- CAC : 2 100 EUR en année 1, 1 800 EUR en année 2, 1 500 EUR en année 3 ;
- churn logo : 12 % puis 10 % ;
- marge brute : 72 %, 76 %, 79 % ;
- délai de payback CAC : 6,0 mois, puis 4,8 mois, puis 3,8 mois ;
- ARR de fin d'année : 708 000 EUR, 1 685 040 EUR, 3 050 536 EUR.

Ces KPI ont une fonction de gouvernance. Ils permettent de détecter rapidement une dérive de conversion, de coût d'acquisition, de marge ou de rétention.

## 12. Principaux risques du modèle

Les risques majeurs du business model sont les suivants :

- un coût d'acquisition supérieur aux hypothèses ;
- un niveau de conversion démo ou POC vers abonnement insuffisant ;
- une dilution du positionnement par surenchère fonctionnelle ;
- une dépendance trop forte à un canal de distribution unique ;
- une insuffisante standardisation de l'onboarding et du support ;
- une cannibalisation excessive vers le plan Starter, qui réduirait l'ACV moyen.

Pour limiter ces risques, le modèle doit rester discipliné : ciblage serré, offre lisible, critères de qualification stricts et suivi mensuel des KPI. La robustesse économique du projet dépendra moins d'une multiplication des options que de la capacité à maintenir une promesse claire et répétable.

## 13. Conclusion

Le business model de DevinciWatch est cohérent avec le diagnostic de marché. Il repose sur une promesse simple : générer un résultat opérationnel tangible pour des organisations qui ont besoin de mieux superviser sans surinvestir dans une complexité difficile à absorber.

La réussite du modèle dépendra moins d'une sophistication tarifaire excessive que de la capacité à démontrer rapidement la valeur, à contenir le CAC, à industrialiser l'onboarding et à améliorer la rétention.

## 14. Références mobilisées

### Références principales

- [Étude de marché](../02_etude_de_marche/rendu_principal.md)
- [Modèle TAM / SAM / SOM](../02_etude_de_marche/references/05_modele_tam_sam_som.md)
- [Stratégie d'entrée sur le marché](../02_etude_de_marche/references/06_strategie_entree_marche.md)
- [Risques, KPI et preuves](../02_etude_de_marche/references/07_risques_kpi_et_preuves.md)
- [Sources de référence](../02_etude_de_marche/references/08_sources_reference.md)
- [README de l'étude de marché](../02_etude_de_marche/README.md)

### Références chiffrées

- [Annexe BM-1] [Hypothèses business model](annexes/business_model_assumptions_v4.csv)
- [Annexe BM-2] [Grille tarifaire](annexes/pricing_grid_v1.csv)
- [Annexe BM-3] [Prévision trois ans](annexes/forecast_3y_v4_base.csv)
- [Annexe BM-4] [Modèle de scénarios](annexes/scenario_model_v4.csv)
- [Annexe BM-5] [KPI cibles](annexes/kpi_targets_v4.csv)
- [Annexe BM-6] [Plan de mix canal](annexes/channel_mix_plan_v3.csv)

### Références antérieures conservées

- [Registre transverse des sources](../90_references_transverses/source_register.csv)
- [Annexe TAM / SAM / SOM](../02_etude_de_marche/annexes/tam_sam_som_bottomup_v2.csv)
- [Matrice go-to-market](../02_etude_de_marche/annexes/gtm_comparison_matrix.csv)
- [Passerelle marché vers business model](../02_etude_de_marche/annexes/market_to_business_model_bridge.csv)

Ces références relient explicitement le business model aux hypothèses marché, aux sources institutionnelles, aux analyses stratégiques et au choix d'un pricing plus accessible.

## 15. Annexes chiffrées

- [Hypothèses business model](annexes/business_model_assumptions_v4.csv)
- [Grille tarifaire](annexes/pricing_grid_v1.csv)
- [Prévision trois ans](annexes/forecast_3y_v4_base.csv)
- [Modèle de scénarios](annexes/scenario_model_v4.csv)
- [KPI cibles](annexes/kpi_targets_v4.csv)
- [Plan de mix canal](annexes/channel_mix_plan_v3.csv)
