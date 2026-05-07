# Rapport DevOps - DevinciWatch
**Date**: 6 Mai 2026  
**Ingénieur**: DevOps Engineer  
**Epic**: EPIC-01 - Socle applicatif

---

## 1. Fichiers Docker créés/modifiés

### Fichiers créés :

| Fichier | Description |
|---------|-------------|
| `product/backend/Dockerfile` | Image Docker pour le backend FastAPI (Python 3.11-slim) |
| `product/backend/requirements.txt` | Dépendances Python (FastAPI, SQLAlchemy, Redis, etc.) |
| `product/backend/.env.example` | Exemple de variables d'environnement (sans secrets réels) |
| `product/backend/.dockerignore` | Fichiers exclus du build Docker |
| `product/docker-compose.yml` | Orchestration des services (backend, postgres, redis) |
| `product/docker-compose.override.yml` | Configuration de développement (volumes, debug) |
| `product/.dockerignore` | Exclusions pour le build à la racine |
| `product/.gitignore` | Fichiers à ignorer par Git (inclut .env, venv, etc.) |
| `product/Makefile` | Raccourcis pour les commandes courantes |
| `product/scripts/start.sh` | Script de démarrage des services |
| `product/scripts/setup.sh` | Script d'initialisation (DB, migrations) |
| `product/backend/app/main.py` | Point d'entrée FastAPI avec endpoints de base |
| `product/backend/tests/test_main.py` | Tests unitaires pour l'endpoint principal |
| `product/backend/alembic.ini` | Configuration Alembic (migrations DB) |
| `product/backend/alembic/env.py` | Script d'environnement Alembic |
| `product/README.md` | Documentation du dossier product |
| `.github/workflows/ci.yml` | Pipeline CI (lint, test, build, security) |
| `.github/workflows/cd.yml` | Pipeline CD (deploy staging/production) |
| `docs/CI-CD.md` | Documentation détaillée CI/CD |

### Fichiers modifiés :
- `product/backend/.env.example` (enrichi avec toutes les variables)
- `product/backend/app/config.py` (déjà existant, vérifié)

---

## 2. Services configurés

### Services Docker Compose :

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| **backend** | Build local (Dockerfile) | 8000 | API FastAPI avec uvicorn |
| **postgres** | postgres:16-alpine | 5432 | Base de données PostgreSQL |
| **redis** | redis:7-alpine | 6379 | Cache et broker de messages |

### Configuration des services :

#### Backend (FastAPI)
- **Build context** : `./backend`
- **Commande** : `uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload`
- **Variables d'environnement** : Chargées depuis `backend/.env`
- **Volumes** : Code monté en volume pour le hot-reload
- **Healthcheck** : Endpoint `/health`
- **Dépendances** : Attend que postgres et redis soient healthy

#### PostgreSQL
- **Image** : `postgres:16-alpine`
- **Variables** : `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB`
- **Volume persistant** : `postgres-data`
- **Healthcheck** : `pg_isready`

#### Redis
- **Image** : `redis:7-alpine`
- **Commande** : `redis-server --appendonly yes`
- **Volume persistant** : `redis-data`
- **Healthcheck** : `redis-cli ping`

### Réseau et Volumes :
- **Réseau** : `devinciwatch-network` (bridge)
- **Volumes** :
  - `postgres-data` : Données PostgreSQL persistantes
  - `redis-data` : Données Redis persistantes

---

## 3. Commandes de lancement

### Configuration initiale (première fois) :
```bash
cd product/
./scripts/setup.sh
```
Ce script va :
- Vérifier les prérequis (Docker, Docker Compose)
- Créer le fichier `.env` depuis `.env.example`
- Construire les images Docker
- Démarrer PostgreSQL et Redis
- Attendre que les services soient prêts
- Initialiser la base de données (migrations Alembic)

### Démarrage rapide :
```bash
# Avec Makefile (recommandé)
make up

# Avec le script
./scripts/start.sh --detach

# Avec docker compose directement
docker compose up -d
```

