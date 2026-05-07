# DevinciWatch - Quickstart (DevOps)

## 🚀 Démarrage en 3 minutes

### Prérequis
- Docker + Docker Compose installés
- Git

### 1. Configuration initiale
```bash
cd product/
./scripts/setup.sh
```

### 2. Démarrer l'application
```bash
./scripts/start.sh --detach
# ou simplement : make up
```

### 3. Accéder à l'API
- **Swagger Docs** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/health

---

## 📁 Structure créée

```
product/
├── backend/
│   ├── Dockerfile          ✓ Image FastAPI
│   ├── requirements.txt    ✓ Dépendances Python
│   ├── .env.example       ✓ Variables d'environnement
│   ├── app/
│   │   └── main.py        ✓ Point d'entrée FastAPI
│   ├── tests/
│   │   └── test_main.py   ✓ Tests de base
│   └── alembic/           ✓ Migrations DB
├── scripts/
│   ├── setup.sh           ✓ Configuration initiale
│   └── start.sh           ✓ Démarrage services
├── docker-compose.yml          ✓ Orchestration
├── docker-compose.override.yml ✓ Config dev
├── Makefile                    ✓ Raccourcis
└── README.md                   ✓ Documentation
```

**CI/CD :**
```
.github/workflows/
├── ci.yml  ✓ Pipeline CI (lint, test, build, security)
└── cd.yml  ✓ Pipeline CD (deploy staging/production)
```

---

## 🛠️ Commandes utiles

| Commande | Description |
|----------|-------------|
| `make up` | Démarrer les services |
| `make down` | Arrêter les services |
| `make logs` | Voir les logs |
| `make test` | Lancer les tests |
| `make lint` | Vérifier le code |
| `make db-up` | Migration DB (alembic upgrade) |

Ou avec docker compose :
```bash
docker compose up -d    # Démarrer
docker compose down     # Arrêter
docker compose logs -f  # Logs
```

---

## ⚙️ Services configurés

| Service | Image | Port | Description |
|---------|-------|------|-------------|
| backend | Local build | 8000 | API FastAPI |
| postgres | postgres:16-alpine | 5432 | Base de données |
| redis | redis:7-alpine | 6379 | Cache + Broker |

---

## 🔒 Sécurité

- ✅ Aucun secret réel dans le code
- ✅ `.env` dans `.gitignore`
- ✅ Scan de sécurité en CI (Trivy)
- ✅ Vérification des secrets (TruffleHog)
- ⚠️ **Changer les mots de passe par défaut avant production !**

---

## 📖 Documentation

- **DevOps Report** : `DEVOPS_REPORT.md` (détails complets)
- **CI/CD Guide** : `docs/CI-CD.md`
- **Product README** : `product/README.md`
- **API Docs** : http://localhost:8000/docs (une fois lancé)

---

## ✅ Prochaines étapes

1. **Backend dev** : Implémenter les routes dans `backend/app/`
2. **Tests** : Ajouter des tests dans `backend/tests/`
3. **CI/CD** : Configurer les secrets GitHub
4. **Security** : Audit avec `security-tech-lead`

---

**Le lab est prêt ! 🎉**
