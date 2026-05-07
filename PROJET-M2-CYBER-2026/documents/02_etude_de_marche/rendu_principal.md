# Étude de marché - DevinciWatch

## 1. Objet du document

La présente étude de marché a pour objectif de démontrer la pertinence économique et stratégique de DevinciWatch, solution de supervision et d'analyse cyber réseau orientée usage. Elle s'inscrit dans le cadre du projet défini par le [kick-off](../01_documents_pedagogiques/kickoff/KICKOFF.md) et par le cahier d'attendus, qui demandent explicitement une étude de marché, un modèle économique et une stratégie d'entrée sur le marché.

L'analyse adopte une posture rigoureuse : elle distingue les faits documentés, les hypothèses de travail et les décisions qui en découlent. Cette distinction est essentielle, car un projet cyber ne peut pas être justifié uniquement par l'intuition technique ; il doit s'appuyer sur une compréhension argumentée de la demande, de la concurrence, des contraintes réglementaires et de la capacité réelle du marché à adopter la solution.

Cette étude répond à quatre questions structurantes :

1. Le besoin adressé est-il réel, durable et suffisamment prioritaire pour des organisations clientes ?
2. Quels segments présentent le meilleur équilibre entre besoin, accessibilité commerciale et capacité de paiement ?
3. Comment positionner la solution face aux alternatives existantes ?
4. Quelle trajectoire d'entrée sur le marché paraît la plus crédible à court et moyen terme ?

### 1.1. Méthode de travail et logique de preuve

L'étude suit une logique en huit étapes afin de rendre les résultats traçables et discutables :

1. collecter les signaux de marché à partir de sources institutionnelles, sectorielles et concurrentielles ;
2. qualifier la fiabilité des sources selon leur origine, leur fraîcheur, leur usage décisionnel et leur niveau de confiance ;
3. transformer les constats documentés en hypothèses de marché explicites ;
4. appliquer une modélisation bottom-up du marché adressable ;
5. tester les hypothèses avec des scénarios prudent, central et ambitieux ;
6. identifier les variables les plus sensibles : accès commercial, ACV, conversion POC, CAC, churn ;
7. traduire les résultats en décisions de segmentation, positionnement, prix et go-to-market ;
8. transmettre les hypothèses retenues au [business model](../03_business_model/rendu_principal.md) et au [business plan](../04_business_plan/rendu_principal.md).

Cette méthode évite de partir d'une estimation macro trop abstraite. Elle privilégie une chaîne de justification observable : source -> constat -> hypothèse -> calcul -> décision. Les annexes chiffrées créées pour cette étude conservent cette traçabilité.

## 2. Rappel du besoin initial

Le projet DevinciWatch vise à concevoir un outil de supervision et d'analyse réseau capable de :

- détecter les équipements connectés ;
- scanner des plages d'adresses IP ;
- identifier les ports ouverts ;
- récupérer des informations sur les services réseau ;
- observer le trafic ;
- détecter des comportements suspects ou malveillants ;
- générer des alertes ;
- produire des exports exploitables, notamment en JSON et CSV.

L'enjeu n'est donc pas seulement technique. Il s'agit de transformer ce socle fonctionnel en offre lisible, utile et défendable sur un marché où les clients attendent à la fois de la détection, de la réactivité et de la traçabilité. Le produit doit ainsi répondre à une double exigence : produire des signaux cyber pertinents et rendre ces signaux suffisamment compréhensibles pour soutenir une décision opérationnelle.

## 3. Hypothèse centrale de marché

L'hypothèse retenue est la suivante : il existe une place de marché pour une solution de supervision cyber réseau plus simple à déployer et à exploiter que les stacks SIEM/XDR lourdes, tout en étant plus industrialisée et plus orientée résultat qu'un assemblage open source maintenu en interne.

Cette hypothèse ne suppose pas que DevinciWatch remplace les plateformes les plus matures. Elle affirme plutôt l'existence d'un espace intermédiaire : celui des organisations qui ont besoin d'une visibilité cyber concrète, mais qui ne peuvent pas absorber la complexité humaine, financière et technique d'un SOC complet.

### 3.1. Validation par l'analyse des données (mai 2026)

L'analyse technique récente (30 CVE récents collectés via NVD, 1 587 entrées CISA KEV) confirme l'intensité de la menace :

