# EPIC-04 - Détection, alertes et audit

**Lien**: [Gestion de projet §8](../../documents/07_gestion_de_projet/rendu_principal.md#8-product-backlog-structuré) | [§9 Features](../../documents/07_gestion_de_projet/rendu_principal.md#9-features-par-epic)

## Objectif
Générer, consulter et tracer les alertes et actions sensibles (Priorité P1)

## User Stories

| ID | User Story | SP | Sprint | Owner | Issue # |
|---|---|---|---|---|---|
| US-04.1 | Génération alerte (règle simple) | 5 | Sprint 3 | Ken Thompson | |
| US-04.2 | Cycle de vie alertes | 3 | Sprint 3 | Tim Berners-Lee | |
| US-04.3 | Audit trail | 3 | Sprint 3 | Radia Perlman | |

## Tasks Techniques (US-04.1 - Détection)

- [ ] Règle simple (ex: port scan, brute force) - Ken Thompson
- [ ] Worker Celery détection - Ken Thompson
- [ ] Modèle `Alert` PostgreSQL - Barbara Liskov
- [ ] Route `POST /detect` (FastAPI) - Ken Thompson
- [ ] Persistance alerte - Barbara Liskov
- [ ] Tests scénario suspect → alerte - Margaret Hamilton

## Tasks Techniques (US-04.2 - Alertes)

- [ ] Endpoints liste/détail alertes - Tim Berners-Lee
- [ ] Vue alertes (UI) - Tim Berners-Lee
- [ ] Changement statut alerte - Tim Berners-Lee
- [ ] Tests UI alertes - Margaret Hamilton

## Tasks Techniques (US-04.3 - Audit)

- [ ] Modèle `AuditLog` - Barbara Liskov
- [ ] Logger connexions/exports/actions - Radia Perlman
- [ ] Endpoint `/audit` (API) - Barbara Liskov
- [ ] Vue audit (UI) - Tim Berners-Lee

## Definition of Ready (US-04.1)

- [ ] Règle simple codée
- [ ] Worker Celery configuré
- [ ] Modèle alerte créé
- [ ] Scénario suspect prêt

## Definition of Done (US-04.1)

- [ ] Alerte générée dans le lab
- [ ] Visible dans dashboard
- [ ] Statut modifiable
- [ ] Log audit créé
- [ ] Preuve: alerte + export CSV

## Accepatance Criteria

| Critère | Preuve attendue |
|---|---|
| Alerte générée | Scénario suspect → alerte visible |
| Alerte consultable | Dashboard affiche détail alerte |
| Audit loggé | Action sensible dans journal |
