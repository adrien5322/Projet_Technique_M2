# DAR-Cyber Backend

Backend FastAPI pour la plateforme de cybersurveillance DAR-Cyber.

## Structure

```
backend/
├── app/
│   ├── main.py              # Point d'entrée FastAPI
│   ├── config.py             # Configuration (Pydantic Settings)
│   ├── models/              # Modèles SQLAlchemy
│   ├── schemas/             # Schémas Pydantic
│   ├── auth/                # Authentification et JWT
│   ├── core/                # Éléments core (health check)
│   └── [autres modules]     # telemetry, discovery, etc.
├── tests/                   # Tests pytest
├── requirements.txt         # Dépendances Python
├── .env.example            # Exemple de configuration
└── setup.sh                # Script d'installation
```

## Installation

### Prérequis
- Python 3.10+
- pip
- PostgreSQL (pour production)
- Redis (pour Celery)

### Étapes

1. **Installer les dépendances système (Ubuntu/Debian) :**
   ```bash
   sudo apt-get update
   sudo apt-get install -y python3-pip python3-venv
   ```

2. **Lancer le script d'installation :**
   ```bash
   cd backend
   ./setup.sh
   ```

3. **Configurer l'environnement :**
   ```bash
   # Éditer .env avec vos paramètres
   nano .env
   ```

4. **Lancer le serveur de développement :**
   ```bash
   source venv/bin/activate
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

## Endpoints Disponibles

### Health Check
- `GET /health` - Vérification de l'état de l'application

### Authentification (US-01.1)
- `POST /api/v1/auth/login` - Connexion et obtention de JWT
  - Identifiants de test : 
    - admin / admin123 (rôle admin)
    - analyst / analyst123 (rôle analyst)
- `GET /api/v1/auth/me` - Informations de l'utilisateur connecté (protégé)

### Root
- `GET /` - Informations sur l'API

## Documentation Interactive

- Swagger UI : http://localhost:8000/api/v1/docs
- ReDoc : http://localhost:8000/api/v1/redoc

## Tests

```bash
source venv/bin/activate
pytest tests/ -v
```

## Configuration

Voir `.env.example` pour toutes les variables disponibles.

**⚠️ Ne jamais commiter le fichier `.env` avec de vrais secrets !**

## EPIC-01: Socle Applicatif

Cette implémentation couvre :
- ✅ US-01.1 : Modèle User avec rôles admin/analyst
- ✅ US-01.2 : Authentification JWT et RBAC
- ✅ US-01.3 : Endpoint health et structure de base

## Prochaines Étapes

- EPIC-02 : Télémétrie et Heartbeat
- EPIC-03 : Inventaire d'actifs
- EPIC-04 : Détection et alertes