- **Score d'intensité de la menace** : 1 114,8 (niveau Élevé)
- **CVE récents analysés (2026)** : 30 vulnérabilités dont 13 critiques/hauts (43 %)
- **Vulnérabilités connues et exploitées (CISA KEV)** : 1 587 entrées référencées
- **Ransomware identifié** : 317 cas documentés (20 % des KEV)
- **Implication pour le marché SIEM** : Forte demande soutenue par la criticité croissante

**Top 5 des fournisseurs les plus touchés** (source : CISA KEV) :
1. Microsoft (370 vulnérabilités)
2. Apple (93)
3. Cisco (89)
4. Adobe (78)
5. Google (71)

**Répartition des CVE 2026 par sévérité** (source : NVD) :
- Critique : 7 (23 %)
- Élevé : 6 (20 %)
- Moyen : 17 (57 %)

**Exemples de vulnérabilités critiques récentes (2026)** :
- CVE-2026-42364 : GeoVision LPC2011 - OS Command Injection (9,9/10)
- CVE-2026-42368 : GeoVision GV-VMS V20 - Privilege Escalation (9,9/10)
- CVE-2026-42369 : GeoVision GV-VMS V20 - Credentials Leak (10,0/10)

Cette concentration des risques sur les technologies dominantes, combinée à l'émergence de vulnérabilités critiques sur des équipements connectés (GeoVision, MindsDB, etc.), valide le positionnement de DevinciWatch : une solution accessible, orientée détection réseau, capable de surveiller l'infrastructure indépendamment du fournisseur.

Cette hypothèse repose sur trois constats convergents :

- la pression cyber reste élevée dans les pays cibles ;
- la pression réglementaire pousse à mieux détecter, tracer et démontrer ;
- la pénurie de compétences cyber favorise les offres qui réduisent la complexité opérationnelle.

## 4. Analyse du contexte et de la demande

### 4.1. Une menace durable et documentée

Les données collectées dans les annexes montrent une intensité élevée et persistante de la menace cyber sur le périmètre prioritaire France, Belgique et Suisse francophone.

En France, l'ANSSI a traité 3 586 événements de sécurité en 2025, dont 2 209 signalements et 1 366 incidents [S01]. Sur le même marché, Cybermalveillance.gouv.fr a accompagné plus de 500 000 victimes, avec une progression de 107 % des violations de données et de 70 % du phishing [S02].

En Belgique, le Centre for Cybersecurity Belgium fait état de 556 notifications de cyberattaques, 635 notifications NIS2, 105 cas de ransomware et 63 attaques DDoS sur l'année 2025 [S21]. Les incidents signalés progressent de 70 % et les incidents cyber de 58 % [S22].

En Suisse, les rapports semestriels du NCSC recensent 35 727 signalements sur le premier semestre, dont 58 % liés à la fraude, puis 29 006 signalements volontaires sur la période suivante [S23][S24].

### 4.2. Une pression réglementaire qui transforme le besoin en priorité

La directive NIS2 étend les obligations de gestion du risque et de notification à 18 secteurs critiques [S05]. Cette évolution ne crée pas seulement une contrainte documentaire ; elle renforce le besoin d'outils capables de fournir des éléments probants : journaux exploitables, alertes structurées, visibilité opérationnelle et reporting.

Dans cette logique, une solution comme DevinciWatch doit être pensée non seulement comme un outil de surveillance, mais comme un outil d'exécution et de preuve.

### 4.3. Une difficulté structurelle de recrutement et d'exploitation

L'ENISA souligne que 76 % des organisations font face à des difficultés de recrutement sur les profils cyber et 71 % à des difficultés de rétention [S13]. Cette tension a une conséquence directe : la valeur d'une solution n'est pas seulement fonction de sa couverture technique, mais de sa capacité à être réellement opérée par une équipe réduite.

De plus, Mandiant relève un dwell time médian mondial de 11 jours, avec une forte présence des exploits comme vecteur initial (33 %) et des identifiants compromis (16 %) [S04]. Ces données renforcent l'intérêt d'une solution capable d'accélérer la détection et la qualification opérationnelle.

## 5. Périmètre de marché retenu

### 5.1. Périmètre géographique

