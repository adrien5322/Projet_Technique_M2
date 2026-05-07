# DevinciWatch - Variables d'environnement

## 📋 Résumé des variables

Ce document liste toutes les variables d'environnement utilisées par DevinciWatch.

## Fichier source : `product/backend/.env.example`

---

## 🔧 Application

| Variable | Défaut | Description |
|----------|--------|-------------|
| `APP_NAME` | DevinciWatch | Nom de l'application |
| `APP_VERSION` | 0.1.0 | Version de l'application |
| `DEBUG` | true | Mode debug (true/false) |
| `HOST` | 0.0.0.0 | Adresse d'écoute |
| `PORT` | 8000 | Port de l'API |

---

## 🗄️ Base de données (PostgreSQL)

| Variable | Défaut | Description |
|----------|--------|-------------|
| `DATABASE_URL` | postgresql://devinciwatch:... | URL complète de connexion |
| `POSTGRES_USER` | devinciwatch | Utilisateur PostgreSQL |
| `POSTGRES_PASSWORD` | devinciwatch_secure_... | Mot de passe PostgreSQL ⚠️ |
| `POSTGRES_DB` | devinciwatch | Nom de la base de données |
| `POSTGRES_PORT` | 5432 | Port PostgreSQL |

**Format DATABASE_URL :**
```
postgresql://<user>:<password>@<host>:<port>/<database>
```

**En Docker :**
```
postgresql://devinciwatch:password@postgres:5432/devinciwatch
```

**En local (hors Docker) :**
```
postgresql://devinciwatch:password@localhost:5432/devinciwatch
```

---

## 🔐 JWT Security

| Variable | Défaut | Description |
|----------|--------|-------------|
| `JWT_SECRET_KEY` | your-super-secret... | Clé secrète JWT ⚠️ |
| `JWT_ALGORITHM` | HS256 | Algorithme de chiffrement |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | 30 | Durée de validité du token (minutes) |

⚠️ **Sécurité** : 
- `JWT_SECRET_KEY` doit faire au moins 32 caractères
- Générer une clé forte : `openssl rand -hex 32`
- **Jamais de clé faible en production !**

---

## 📦 Redis (Cache & Message Broker)

| Variable | Défaut | Description |
|----------|--------|-------------|
| `REDIS_URL` | redis://redis:6379/0 | URL de connexion Redis |
| `REDIS_PORT` | 6379 | Port Redis |

**Format REDIS_URL :**
```
redis://<host>:<port>/<db_number>
```

---

## 🌐 CORS (Cross-Origin Resource Sharing)

| Variable | Défaut | Description |
|----------|--------|-------------|
| `CORS_ORIGINS` | ["http://localhost:3000",...] | Origins autorisées (JSON array) |

**Exemple :**
```bash
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000","https://app.devinciwatch.com"]
```

---

## 📝 Logging

| Variable | Défaut | Description |
|----------|--------|-------------|
| `LOG_LEVEL` | info | Niveau de log (debug/info/warning/error/critical) |

---

## 🚀 Features (Optionnelles)

| Variable | Défaut | Description |
|----------|--------|-------------|
| `ENABLE_SWAGGER` | true | Activer Swagger UI (/docs) |
| `ENABLE_REDOC` | true | Activer ReDoc (/redoc) |
| `RATE_LIMIT_PER_MINUTE` | 100 | Limite de requêtes par minute |

---

## 🐳 Variables Docker Compose

Ces variables sont utilisées dans `docker-compose.yml` :

| Variable | Description |
|----------|-------------|
| `POSTGRES_USER` | Transmis au service postgres |
| `POSTGRES_PASSWORD` | Transmis au service postgres ⚠️ |
| `POSTGRES_DB` | Transmis au service postgres |
| `POSTGRES_PORT` | Mapping de port hôte |
| `REDIS_PORT` | Mapping de port hôte |
| `PORT` | Mapping de port pour le backend |

---

## 📝 Exemple de fichier `.env`

```bash
# Application
APP_NAME=DevinciWatch
APP_VERSION=0.1.0
DEBUG=true
HOST=0.0.0.0
PORT=8000

# Database
DATABASE_URL=postgresql://devinciwatch:mypassword@postgres:5432/devinciwatch
POSTGRES_USER=devinciwatch
POSTGRES_PASSWORD=my_secure_password_123
POSTGRES_DB=devinciwatch
POSTGRES_PORT=5432

# JWT
JWT_SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Redis
REDIS_URL=redis://redis:6379/0
REDIS_PORT=6379

# CORS
CORS_ORIGINS=["http://localhost:3000","http://localhost:8000"]

# Logging
LOG_LEVEL=info
```

---

## ⚠️ Sécurité - Checklist

- [ ] `JWT_SECRET_KEY` changé (min 32 chars)
- [ ] `POSTGRES_PASSWORD` changé (mot de passe fort)
- [ ] `DEBUG=false` en production
- [ ] `CORS_ORIGINS` restreint en production
- [ ] Fichier `.env` dans `.gitignore`
- [ ] Pas de secrets en dur dans le code
- [ ] Scan de sécurité activé en CI

---

## 🔄 Générer une clé JWT secrète

```bash
# Méthode 1 : OpenSSL (recommandé)
openssl rand -hex 32

# Méthode 2 : Python
python -c "import secrets; print(secrets.token_hex(32))"
```

---

## 📖 Références

- [Pydantic Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- [FastAPI Configuration](https://fastapi.tiangolo.com/advanced/settings/)
- [PostgreSQL Docker](https://hub.docker.com/_/postgres)
- [Redis Docker](https://hub.docker.com/_/redis)