### Développement (avec logs) :
```bash
# Avec Makefile
make

# Avec le script
./scripts/start.sh

# Avec docker compose
docker compose up
```

### Reconstruction après modification du Dockerfile :
```bash
./scripts/start.sh --build
# ou
make build && make up
```

### Voir les logs :
```bash
make logs
# ou
docker compose logs -f
# ou pour un service spécifique
docker compose logs -f backend
```

### Arrêter les services :
```bash
make down
# ou
docker compose down
```

⚠️ **Supprimer aussi les volumes (données perdues)** :
```bash
docker compose down -v
```

### Accès aux services :
- **API** : http://localhost:8000
- **Documentation Swagger** : http://localhost:8000/docs
- **Documentation ReDoc** : http://localhost:8000/redoc
- **Health Check** : http://localhost:8000/health
- **PostgreSQL** : localhost:5432
- **Redis** : localhost:6379

---

## 4. Problèmes rencontrés et solutions

### Problème 1 : Structure backend existante mais incomplète
**Description** : Le dossier `backend/` existait avec des sous-dossiers (alerts, auth, etc.) mais sans fichiers Python réels (sauf `config.py` et `__init__.py`).

**Solution** : 
- Création du fichier `app/main.py` avec un point d'entrée FastAPI minimal
- Création de tests de base dans `tests/test_main.py`
- Vérification que `config.py` utilise correctement Pydantic Settings

### Problème 2 : Absence de requirements.txt
**Description** : Aucun fichier de dépendances Python n'était présent.

**Solution** : Création de `requirements.txt` avec les dépendances essentielles :
- FastAPI + Uvicorn
- SQLAlchemy + Psycopg2 (PostgreSQL)
- Pydantic Settings
- Redis + Celery
- JWT (python-jose, passlib)
- Outils de test (pytest, httpx)

### Problème 3 : Configuration Alembic manquante
**Description** : Le dossier `alembic/` existait mais sans fichier `alembic.ini` ni `env.py`.

**Solution** : Création des fichiers de configuration Alembic minimaux pour permettre les migrations.

### Problème 4 : Fichier .env.example incomplet
**Description** : Le fichier existant ne documentait pas toutes les variables nécessaires.

**Solution** : Enrichissement du fichier avec :
- Toutes les variables de configuration
- Commentaires explicatifs
- Sections claires (Application, Database, JWT, Redis, etc.)
- Avertissements sur les secrets

### Problème 5 : Présence d'un venv dans le dépôt
**Description** : Un dossier `backend/venv/` était présent et aurait pu être commité.

**Solution** : Ajout de `backend/venv/` dans `.gitignore` pour éviter de versionner les environnements virtuels.

### Problème 6 : Pas de healthcheck dans l'application
**Description** : Le Dockerfile et docker-compose référençaient un endpoint `/health` qui n'existait pas.

**Solution** : Ajout de l'endpoint `/health` dans `app/main.py` retournant un JSON avec le statut de santé.

---

## 5. Variables d'environnement documentées

### Fichier `backend/.env.example` :

```bash
# Application
APP_NAME=DevinciWatch
APP_VERSION=0.1.0
DEBUG=true

# Server
HOST=0.0.0.0
PORT=8000

# Database (PostgreSQL)
DATABASE_URL=postgresql://devinciwatch:devinciwatch@postgres:5432/devinciwatch
POSTGRES_USER=devinciwatch
POSTGRES_PASSWORD=devinciwatch_secure_password_change_me
POSTGRES_DB=devinciwatch
POSTGRES_PORT=5432

# JWT Security
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production-min-32-chars
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PORT=6379

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","http://localhost"]

# Logging
LOG_LEVEL=info
```

⚠️ **Important** : 
- Ne jamais commiter le fichier `.env` avec de vraies valeurs
- Changer `JWT_SECRET_KEY` et `POSTGRES_PASSWORD` en production
- Utiliser des secrets forts (générer avec `openssl rand -hex 32`)

---

## 6. CI/CD Pipeline

### CI Pipeline (`.github/workflows/ci.yml`) :