Le périmètre prioritaire retenu est constitué de la France, de la Belgique et de la Suisse francophone. Ce choix est justifié par :

- la disponibilité de sources publiques solides et récentes ;
- une proximité réglementaire et linguistique favorable au démarrage ;
- un tissu d'organisations exposées aux mêmes enjeux de cybersécurité, de conformité et de manque de compétences.

### 5.2. Segments visés

Trois segments ont été retenus :

1. les PME de 50 à 249 employés ;
2. les ETI de 250 à 1 000 employés ;
3. les organisations sensibles, notamment dans la santé, l'éducation, le secteur public local et les services numériques.

Ces segments présentent un point commun décisif : ils ont souvent besoin d'une meilleure supervision, mais ne disposent pas toujours des ressources pour opérer une plateforme lourde ou un SOC avancé.

## 6. Segmentation, ciblage et positionnement

### 6.1. Critères de ciblage

Le ciblage a été construit à partir de quatre critères :

- niveau d'exposition cyber ;
- intensité de la contrainte de conformité ;
- insuffisance ou absence de capacité SOC interne ;
- capacité à absorber un abonnement annuel B2B.

### 6.2. Cibles prioritaires

Les cibles prioritaires sont les organisations qui cumulent les caractéristiques suivantes :

- infrastructure réseau suffisamment structurée pour que la supervision crée de la valeur ;
- besoin de visibilité et de reporting ;
- capacité de décision relativement courte ;
- maturité suffisante pour industrialiser un usage, mais insuffisante pour déployer un SIEM enterprise complet.

### 6.3. Positionnement recommandé

Le positionnement recommandé est le suivant :

> DevinciWatch est une solution de supervision cyber réseau pragmatique, conçue pour des équipes réduites, qui fournit des alertes actionnables, une visibilité exploitable et des preuves exportables sans la complexité d'une plateforme SIEM enterprise.

Ce positionnement repose sur quatre piliers de valeur :

- simplicité de mise en œuvre ;
- réduction du temps de détection et de qualification ;
- lisibilité économique ;
- capacité native à produire de la preuve.

## 7. Analyse concurrentielle

### 7.1. SIEM et XDR cloud enterprise

Les solutions de type Datadog, Splunk, Microsoft Sentinel ou Elastic Security bénéficient d'une couverture fonctionnelle large et d'un écosystème mature. En revanche, elles présentent souvent, pour la cible PME/ETI, trois limites majeures :

- un coût parfois difficile à anticiper ;
- une dépendance à des compétences de paramétrage et d'exploitation ;
- une charge de conduite du changement non négligeable.

Les données de benchmark montrent par exemple des modèles tarifaires liés au volume d'événements ou au nombre d'hôtes, ce qui peut accroître l'imprévisibilité budgétaire [S09][S10].

### 7.2. Stacks open source de type SOC

Les approches construites autour de Wazuh, Suricata, Zeek, ELK ou Security Onion offrent une grande souplesse et un coût de licence faible. Elles restent toutefois plus exigeantes à industrialiser et à maintenir. Le coût visible est bas, mais le coût caché d'exploitation peut être élevé.

Le benchmark conservé en annexe confirme cet arbitrage. Le prix catalogue Wazuh Cloud à 100 agents, 250 agents et 500 agents donne un repère utile, mais ne suffit pas à refléter le coût total d'usage [S08].

### 7.3. MSSP et SOC externalisés

Les MSSP répondent bien au besoin d'externalisation de la compétence, mais ils peuvent réduire le contrôle direct, allonger certains temps de boucle et augmenter le coût récurrent selon le niveau d'accompagnement attendu.

### 7.4. Espace de différenciation de DevinciWatch

L'espace de différenciation défendable n'est pas la guerre de fonctionnalités. Il réside dans la combinaison suivante :

- déploiement plus rapide ;
- coût plus lisible ;
- gouvernance plus simple ;
- production native d'alertes et d'exports exploitables.

La proposition de valeur doit donc rester centrée sur le résultat opérationnel et sur la preuve, pas sur l'accumulation fonctionnelle.

## 8. Modélisation TAM / SAM / SOM

Le modèle retenu en annexe s'appuie sur une approche bottom-up :

`SOM_segment = N_org × t_need × t_fit × t_access × ACV`

