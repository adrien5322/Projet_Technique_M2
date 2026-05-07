# DevinciWatch - CI/CD Documentation

## Vue d'ensemble

Le pipeline CI/CD de DevinciWatch utilise GitHub Actions pour automatiser les tests, le build et le déploiement.

## Workflows

### 1. CI (`ci.yml`) - Intégration Continue

**Déclenchement :**
- Push sur `main` ou `develop`
- Pull Request vers `main` ou `develop`

**Jobs :**

#### lint
- Vérifie le code avec `flake8`
- Vérifie le formatage avec `black`
- Vérifie l'ordre des imports avec `isort`

#### test
- Tests unitaires avec `pytest`
- Utilise PostgreSQL et Redis comme services
- Génération de rapport de couverture (Codecov)

#### build
- Construction de l'image Docker
- Test de l'image construite
- Sauvegarde en artifact (uniquement sur `main`)

#### security
- Scan de vulnérabilités avec Trivy
- Vérification des secrets avec TruffleHog

#### secrets-check
- Vérifie l'absence de fichiers `.env` dans le dépôt
- Scan des secrets exposés

### 2. CD (`cd.yml`) - Déploiement Continu

**Déclenchement :**
- Push sur `main` (staging)
- Tags `v*` (production)
- Manuel (`workflow_dispatch`)

**Jobs :**

#### deploy-staging
- Build et push de l'image vers GitHub Container Registry
- Déploiement en environnement de staging

#### deploy-production
- Build et push de l'image avec tags de version
- Déploiement en production
- Création d'une Release GitHub

#### notify
- Notification du statut de déploiement

## Secrets GitHub requis

Configurez ces secrets dans les paramètres du dépôt GitHub (`Settings > Secrets and variables > Actions`) :

### Pour la CI
- `CODECOV_TOKEN` (optionnel) : Token pour Codecov

### Pour le CD - Staging
- `STAGING_HOST` : Hôte de staging
- `STAGING_SSH_KEY` : Clé SSH pour le déploiement

### Pour le CD - Production
- `PRODUCTION_HOST` : Hôte de production
- `PRODUCTION_SSH_KEY` : Clé SSH pour le déploiement

## Utilisation

### Lancer la CI manuellement

1. Aller dans l'onglet "Actions" du dépôt
2. Sélectionner le workflow "DevinciWatch CI/CD"
3. Cliquer sur "Run workflow"
4. Choisir la branche et lancer

### Déployer manuellement

1. Aller dans l'onglet "Actions"
2. Sélectionner "DevinciWatch CD - Deploy"
3. Cliquer sur "Run workflow"
4. Choisir l'environnement (staging/production)

## Images Docker

Les images sont stockées sur GitHub Container Registry (ghcr.io) :

```
ghcr.io/<owner>/<repo>:main
ghcr.io/<owner>/<repo>:sha-<commit-sha>
ghcr.io/<owner>/<repo>:v1.0.0  # pour les tags
```

## Environnements GitHub

Configurez les environnements dans `Settings > Environments` :

### staging
- Protection : aucune (ou branche `main`)
- Secrets : `STAGING_HOST`, `STAGING_SSH_KEY`

### production
- Protection : approbation requise recommandée
- Secrets : `PRODUCTION_HOST`, `PRODUCTION_SSH_KEY`

## Personnalisation

### Modifier les branches de déclenchement

Éditez les sections `on:` dans les fichiers `.github/workflows/*.yml`

### Ajouter des tests E2E

Ajoutez un nouveau job dans `ci.yml` :

```yaml
e2e:
  name: End-to-End Tests
  runs-on: ubuntu-latest
  steps:
    - uses: actions/checkout@v4
    # ... configuration
```

### Modifier le déploiement

Éditez les étapes de déploiement dans `cd.yml` selon votre infrastructure (Kubernetes, Docker Swarm, SSH, etc.)

## Dépannage

### Le workflow échoue sur le lint
```bash
# En local, corrigez avec :
make format
make lint
```

### Le workflow échoue sur les tests
```bash
# En local, lancez les tests :
make test
# Vérifiez les logs pour plus de détails
```

### L'image Docker ne se build pas
```bash
# Testez le build en local :
make build
# Vérifiez le Dockerfile pour d'éventuelles erreurs
```

## Sécurité

⚠️ **Ne jamais exposer de secrets dans les logs CI !**

- Utilisez toujours des GitHub Secrets
- Ne faites jamais `echo $SECRET` dans les workflows
- Vérifiez que `.env` est bien dans `.gitignore`

## Ressources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Docker Build Push Action](https://github.com/docker/build-push-action)
- [Trivy Security Scanner](https://github.com/aquasecurity/trivy)
