# EPIC-01 - Socle applicatif et sécurité

**Lien**: [Gestion de projet §8](../../documents/07_gestion_de_projet/rendu_principal.md#8-product-backlog-structuré) | [§9 Features](../../documents/07_gestion_de_projet/rendu_principal.md#9-features-par-epic)

## Objectif
Poser les bases FastAPI, authentification, rôles, configuration et santé applicative (Priorité P1)

## User Stories

| ID | User Story | SP | Sprint | Owner | Issue # |
|---|---|---|---|---|---|
| US-01.1 | Authentification utilisateur | 5 | Sprint 1 | Barbara Liskov | |
| US-01.2 | Contrôle d'accès (rôles admin/analyst) | 3 | Sprint 1 | Barbara Liskov | |
| US-01.3 | Santé applicative (/health endpoint) | 2 | Sprint 1 | Ken Thompson | |

## Tasks Techniques (US-01.1 - Authentification)

- [ ] Créer modèle `User` (SQLAlchemy) - Barbara Liskov
- [ ] Implémenter route `POST /login` (FastAPI) - Barbara Liskov
- [ ] Gérer JWT token/session - Barbara Liskov
- [ ] Protéger routes privées avec middleware - Ken Thompson
- [ ] Tests unitaires auth - Margaret Hamilton
- [ ] Documentation API auth - Linus Torvalds

## Tasks Techniques (US-01.2 - Rôles)

- [ ] Définir `admin` / `analyst` - Barbara Liskov
- [ ] Middleware contrôle d'accès - Ken Thompson
- [ ] Tests refus d'action - Margaret Hamilton
- [ ] Documentation rôles - Linus Torvalds

## Tasks Techniques (US-01.3 - Santé)

- [ ] Créer endpoint `GET /health` - Ken Thompson
- [ ] Logger erreurs basiques - Ken Thompson
- [ ] Tests endpoint santé - Margaret Hamilton
- [ ] Documentation `/health` - Linus Torvalds

## Definition of Ready (US-01.1)

- [ ] Schéma utilisateur défini
- [ ] Route `/login` créée dans `serveur-soc`
- [ ] Payload JWT prêt
- [ ] Test de connexion initial configuré

## Definition of Done (US-01.1)

- [ ] Connexion valide acceptée
- [ ] Token JWT retourné
- [ ] Route `/me` renvoie utilisateur
- [ ] Accès refusé sans token
- [ ] Preuve: capture login réussi/échoué

## Accepatance Criteria

| Critère | Preuve attendue |
|---|---|
| Connexion valide | Token JWT reçu, 200 OK |
| Connexion invalide | 401 Unauthorized |
| Accès sans token | 403 Forbidden |
| Route `/me` | JSON utilisateur connecté |