Cette approche est plus pertinente qu'une estimation purement macro, car elle introduit des variables de réalisme commercial : besoin, compatibilité, accès au segment et valeur annuelle moyenne du contrat.

### 8.1. Processus de chiffrage

La modélisation distingue trois niveaux :

| Niveau | Objectif | Formule |
|---|---|---|
| Base segment | Identifier le nombre d'organisations théoriquement pertinentes | `N_org` |
| SAM | Estimer la valeur annuelle accessible en fonction du besoin et du fit | `N_org × t_need × t_fit × ACV` |
| SOM | Estimer la part réellement atteignable à 24-36 mois | `SAM × t_access` |

Les coefficients utilisés ont la signification suivante :

| Coefficient | Signification | Interprétation DevinciWatch |
|---|---|---|
| `t_need` | Part du segment ayant un besoin cyber réseau prioritaire | Intensité de menace, conformité, besoin de reporting |
| `t_fit` | Part du segment compatible avec une solution pragmatique | Maturité suffisante, budget, absence de SOC lourd |
| `t_access` | Part commercialement atteignable à court/moyen terme | Capacité à toucher le segment via direct ou partenaires |
| `ACV` | Valeur annuelle moyenne du contrat | Prix annuel réaliste selon taille et complexité client |

Le calcul consolidé aboutit à un SAM de travail d'environ 195,2 MEUR et à un SOM central d'environ 4,2 MEUR à horizon 24-36 mois. Ce résultat ne doit pas être interprété comme un chiffre d'affaires garanti, mais comme une borne de potentiel accessible sous hypothèses explicites.

### 8.2. Passage vers les hypothèses business

L'étude de marché identifie une capacité de paiement B2B pouvant aller de 9 000 à 24 000 EUR par an selon les segments et les alternatives comparées. Le [business model](../03_business_model/rendu_principal.md) retient toutefois un pricing public volontairement plus accessible : 20 EUR, 200 EUR et 740 EUR par mois, complété par une offre Enterprise sur devis.

Cette décision transforme la logique économique : DevinciWatch ne cherche plus seulement à capter une valeur annuelle élevée par compte, mais à réduire la friction d'adoption, augmenter le volume de clients atteignables et rendre l'offre plus lisible pour les PME. L'ACV moyen de pilotage devient donc 5 900 EUR par an, porté par :

- une offre Professional à 740 EUR par mois au cœur de la stratégie ;
- une offre Essential à 200 EUR par mois pour les PME mono-site ;
- une offre Starter à 20 EUR par mois conçue comme canal d'adoption et non comme cœur de marge ;
- une offre Enterprise sur devis pour préserver une capacité de montée en valeur ;
- des add-ons de support, rétention ou onboarding.

La cohérence entre l'étude de marché et le business model repose donc sur une logique d'accessibilité : la fourchette marché valide la capacité de paiement maximale de certaines cibles, tandis que la grille retenue privilégie une pénétration plus rapide et un coût plus lisible.

Les hypothèses principales sont les suivantes :

- horizon de pénétration : 24 à 36 mois ;
- ACV de travail business model : 5 900 EUR par an, avec une capacité de paiement marché supérieure sur les segments ETI et sensibles ;
- forte sensibilité à l'accès commercial, au prix moyen et au churn.

Cette modélisation ne constitue pas une prévision automatique ; elle sert à hiérarchiser les segments et à structurer les décisions de go-to-market.

## 9. Stratégie d'entrée sur le marché

Trois options ont été analysées :

1. vente directe ;
2. distribution par partenaires de type MSSP ou intégrateurs ;
3. modèle hybride.

L'analyse comparative conservée en annexe conduit à recommander un modèle hybride. Celui-ci permet :

- de garder un canal direct pour apprendre vite ;
- d'accélérer la diffusion grâce à des partenaires sélectionnés ;
- de réduire le risque de dépendance à un canal unique.

La stratégie recommandée consiste à sécuriser un minimum de pipeline direct tout en structurant 2 à 3 partenariats ciblés.

### 9.1. Justification chiffrée du choix hybride

La matrice de go-to-market compare les options direct, partenaire et hybride sur cinq critères : vitesse de traction, efficacité du CAC, qualité du pipeline, contrôle de la relation client et risque d'exécution. Le modèle hybride obtient le meilleur score pondéré, car il équilibre apprentissage direct et capacité de diffusion.

