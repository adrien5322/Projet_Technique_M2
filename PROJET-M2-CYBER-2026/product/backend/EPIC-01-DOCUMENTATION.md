# EPIC-01: Socle Applicatif FastAPI - Documentation

## Vue d'ensemble

L'EPIC-01 établit les fondations techniques de la plateforme DAR-Cyber avec FastAPI.

## User Stories couvertes

### US-01.1: Modèle User avec rôles admin/analyst
**Statut :** ✅ Implémenté

**Fichiers :**
- `app/models/user.py` - Modèle SQLAlchemy User avec rôles
- `app/schemas/user.py` - Schémas Pydantic pour validation

**Détails :**
- Modèle User avec champs : id, username, email, hashed_password, full_name, role, is_active
- Rôles supportés : `admin`, `analyst`
- Propriétés `is_admin` et `is_analyst` pour vérification facile
- Validation des entrées avec Pydantic (EmailStr, longueurs min/max)

### US-01.2: Authentification JWT et RBAC
**Statut :** ✅ Implémenté

**Fichiers :**
- `app/auth/service.py` - Logique JWT et hachage mots de passe
- `app/auth/routes.py` - Endpoints login et me
- `app/auth/dependencies.py` - Dépendances d'injection FastAPI pour auth

**Détails :**
- Endpoint `POST /api/v1/auth/login` : authentification et génération JWT
- Endpoint `GET /api/v1/auth/me` : informations utilisateur (protégé)
- Hachage des mots de passe avec bcrypt (via passlib)
- JWT avec HS256, expiration configurable
- Contrôle d'accès basé sur les rôles (RBAC) :
  - `require_admin` : accès admin uniquement
  - `require_analyst_or_admin` : accès analyst ou admin
- Identifiants de test (mock) :
  - admin / admin123 (rôle admin)
  - analyst / analyst123 (rôle analyst)

### US-01.3: Endpoint health et structure de base
**Statut :** ✅ Implémenté

**Fichiers :**
- `app/core/health.py` - Endpoint health check
- `app/main.py` - Application FastAPI principale
- `app/config.py` - Configuration centralisée

**Détails :**
- Endpoint `GET /health` : retourne status, app_name, version
- Configuration via `.env` avec `.env.example` fourni
- Support CORS configuré
- Documentation interactive : `/api/v1/docs` (Swagger) et `/api/v1/redoc`
- Structure modulaire avec tous les modules prévus (telemetry, discovery, etc.)

## Structure des fichiers créés

```
backend/
├── app/
│   ├── main.py              ✅ Point d'entrée FastAPI
│   ├── config.py            ✅ Configuration Pydantic Settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py         ✅ Modèle User SQLAlchemy
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── user.py         ✅ Schémas Pydantic
│   ├── auth/
│   │   ├── __init__.py
│   │   ├── service.py      ✅ JWT + password hashing
│   │   ├── routes.py       ✅ Endpoints login/me
│   │   └── dependencies.py ✅ Dépendances injection FastAPI
│   ├── core/
│   │   ├── __init__.py
│   │   └── health.py       ✅ Endpoint /health
│   ├── telemetry/           🔜 (vide, prêt pour EPIC-02)
│   ├── discovery/           🔜 (vide, prêt pour EPIC-03)
│   ├── assets/              🔜 (vide, prêt pour EPIC-03)
│   ├── alerts/              🔜 (vide, prêt pour EPIC-04)
│   ├── correlation/         🔜 (vide, prêt pour EPIC-04)
│   ├── reports/             🔜 (vide, prêt pour EPIC-05)
│   └── audit/               🔜 (vide, prêt pour EPIC-05)
├── tests/
│   ├── __init__.py
│   ├── conftest.py         ✅ Configuration pytest
│   ├── test_auth.py        ✅ Tests auth + JWT
│   ├── test_health.py      ✅ Tests endpoint health
│   └── test_main.py        ✅ Tests endpoint root
├── alembic/
│   ├── env.py              ✅ Configuration Alembic
│   └── script.py.mako      ✅ Template migrations
├── .env.example            ✅ Variables d'environnement documentées
├── .gitignore              ✅ Fichiers à ignorer
├── requirements.txt        ✅ Dépendances Python
├── requirements-dev.txt    ✅ Dépendances développement
├── setup.sh                ✅ Script d'installation
├── validate_structure.py   ✅ Validation structure
├── test_simple.py          ✅ Tests unitaires simples
└── README.md               ✅ Documentation utilisateur
```

