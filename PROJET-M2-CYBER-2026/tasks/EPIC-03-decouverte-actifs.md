# EPIC-03 - Découverte réseau et actifs

**Lien**: [Gestion de projet §8](../../documents/07_gestion_de_projet/rendu_principal.md#8-product-backlog-structuré) | [§9 Features](../../documents/07_gestion_de_projet/rendu_principal.md#9-features-par-epic)

## Objectif
Identifier actifs, ports et services observables dans le lab (Priorité P1)

## User Stories

| ID | User Story | SP | Sprint | Owner | Issue # |
|---|---|---|---|---|---|
| US-03.1 | Scan IP (découverte) | 5 | Sprint 2-3 | Ken Thompson | |
| US-03.2 | Inventaire actifs | 5 | Sprint 3 | Barbara Liskov | |
| US-03.3 | Ports et services | 3 | Sprint 3 | Ken Thompson | |

## Tasks Techniques (US-03.1 - Scan IP)

- [ ] Scan contrôlé (limites IP lab) - Ken Thompson
- [ ] Modèle `Asset` PostgreSQL - Barbara Liskov
- [ ] Route `POST /scan` (FastAPI) - Ken Thompson
- [ ] Association IP → Asset - Barbara Liskov
- [ ] Vue liste actifs (API + UI) - Tim Berners-Lee
- [ ] Tests scan contrôlé - Margaret Hamilton

## Tasks Techniques (US-03.2 - Inventaire)

- [ ] Création actif depuis événements - Barbara Liskov
- [ ] Route `GET /assets` (API) - Barbara Liskov
- [ ] Vue détail actif (UI) - Tim Berners-Lee
- [ ] Mise à jour actif (heartbeat/events) - Ken Thompson

## Tasks Techniques (US-03.3 - Ports/Services)

- [ ] Scan ports (nmap/ scapy simplifié) - Ken Thompson
- [ ] Modèle `PortFinding` - Barbara Liskov
- [ ] Association actif → ports - Ken Thompson
- [ ] Affichage ports/services - Tim Berners-Lee

## Definition of Ready (US-03.1)

- [ ] Plage IP lab définie
- [ ] Scan contrôlé autorisé
- [ ] Modèle asset lié
- [ ] Affichage liste prévu

## Definition of Done (US-03.1)

- [ ] Actif créé après scan
- [ ] IP/ports/services visibles
- [ ] Scan limité au lab Docker
- [ ] Preuve: actif dans dashboard

## Accepatance Criteria

| Critère | Preuve attendue |
|---|---|
| Actifs visibles | IP + dernière observation |
| Ports associés | Actif montre ports ouverts |
| Scan limité | Pas de scan hors lab Docker |
