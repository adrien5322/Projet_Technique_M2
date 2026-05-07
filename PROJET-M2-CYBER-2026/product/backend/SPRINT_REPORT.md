# Rapport de Sprint — DAR-Cyber

**Date :** 07/05/2026
**Projet :** DAR-Cyber (ex-DevinciWatch)
**Phase :** Socle applicatif + Interface web + Correction infrastructure

---

## Résumé

Le sprint a consolidé le socle applicatif FastAPI, sécurisé l'authentification, rendu l'infrastructure Docker fiable et livré l'interface web SOC complète avec dashboard, assets, events, alerts et attackers.

---

## Métriques

| Métrique | Valeur |
|---|---|
| Routes API/UI | 49 endpoints |
| Fichiers de test | 19 |
| Fonctions de test | 465 |
| Modules backend | 12 (auth, telemetry, events, alerts, assets, audit, correlation, discovery, reports, dashboard, discovery, middleware) |
| Modèles SQLAlchemy | 9 (user, asset, alert, audit, correlation, event, telemetry, port_finding, correlation_group) |
| Schémas Pydantic | 11 |
| Templates HTML | 7 |
| Migrations Alembic | 6 |
| Conteneurs Docker | 3 (backend, postgres, redis) |

---

## EPICs couvertes

### EPIC-01 — Socle applicatif et sécurité (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-01.1 Authentification utilisateur | ✅ Terminé | JWT + bcrypt + login/me |
| US-01.2 Contrôle d'accès RBAC | ✅ Terminé | Rôles admin/analyst + dépendances |
| US-01.3 Santé applicative | ✅ Terminé | /health + / avec métadonnées |

### EPIC-02 — Collection endpoint et télémétrie (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-02.1 Heartbeat endpoint | ✅ Terminé | POST /telemetry/heartbeat + persistance |
| US-02.2 Events ingestion | ✅ Terminé | POST /events + GET /events |
| US-02.3 Auth agent (secret) | ✅ Terminé | X-Agent-Secret header + middleware |

### EPIC-03 — Découverte réseau et actifs (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-03.1 Scan IP | ✅ Terminé | POST /discovery/scan avec nmap |
| US-03.2 Inventaire actifs | ✅ Terminé | CRUD assets + liste UI |
| US-03.3 Ports et services | ✅ Terminé | Modèle PortFinding + association |

### EPIC-04 — Détection et alertes (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-04.x Règles de détection | ✅ Terminé | Service + routes alerts |
| US-04.x Gestion alertes | ✅ Terminé | CRUD + changement statut via UI |

### EPIC-05 — Corrélation (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-05.x Corrélation d'événements | ✅ Terminé | Routes + service + groupes |

### EPIC-06 — Interface web et visualisation (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-06.1 Dashboard synthétique | ✅ Terminé | Métriques, graphique activité, alertes récentes |
| US-06.2 Vues analyste | ✅ Terminé | Pages Assets, Events, Alerts |
| US-06.3 IP attaquantes | ✅ Terminé | Top attackers + scoring |

### EPIC-07 — Reporting, exports et preuves (P1)
| User Story | Statut | Notes |
|---|---|---|
| US-07.1 Export CSV | ✅ Terminé | 8 endpoints d'export |
| US-07.2 Export JSON | ✅ Terminé | Export structuré avec métadonnées |
| US-07.3 Preuve scénario | ✅ Terminé | Métadonnées + audit |

---

## Travail réalisé dans le sprint

### Infrastructure Docker
- Installation et configuration de Docker (v29.4.3)
- docker-compose.yml avec 3 services (backend, postgres:16-alpine, redis:7-alpine)
- Healthchecks sur tous les services
- Volumes persistants pour PostgreSQL et Redis
- Fichier d'override pour le développement local

### Base de données
- PostgreSQL initialisé avec migrations Alembic
- 6 migrations créant toutes les tables (users, telemetry_heartbeats, assets, events, alerts, audit, port_findings, correlation_groups)
- Correction des IDs de révision pour compatibilité PostgreSQL (varchar(32))

