# EPIC-07 - Reporting, exports et preuves

**Lien**: [Gestion de projet §8](../../documents/07_gestion_de_projet/rendu_principal.md#8-product-backlog-structuré) | [§9 Features](../../documents/07_gestion_de_projet/rendu_principal.md#9-features-par-epic)

## Objectif
Produire des exports CSV/JSON et des preuves de validation (Priorité P1)

## User Stories

| ID | User Story | SP | Sprint | Owner | Issue # |
|---|---|---|---|---|---|
| US-07.1 | Export CSV (alertes/events) | 3 | Sprint 4-5 | Barbara Liskov | |
| US-07.2 | Export JSON (structuré) | 3 | Sprint 5 | Barbara Liskov | |
| US-07.3 | Preuve scénario (lien export) | 3 | Sprint 5 | Margaret Hamilton | |

## Tasks Techniques (US-07.1 - CSV)

- [ ] Génération CSV (Python csv module) - Barbara Liskov
- [ ] Endpoint `GET /export/csv` (FastAPI) - Barbara Liskov
- [ ] Téléchargement fichier - Tim Berners-Lee
- [ ] Log audit export - Radia Perlman
- [ ] Tests export CSV - Margaret Hamilton

## Tasks Techniques (US-07.2 - JSON)

- [ ] Génération JSON structuré - Barbara Liskov
- [ ] Endpoint `GET /export/json` - Barbara Liskov
- [ ] Métadonnées export - Barbara Liskov
- [ ] Tests export JSON - Margaret Hamilton

## Tasks Techniques (US-07.3 - Preuve)

- [ ] Nommage export (timestamp/scénario) - Linus Torvalds
- [ ] Métadonnées scénario - Margaret Hamilton
- [ ] Documentation preuve - Linus Torvalds
- [ ] Capture export + scénario - Margaret Hamilton

## Definition of Ready (US-07.1)

- [ ] Format CSV défini
- [ ] Endpoint `/export` prêt
- [ ] Log audit configuré

## Definition of Done (US-07.1)

- [ ] CSV généré et téléchargeable
- [ ] Log audit de l'export
- [ ] Preuve: fichier CSV exploitable

## Accepatance Criteria

| Critère | Preuve attendue |
|---|---|
| Export CSV | Fichier téléchargé, colonnes correctes |
| Export JSON | JSON structuré, métadonnées |
| Preuve liée | Export rattaché au scénario |