**Jobs :**
1. **lint** : Vérifie le code (flake8, black, isort)
2. **test** : Tests unitaires avec pytest + services PostgreSQL/Redis
3. **build** : Construction de l'image Docker
4. **security** : Scan de vulnérabilités (Trivy) + secrets (TruffleHog)
5. **secrets-check** : Vérifie l'absence de fichiers `.env` et de secrets exposés

**Déclenchement :**
- Push sur `main` ou `develop`
- Pull Request vers `main` ou `develop`

### CD Pipeline (`.github/workflows/cd.yml`) :

**Jobs :**
1. **deploy-staging** : Déploiement en staging (sur `main`)
2. **deploy-production** : Déploiement en production (sur tags `v*`)
3. **notify** : Notification du statut

**Environnements :**
- `staging` : Déploiement automatique depuis `main`
- `production` : Déploiement manuel ou par tag

**Secrets GitHub requis :**
- `STAGING_HOST`, `STAGING_SSH_KEY`
- `PRODUCTION_HOST`, `PRODUCTION_SSH_KEY`
- `CODECOV_TOKEN` (optionnel)

---

## 7. Risques opérationnels

### Risques identifiés :

| Risque | Impact | Mitigation |
|--------|--------|------------|
| **Fuite de secrets** | Critique | `.env` dans `.gitignore`, scan TruffleHog en CI |
| **Dépendances vulnérables** | Élevé | Scan Trivy en CI, mise à jour régulière |
| **Perte de données (volumes)** | Élevé | Sauvegardes régulières de `postgres-data` |
| **Déploiement sans tests** | Moyen | CI obligatoire avant merge (branch protection) |
| **Accès non autorisé** | Critique | JWT secret fort, CORS configuré, HTTPS en prod |
| **Ressources Docker épuisées** | Moyen | Limites de ressources dans docker-compose |
| **Conflits de ports** | Faible | Documentation claire des ports utilisés |

### Recommandations :

1. **Sécurité** :
   - Changer tous les mots de passe par défaut avant production
   - Activer le chiffrement TLS/HTTPS
   - Implémenter le rate limiting
   - Audit régulier des dépendances

2. **Monitoring** :
   - Ajouter Prometheus/Grafana pour le monitoring
   - Centraliser les logs (ELK stack ou similaire)
   - Configurer des alertes sur les healthchecks

3. **Sauvegardes** :
   - Script de backup automatique pour PostgreSQL
   - Sauvegarde régulière des volumes Docker
   - Test de restauration périodique

4. **Haute disponibilité** :
   - Multi-replicas pour le backend (avec load balancer)
   - Cluster PostgreSQL (master-slave)
   - Redis Sentinel ou Cluster

---

## 8. Prochaines étapes

### Pour le développeur backend :
1. Implémenter les routeurs FastAPI dans chaque module (`auth/`, `alerts/`, etc.)
2. Créer les modèles SQLAlchemy dans `models/`
3. Ajouter les schémas Pydantic dans `schemas/`
4. Écrire les tests unitaires pour chaque module
5. Configurer les migrations Alembic pour les modèles

### Pour le DevOps :
1. Configurer les secrets GitHub pour la CI/CD
2. Mettre en place l'environnement de staging
3. Configurer le monitoring et les alertes
4. Documenter le processus de déploiement réel
5. Mettre en place les sauvegardes automatiques

### Pour la sécurité :
1. Audit du code avec `security-tech-lead`
2. Test de pénétration du lab
3. Validation de la configuration Docker (non-root, etc.)
4. Scan de vulnérabilités régulier

---

## Conclusion

Le socle applicatif DevinciWatch est maintenant **opérationnel et reproductible**. Un simple `./scripts/setup.sh` suivi de `./scripts/start.sh` permet de lancer tout l'environnement en local.

La CI/CD est configurée pour automatiser les tests, le build et le déploiement, avec une attention particulière portée sur la sécurité (aucun secret exposé, scans automatiques).

**Le lab est prêt pour le développement des fonctionnalités EPIC-01.**