Cette décision influence directement le business model : le lancement conserve une majorité de ventes directes en année 1, puis augmente progressivement la part partenaire afin de réduire la dépendance au canal direct et d'accélérer l'accès aux organisations cibles.

## 10. Risques de marché identifiés

Les principaux risques de marché sont les suivants :

- une conversion démo ou POC vers abonnement inférieure aux hypothèses ;
- un coût d'acquisition trop élevé sur certaines verticales ;
- un positionnement insuffisamment différencié ;
- une valeur perçue diluée si le produit devient trop large trop tôt.

Ces risques appellent une exécution disciplinée : qualification stricte, cadrage du POC, pilotage des KPI et clarté du message commercial.

### 10.1. Variables sensibles à surveiller

| Variable | Risque si dérive | Impact business | Réponse recommandée |
|---|---|---|---|
| `t_access` | Marché identifié mais difficile à atteindre | Pipeline insuffisant | Structurer partenaires et qualification verticale |
| ACV | Prix moyen inférieur au mix cible | ARR et marge affaiblies | Clarifier packaging et valeur des add-ons |
| Conversion POC -> production | POC non transformés | CAC non amorti | Définir critères de succès POC avant lancement |
| CAC | Acquisition trop coûteuse | Payback trop long | Standardiser discours, playbooks et canaux |
| Churn | Perte de clients après première année | LTV/CAC dégradé | Onboarding, support, métriques d'adoption |

Ces variables sont reprises dans les annexes de sensibilité et dans les hypothèses du business model afin de maintenir une continuité entre diagnostic marché, modèle économique et business plan.

## 11. Conclusion générale

L'étude de marché valide l'existence d'une opportunité crédible pour DevinciWatch. Le marché n'est pas en manque d'outils ; il est en manque de solutions réellement exploitables, économiquement lisibles et capables de transformer la conformité et la surveillance en action opérationnelle.

La priorité n'est donc pas de rivaliser frontalement avec les plateformes les plus complètes du marché. Elle est de proposer une solution claire, utile et démontrable pour des organisations qui doivent améliorer leur supervision sans complexifier davantage leur exploitation.

### 11.1. Décisions structurantes issues de l'étude

| Décision | Justification marché | Impact pour la suite |
|---|---|---|
| Cibler PME, ETI et organisations sensibles | Besoin cyber réel, mais capacité SOC limitée | Alimente le business model et la feuille de cadrage |
| Positionnement intermédiaire | Écart entre SIEM enterprise et open source exigeant | Promesse centrée sur simplicité, alerte, preuve |
| Prix annuel lisible | Risque de coûts variables chez certaines alternatives | Construction d'offres annuelles B2B |
| Go-to-market hybride | Direct utile pour apprendre, partenaires utiles pour diffuser | Mix canal progressif dans le business plan |
| MVP orienté preuve | Besoin de traçabilité, conformité et valeur démontrable | Priorité aux alertes, exports, audit et scénario reproductible |

## 12. Références mobilisées

### Références externes