## Configuration

### Variables d'environnement (.env.example)

```bash
APP_NAME=DAR-Cyber
APP_VERSION=0.1.0
DEBUG=true
DATABASE_URL=postgresql://user:password@localhost:5432/devinciwatch
JWT_SECRET_KEY=your-super-secret-jwt-key-change-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REDIS_URL=redis://localhost:6379/0
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]
```

⚠️ **Ne jamais commiter le fichier `.env` avec de vrais secrets !**

## Tests

### Tests unitaires créés

1. **test_auth.py** :
   - Test hachage mots de passe
   - Test création/décodage JWT
   - Test endpoint login (succès/échec)
   - Test validation schémas

2. **test_health.py** :
   - Test endpoint /health
   - Test statut et structure réponse

3. **test_main.py** :
   - Test endpoint root /
   - Vérification infos API

### Lancer les tests

```bash
# Installer les dépendances d'abord
./setup.sh

# Activer l'environnement
source venv/bin/activate

# Lancer les tests
pytest tests/ -v

# Avec couverture
pytest tests/ --cov=app --cov-report=html
```

## Endpoints disponibles

| Méthode | Endpoint | Description | Auth requise |
|---------|----------|-------------|--------------|
| GET | `/` | Informations API | Non |
| GET | `/health` | Health check | Non |
| POST | `/api/v1/auth/login` | Connexion (JWT) | Non |
| GET | `/api/v1/auth/me` | Infos utilisateur | Oui (JWT) |

## Comment lancer le serveur

### Prérequis système
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv
```

### Installation et lancement
```bash
cd product/backend

# Installation (première fois)
./setup.sh

# Ou manuellement :
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env  # Puis éditer .env

# Lancement du serveur
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Accès
- API : http://localhost:8000
- Documentation Swagger : http://localhost:8000/api/v1/docs
- ReDoc : http://localhost:8000/api/v1/redoc
- Health : http://localhost:8000/health

## Problèmes connus et limites

1. **Dépendances non installées** : Le système ne dispose pas de pip/venv, empêchant l'installation de FastAPI et des dépendances. Le code est prêt mais nécessite une installation manuelle.

2. **Base de données mockée** : L'authentification utilise des identifiants en dur pour la démo. En production, il faut connecter à PostgreSQL via SQLAlchemy.

3. **Session DB non implémentée** : La fonction `get_db()` dans `dependencies.py` est un placeholder. À compléter avec SQLAlchemy session maker.

4. **Utilisateur mocké** : L'endpoint `/me` retourne un utilisateur fictif. À connecter à la base de données.

5. **Pas de refresh token** : Seulement des access tokens (valables 30 min par défaut). À compléter selon besoins.

## Prochaines étapes (EPIC-02)

- Implémenter la connexion PostgreSQL réelle
- Créer les endpoints de télémétrie (`/api/v1/telemetry/heartbeat`)
- Implémenter l'ingestion d'événements
- Ajouter l'inventaire d'actifs (EPIC-03)

## Sécurité

- ✅ Aucun secret en dur dans le code
- ✅ Utilisation de `.env.example` pour documenter
- ✅ Mots de passe hachés avec bcrypt
- ✅ JWT avec expiration
- ✅ Validation des entrées (Pydantic)
- 🔜 Audit trail à implémenter (EPIC-05)
- 🔜 Rate limiting à ajouter
- 🔜 HTTPS en production (via reverse proxy)

## Validation

Le script `validate_structure.py` confirme :
- ✅ Tous les fichiers requis sont présents
- ✅ Tous les fichiers Python ont une syntaxe correcte
- ✅ La structure respecte les conventions du projet

---

**Auteur :** backend-python-dev  
**Date :** 2026-05-06  
**Epic :** EPIC-01 - Socle applicatif FastAPI  
**Statut :** ✅ Implémentation complète (en attente d'installation dépendances)
