# DAR-Cyber - Product

Ce dossier contient le code source du produit DAR-Cyber, une plateforme SOC (Security Operations Center).

## Structure du projet

```
product/
├── backend/                 # Backend FastAPI
│   ├── app/                # Code de l'application
│   │   ├── alerts/         # Module Alertes
│   │   ├── assets/         # Module Assets
│   │   ├── audit/          # Module Audit
│   │   ├── auth/           # Module Authentification
│   │   ├── core/           # Configuration centrale
│   │   ├── correlation/   # Module Corrélation
│   │   ├── discovery/      # Module Découverte
│   │   ├── reports/        # Module Rapports
│   │   ├── telemetry/      # Module Télémétrie
│   │   ├── config.py       # Configuration (Pydantic Settings)
│   │   └── main.py         # Point d'entrée FastAPI
│   ├── tests/              # Tests pytest
│   ├── alembic/            # Migrations de base de données
│   ├── .env.example        # Exemple de variables d'environnement
│   ├── requirements.txt    # Dépendances Python
│   └── Dockerfile          # Image Docker du backend
├── scripts/                # Scripts de déploiement et d'initialisation
│   ├── start.sh           # Démarrage des services
│   └── setup.sh           # Configuration initiale
├── docker-compose.yml      # Orchestration des services
├── docker-compose.override.yml  # Configuration de développement
└── .dockerignore          # Fichiers exclus du build Docker
```

## Prérequis

- Docker (version 20.10+)
- Docker Compose (version 2.0+)
- (Optionnel) Python 3.11+ pour le développement local

## Démarrage rapide

### 1. Configuration initiale (première fois)

```bash
cd product/
./scripts/setup.sh
```

Ce script va :
- Vérifier les prérequis
- Créer le fichier `.env` à partir de `.env.example`
- Construire les images Docker
- Démarrer PostgreSQL et Redis
- Initialiser la base de données

### 2. Démarrer l'application

```bash
# Mode détaché (arrière-plan)
./scripts/start.sh --detach

# Mode développement (avec logs)
./scripts/start.sh --build
```

### 3. Accéder à l'application

- **API**: http://localhost:8000
- **Documentation Swagger**: http://localhost:8000/docs
- **Documentation ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

### 4. Arrêter l'application

```bash
docker compose down
```

Pour supprimer aussi les volumes (⚠️ supprime les données) :
```bash
docker compose down -v
```

## Variables d'environnement

Copiez `.env.example` vers `.env` et ajustez les valeurs :

```bash
cp backend/.env.example backend/.env
```

**Variables importantes :**
- `DATABASE_URL` : URL de connexion PostgreSQL
- `REDIS_URL` : URL de connexion Redis
- `JWT_SECRET_KEY` : Clé secrète pour les tokens JWT (⚠️ changer en production)
- `DEBUG` : Mode debug (true/false)

## Commandes utiles

### Voir les logs
```bash
docker compose logs -f [service]
# Exemple: docker compose logs -f backend
```

### Exécuter des commandes dans un conteneur
```bash
docker compose exec backend bash
docker compose exec postgres psql -U devinciwatch
```

### Migrations de base de données (Alembic)
```bash
# Créer une migration
docker compose run --rm backend alembic revision --autogenerate -m "Description"

# Appliquer les migrations
docker compose run --rm backend alembic upgrade head

# Annuler la dernière migration
docker compose run --rm backend alembic downgrade -1
```

### Tests
```bash
# Exécuter les tests dans le conteneur
docker compose run --rm backend pytest tests/ -v

# Avec couverture de code
docker compose run --rm backend pytest tests/ --cov=app --cov-report=html
```

## Développement local (sans Docker)

```bash
cd backend/
python -m venv venv
source venv/bin/activate  # ou `venv\Scripts\activate` sur Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## CI/CD

Le projet utilise GitHub Actions pour :
- **CI** (`.github/workflows/ci.yml`) : Lint, tests, build Docker, scan de sécurité
- **CD** (`.github/workflows/cd.yml`) : Déploiement en staging/production

## Services Docker

| Service   | Description                    | Port par défaut |
|-----------|--------------------------------|-----------------|
| backend   | API FastAPI                    | 8000            |
| postgres  | Base de données PostgreSQL     | 5432            |
| redis     | Cache et broker de messages    | 6379            |

## Réseaux et Volumes

- **Réseau** : `devinciwatch-network` (bridge)
- **Volumes** :
  - `postgres-data` : Données PostgreSQL persistantes
  - `redis-data` : Données Redis persistantes

## Sécurité

⚠️ **Ne jamais commiter de fichier `.env` avec de vraies valeurs secrètes !**

Le fichier `.env` est dans `.gitignore` et `.dockerignore`.

## License

Propriétaire - DAR-Cyber Project