- [S01] [ANSSI, Panorama de la cybermenace 2025](https://cyber.gouv.fr/actualites/panorama-de-la-cybermenace-2025/).
- [S02] [Cybermalveillance.gouv.fr, Rapport d'activité 2025](https://www.cybermalveillance.gouv.fr/tous-nos-contenus/actualites/rapport-activite-2025).
- [S04] [Google Cloud / Mandiant, M-Trends 2025](https://cloud.google.com/blog/topics/threat-intelligence/m-trends-2025).
- [S05] [Commission européenne, Directive NIS2](https://digital-strategy.ec.europa.eu/en/policies/nis2-directive).
- [S08] [Wazuh Cloud Pricing](https://wazuh.com/cloud/).
- [S09] [Datadog Cloud SIEM Pricing](https://www.datadoghq.com/pricing/?product=cloud-siem).
- [S10] [Datadog Workload Protection Pricing](https://www.datadoghq.com/pricing/?product=workload-protection).
- [S13] [ENISA, NIS Investments 2025 - communication et données associées](https://www.enisa.europa.eu/news/whats-driving-cybersecurity-investments-and-where-lie-the-challenges).
- [S14] [ENISA, NIS360 2024](https://www.enisa.europa.eu/news/enisa-nis360-2024-report).
- [S16] [NIST Cybersecurity Framework 2.0](https://www.nist.gov/cyberframework).
- [S17] [Verizon, Data Breach Investigations Report](https://www.verizon.com/business/resources/reports/dbir/).
- [S18] [PwC, Global Digital Trust Insights](https://www.pwc.com/gx/en/issues/cybersecurity/global-digital-trust-insights.html).
- [S19] [IBM, Cost of a Data Breach Report](https://www.ibm.com/reports/data-breach).
- [S20] [OECD, Digital Security](https://www.oecd.org/digital/digital-security/).
- [S21] [Centre for Cybersecurity Belgium, chiffres clés 2025](https://ccb.belgium.be/en).
- [S22] [Centre for Cybersecurity Belgium, réalité cyber 2025](https://ccb.belgium.be/fr/news/plus-dattaques-plus-de-signalements-la-realite-cyber-de-la-belgique-en-2025).
- [S23] [NCSC Suisse, rapport semestriel 2025/1](https://www.ncsc.admin.ch/ncsc/fr/home/dokumentation/berichte/lageberichte/halbjahresbericht-2025-1.html).
- [S24] [NCSC Suisse, rapport semestriel 2025/2](https://www.ncsc.admin.ch/ncsc/fr/home/dokumentation/berichte/lageberichte/halbjahresbericht-2025-2.html).

### Références internes et annexes d'étude

- [Cadrage de référence](references/01_cadrage_reference.md)
- [Analyse de la demande et du contexte](references/02_analyse_demande_et_contexte.md)
- [Segmentation, ciblage et positionnement](references/03_segmentation_ciblage_positionnement.md)
- [Benchmark concurrence](references/04_benchmark_concurrence.md)
- [Modèle TAM / SAM / SOM](references/05_modele_tam_sam_som.md)
- [Stratégie d'entrée sur le marché](references/06_strategie_entree_marche.md)
- [Risques, KPI et preuves](references/07_risques_kpi_et_preuves.md)
- [Sources de référence](references/08_sources_reference.md)
- [README de l'étude de marché](README.md)

### Registre complet des sources antérieures conservées

- [Registre transverse des sources](../90_references_transverses/source_register.csv)
- [Matrice de qualité des sources](../90_references_transverses/source_quality_matrix.csv)

Le registre complet conserve l'ensemble des références exploitées dans l'étude consolidée, notamment les sources institutionnelles, sectorielles et concurrentielles S01 à S32. Il constitue la base de traçabilité détaillée des chiffres et constats mobilisés dans le présent document.

## 13. Annexes chiffrées

- [Registre transverse des sources](../90_references_transverses/source_register.csv)
- [Matrice de qualité des sources](../90_references_transverses/source_quality_matrix.csv)
- [Annexe TAM / SAM / SOM](annexes/tam_sam_som_bottomup_v2.csv)
- [Benchmark concurrence](annexes/competition_benchmark_v2.csv)
- [Matrice comparative go-to-market](annexes/gtm_comparison_matrix.csv)
- [Modèle de KPI business model](annexes/kpi_template_business_model.csv)
- [Modèle de sensibilité](annexes/sensitivity_model_template.csv)
- [TAM / SAM / SOM par pays et segment](annexes/tam_sam_som_by_country_segment.csv)
- [Scénarios TAM / SAM / SOM](annexes/tam_sam_som_scenarios.csv)
- [Registre des hypothèses marché](annexes/market_assumptions_register.csv)
- [Matrice de traçabilité décisionnelle](annexes/decision_traceability_matrix.csv)
- [Scorecard concurrentielle pondérée](annexes/competitor_weighted_scorecard.csv)
- [Matrice GTM pondérée](annexes/gtm_weighted_decision_matrix.csv)
- [Benchmark pricing enrichi](annexes/pricing_benchmark_extended.csv)
- [Passerelle marché vers business model](annexes/market_to_business_model_bridge.csv)
- [Registre des sources enrichi](annexes/source_register_v2.csv)
- [Matrice qualité des sources enrichie](annexes/source_quality_matrix_v2.csv)
