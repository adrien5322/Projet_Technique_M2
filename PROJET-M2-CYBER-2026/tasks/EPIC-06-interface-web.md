# EPIC-06 - Interface web et visualisation

**Lien**: [Gestion de projet §8](../../documents/07_gestion_de_projet/rendu_principal.md#8-product-backlog-structuré) | [§9 Features](../../documents/07_gestion_de_projet/rendu_principal.md#9-features-par-epic)

## Objectif
Fournir un dashboard et des vues analyste exploitables (Priorité P1)

## User Stories

| ID | User Story | SP | Sprint | Owner | Issue # |
|---|---|---|---|---|---|
| US-06.1 | Dashboard synthétique | 5 | Sprint 4 | Tim Berners-Lee | |
| US-06.2 | Vues analyste (actifs/events/alertes) | 5 | Sprint 4 | Tim Berners-Lee | |
| US-06.3 | Visualisation enrichie (IP attaquantes) | 3 | Sprint 4 | Tim Berners-Lee | |

## Tasks Techniques (US-06.1 - Dashboard)

- [ ] Définir métriques (events, alertes, endpoints) - Tim Berners-Lee
- [ ] Endpoint `GET /summary` (FastAPI) - Barbara Liskov
- [ ] Composants UI dashboard - Tim Berners-Lee
- [ ] Navigation dashboard - Tim Berners-Lee
- [ ] Tests UI dashboard - Margaret Hamilton

## Tasks Techniques (US-06.2 - Vues analyste)

- [ ] Navigation entre vues - Tim Berners-Lee
- [ ] Vues liste + détail (actifs, events, alertes) - Tim Berners-Lee
- [ ] États vides (empty states) - Tim Berners-Lee
- [ ] Parcours analyste complet - Tim Berners-Lee

## Tasks Techniques (US-06.3 - IP attaquantes)

- [ ] Agrégation IP sources - Ken Thompson
- [ ] Endpoint `/attackers` (API) - Barbara Liskov
- [ ] Vue IP attaquantes (UI) - Tim Berners-Lee
- [ ] Fréquence affichée - Tim Berners-Lee

## Definition of Ready (US-06.1)

- [ ] Composants UI de base
- [ ] Endpoint `/summary` prêt
- [ ] Navigation dashboard prévue

## Definition of Done (US-06.1)

- [ ] Métriques affichées (events, alertes, exports)
- [ ] Navigation fluide
- [ ] Exports visibles
- [ ] Preuve: captures dashboard

## Accepatance Criteria

| Critère | Preuve attendue |
|---|---|
| Dashboard fonctionnel | Métriques clés affichées |
| Parcours analyste | Navigation actifs→events→alertes |
| IP attaquantes | Sources fréquentes visibles |