### Authentification
- Login JWT + bcrypt via `/api/v1/auth/login`
- Route `/api/v1/auth/me` pour récupérer l'utilisateur connecté
- RBAC : dépendances `require_admin` et `require_analyst_or_admin`
- Auth agent via `X-Agent-Secret` header
- Rate limiter (60 req/min/IP) pour les endpoints agent

### Interface Web (Jinja2 + Starlette)
- 7 templates HTML (base, login, dashboard, assets, events, alerts, attackers)
- Mise à jour de `ui.py` pour compatibilité Starlette 1.0.0
- Auth par cookie `access_token` pour les pages server-rendered
- Synchronisation localStorage → cookie pour la persistence

### Corrections de bugs
| Bug | Cause | Fix |
|---|---|---|
| 404 sur `/dashboard` | Pas de cookie d'auth pour les pages server-rendered | Ajout lecture cookie dans `get_current_user` |
| 404 sur `/api/v1/dashboard/*` | Routeur dashboard API jamais inclus dans `main.py` | Ajout de `app.include_router(dashboard_api_router)` |
| 404 sur `/api/v1/assets` | Double prefix dans `main.py` | Suppression du prefix dupliqué |
| Erreur JS sur Assets | Réponse `{items: [...]}` traitée comme tableau | Extraction `response.items` |
| Erreur JS sur Events | Réponse `{events: [...]}` traitée comme tableau | Extraction `response.events` |
| Erreur JS sur Alerts | Réponse `{items: [...]}` traitée comme tableau | Extraction `response.items` |
| 500 sur `/me` avec email `.local` | email-validator rejette les TLDs spéciaux | Changement pour `@example.com` |
| 422 login en form-urlencoded | Pydantic attend du JSON | Changement Content-Type → application/json |

### Sécurité (P0)
- Mots de passe hardcodés supprimés (`app/auth/routes.py`)
- Connexion base de données réelle (plus de `yield None`)
- `JWT_SECRET_KEY` requis (pas de valeur par défaut)
- `DATABASE_URL` sans défaut avec credentials
- `.env` dans `.gitignore`
- Audit trail implémenté

### Renommage du projet
- `DevinciWatch` → `DAR-Cyber` dans tous les fichiers source
- Templates, config, tests, docs, scripts (30+ fichiers)

---

## Données techniques

### Routes API par module

| Module | Routes |
|---|---|
| Auth | 2 |
| Telemetry | 5 |
| Events | 3 |
| Alerts | 6 |
| Assets | 5 |
| Audit | 2 |
| Correlation | 5 |
| Dashboard (API) | 3 |
| Dashboard (UI) | 6 |
| Discovery | 3 |
| Reports | 8 |
| Core / Health | 1 |
| Root | 1 |
| **Total** | **49** |

### Répartition des tests

| Fichier | Tests |
|---|---|
| test_discovery.py | 66 |
| test_telemetry.py | 57 |
| test_correlation.py | 53 |
| test_reports.py | 50 |
| test_events.py | 49 |
| test_dashboard.py | 46 |
| test_auth.py | 29 |
| test_alerts.py | 29 |
| test_db.py | 17 |
| test_agent_auth.py | 17 |
| test_config.py | 14 |
| test_rate_limiter.py | 13 |
| test_audit.py | 13 |
| test_dashboard_ui.py | 8 |
| test_health.py | 3 |
| test_main.py | 1 |
| **Total** | **465** |

---

## Configuration d'accès

- **Dashboard :** `http://192.168.153.150:8000/dashboard/login`
- **API Docs :** `http://192.168.153.150:8000/docs`
- **Health :** `http://192.168.153.150:8000/health`
- **Comptes test :** `admin` / `analyst` (mot de passe : `admin12345` / `analyst12345`)

---

## Prochaines étapes

1. Exécuter la suite de tests complète (465 tests)
2. Développer les scénarios cyber pour la démonstration
3. Préparer le lab Docker avec endpoint simulé et attaquant
4. Documentation utilisateur et déploiement
5. Audit de sécurité final avant livraison
