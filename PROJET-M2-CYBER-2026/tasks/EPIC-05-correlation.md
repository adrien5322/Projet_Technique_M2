# EPIC-05 - Corrélation et enrichissement analyste

**Lien**: [Gestion de projet §8](../../documents/07_gestion_de_projet/rendu_principal.md#8-product-backlog-structuré) | [§9 Features](../../documents/07_gestion_de_projet/rendu_principal.md#9-features-par-epic)

## Objectif
Regrouper des événements liés pour améliorer la lisibilité SOC (Priorité P2)

## User Stories

| ID | User Story | SP | Sprint | Owner | Issue # |
|---|---|---|---|---|---|
| US-05.1 | Corrélation IP source | 8 | Sprint 4 | Ken Thompson | |
| US-05.2 | Corrélation temporelle | 8 | Sprint 4 | Ken Thompson | |
| US-05.3 | Vue corrélation | 5 | Sprint 4 | Tim Berners-Lee | |

## Tasks Techniques (US-05.1 - IP)

- [ ] Règle corrélation IP - Ken Thompson
- [ ] Modèle `CorrelationGroup` - Barbara Liskov
- [ ] Association events → groupe - Ken Thompson
- [ ] Endpoint corrélations (API) - Barbara Liskov
- [ ] Vue groupes IP (UI) - Tim Berners-Lee
- [ ] Tests corrélation IP - Margaret Hamilton

## Tasks Techniques (US-05.2 - Temporelle)

- [ ] Paramètre fenêtre temporelle - Ken Thompson
- [ ] Requête temporelle PostgreSQL - Barbara Liskov
- [ ] Scoring simple corrélation - Ken Thompson
- [ ] Tests scénario temporel - Margaret Hamilton

## Tasks Techniques (US-05.3 - Vue)

- [ ] Vue consultation corrélations - Tim Berners-Lee
- [ ] Lien alerte → corrélation - Tim Berners-Lee
- [ ] Explication corrélation (UI) - Tim Berners-Lee

## Definition of Ready (US-05.1)

- [ ] Logique de regroupement codée
- [ ] Requête PostgreSQL prête
- [ ] Vue corrélation prévue

## Definition of Done (US-05.1)

- [ ] Groupe créé pour événements liés
- [ ] IP source affichée
- [ ] Historique consultable
- [ ] Preuve: groupe visible dashboard

## Accepatance Criteria

| Critère | Preuve attendue |
|---|---|
| Corrélation IP | Events liés → groupe créé |
| Corrélation temporelle | Répétition visible fenêtre |
| Vue consultable | Analyste voit groupe + détail |
