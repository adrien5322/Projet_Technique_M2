# Utiliser OpenCode avec OpenAI pour développer DevinciWatch

## Objectif du guide

Ce guide explique comment utiliser **OpenCode avec OpenAI** pour créer une équipe d’agents de développement autour du projet **DevinciWatch**.

L’objectif n’est pas encore de créer des agents OpenAI dans le code Python de DevinciWatch.

L’objectif est :

```text
Utiliser OpenCode avec OpenAI pour piloter des agents spécialisés capables d’aider à développer le projet.
```

OpenCode permet de configurer des agents spécialisés, avec des rôles, des permissions et des modes comme `primary` ou `subagent`. Les subagents peuvent être appelés manuellement avec `@nom-agent`. ([OpenCode][1])

---

# 1. Résultat attendu à la fin

À la fin du guide, l’étudiant aura :

```text
PROJET-M2-CYBER-2026/
│
├── opencode.jsonc
├── AGENTS.md
│
├── .opencode/
│   ├── agents/
│   │   ├── project-manager-tech.md
│   │   ├── backend-python-dev.md
│   │   ├── qa-tester.md
│   │   ├── devops-engineer.md
│   │   └── security-tech-lead.md
│   │
│   ├── commands/
│   │   ├── plan-epic.md
│   │   ├── implement-backend.md
│   │   ├── test-feature.md
│   │   ├── security-review.md
│   │   └── prepare-docker.md
│   │
│   └── skills/
│       ├── devinciwatch-project/
│       │   └── SKILL.md
│       ├── fastapi-backend/
│       │   └── SKILL.md
│       ├── python-testing/
│       │   └── SKILL.md
│       ├── devops-docker/
│       │   └── SKILL.md
│       └── cyber-security-review/
│           └── SKILL.md
```

---

# 2. Principe de fonctionnement

Le fonctionnement est le suivant :

```text
Étudiant
   |
   v
OpenCode
   |
   v
OpenAI comme moteur IA
   |
   v
Agents spécialisés OpenCode
```

Les agents sont :

```text
project-manager-tech    : organise le travail
backend-python-dev      : développe le backend Python/FastAPI
qa-tester               : écrit les tests
devops-engineer         : prépare Docker, scripts et CI/CD
security-tech-lead      : audite la sécurité
```

Il faut bien comprendre cette séparation :

```text
OpenCode avec OpenAI
= outil d’aide au développement.

OpenAI Agents SDK dans l’application Python
= fonctionnalité IA intégrée dans le produit.
```

Dans ce guide, on fait uniquement :

```text
OpenCode avec OpenAI.
```

---

# 3. Prérequis

L’étudiant doit avoir :

```text
Git installé
OpenCode installé
Un compte OpenAI
Une clé API OpenAI
Un terminal
Un éditeur de code
```

OpenAI recommande de créer une clé API puis de l’utiliser via une variable d’environnement, afin de ne pas l’écrire directement dans le code. ([Plateforme OpenAI][2])

---

# 4. Étape 1 — Cloner le projet

Dans un terminal :

```bash
git clone https://github.com/yugmerabtene/PROJET-M2-CYBER-2026.git
cd PROJET-M2-CYBER-2026
```

Créer une branche de travail :

```bash
git checkout -b setup/opencode-openai-agents
```

Vérifier l’état Git :

```bash
git status
```

Résultat attendu :

```text
On branch setup/opencode-openai-agents
nothing to commit, working tree clean
```

---

# 5. Étape 2 — Configurer la clé OpenAI

## Sur macOS, Linux ou WSL

```bash
export OPENAI_API_KEY="votre_cle_openai"
```

## Sur Windows PowerShell

```powershell
$env:OPENAI_API_KEY = "votre_cle_openai"
```

Attention : ne jamais écrire la vraie clé dans un fichier du projet.

Mauvaise pratique :

```text
OPENAI_API_KEY=sk-...
```

dans un fichier versionné.

Bonne pratique :

```text
Variable d’environnement locale
ou
fichier .env local non commité
```

---

# 6. Étape 3 — Lancer OpenCode et connecter OpenAI

À la racine du projet :

```bash
opencode
```

Dans OpenCode :

```text
/connect
```

Choisir :

```text
OpenAI
```

Ensuite, choisir le modèle :

```text
/models
```

OpenCode permet de connecter un provider, puis de sélectionner le modèle avec `/models`. ([OpenCode][3])

---

# 7. Étape 4 — Créer les dossiers OpenCode

À la racine du projet :

```bash
mkdir -p .opencode/agents
mkdir -p .opencode/commands
mkdir -p .opencode/skills/devinciwatch-project
mkdir -p .opencode/skills/fastapi-backend
mkdir -p .opencode/skills/python-testing
mkdir -p .opencode/skills/devops-docker
mkdir -p .opencode/skills/cyber-security-review
```

Vérifier :

```bash
find .opencode -maxdepth 3 -type d | sort
```

Résultat attendu :

```text
.opencode
.opencode/agents
.opencode/commands
.opencode/skills
.opencode/skills/cyber-security-review
.opencode/skills/devinciwatch-project
.opencode/skills/devops-docker
.opencode/skills/fastapi-backend
.opencode/skills/python-testing
```

---

# 8. Étape 5 — Créer `opencode.jsonc`

Créer le fichier :

```bash
touch opencode.jsonc
```

Mettre ce contenu :

```jsonc
{
  "$schema": "https://opencode.ai/config.json",

  "enabled_providers": ["openai"],

  "default_agent": "project-manager-tech",

  "model": "{env:OPENCODE_MODEL}",
  "small_model": "{env:OPENCODE_SMALL_MODEL}",

  "instructions": [
    "AGENTS.md",
    "README.md",
    "product/README.md",
    "tasks/*.md",
    "documents/06_cahier_des_charges/rendu_principal.md",
    "documents/07_gestion_de_projet/rendu_principal.md",
    "documents/08_architecture/rendu_principal.md"
  ],

  "permission": {
    "*": "ask",

    "edit": "ask",

    "bash": {
      "*": "ask",
      "git status*": "allow",
      "git diff*": "allow",
      "git log*": "allow",
      "ls*": "allow",
      "find*": "allow",
      "grep*": "allow",
      "python -m pytest*": "allow",
      "pytest*": "allow",
      "ruff*": "allow",
      "git push*": "deny",
      "rm -rf*": "deny"
    },

    "skill": {
      "*": "allow"
    },

    "task": {
      "*": "ask",
      "backend-python-dev": "allow",
      "qa-tester": "allow",
      "devops-engineer": "ask",
      "security-tech-lead": "allow"
    }
  },

  "agent": {
    "project-manager-tech": {
      "mode": "primary",
      "description": "Chef de projet technique DevinciWatch : planification, backlog, priorités et coordination.",
      "prompt": "{file:.opencode/agents/project-manager-tech.md}"
    },

    "backend-python-dev": {
      "mode": "subagent",
      "description": "Développeur backend Python/FastAPI pour DevinciWatch.",
      "prompt": "{file:.opencode/agents/backend-python-dev.md}"
    },

    "qa-tester": {
      "mode": "subagent",
      "description": "Testeur QA Python avec pytest.",
      "prompt": "{file:.opencode/agents/qa-tester.md}"
    },

    "devops-engineer": {
      "mode": "subagent",
      "description": "DevOps Docker, scripts, variables d’environnement et CI/CD.",
      "prompt": "{file:.opencode/agents/devops-engineer.md}"
    },

    "security-tech-lead": {
      "mode": "subagent",
      "description": "Security Tech Lead : audit sécurité, secrets, RBAC, payloads et scénarios cyber.",
      "prompt": "{file:.opencode/agents/security-tech-lead.md}",
      "permission": {
        "edit": "deny"
      }
    }
  }
}
```

Explication :

```text
default_agent
```

indique l’agent principal utilisé par défaut.

```text
project-manager-tech
```

est l’agent principal.

```text
backend-python-dev
qa-tester
devops-engineer
security-tech-lead
```

sont des subagents.

OpenCode permet de définir un agent par défaut, qui doit être un agent principal. ([OpenCode][4])

Les permissions `allow`, `ask` et `deny` permettent d’autoriser, demander confirmation ou bloquer une action. ([OpenCode][5])

---

# 9. Étape 6 — Définir les modèles OpenAI utilisés

## Sur macOS, Linux ou WSL

```bash
export OPENCODE_MODEL="openai/gpt-5.2"
export OPENCODE_SMALL_MODEL="openai/gpt-5-mini"
```

## Sur Windows PowerShell

```powershell
$env:OPENCODE_MODEL = "openai/gpt-5.2"
$env:OPENCODE_SMALL_MODEL = "openai/gpt-5-mini"
```

Remarque : les noms exacts dépendent des modèles visibles dans OpenCode avec :

```text
/models
```

---

# 10. Étape 7 — Créer le fichier `AGENTS.md`

Créer le fichier :

```bash
touch AGENTS.md
```

Mettre ce contenu :

```md
# DevinciWatch - Règles OpenCode avec OpenAI

## Objectif

OpenCode utilise OpenAI comme moteur IA pour aider au développement du projet DevinciWatch.

Les agents définis dans ce dépôt servent uniquement à développer le projet.

Ils ne sont pas des agents intégrés dans l’application Python.

## Agents disponibles

- project-manager-tech : planifie, découpe, coordonne.
- backend-python-dev : développe le backend Python/FastAPI.
- qa-tester : écrit les tests.
- devops-engineer : prépare Docker, scripts, environnement et CI/CD.
- security-tech-lead : audite la sécurité.

## Règles générales

- Ne jamais exposer de secret.
- Ne jamais écrire de vraie clé API dans le code.
- Ne jamais créer de fichier .env avec de vraies valeurs.
- Utiliser .env.example pour documenter les variables.
- Travailler dans product/.
- Commencer par EPIC-01.
- Ne pas générer toute l’application d’un coup.
- Avancer tâche par tâche.
- Tester après chaque fonctionnalité.
- Auditer la sécurité avant validation.

## Workflow obligatoire

1. project-manager-tech analyse l’epic.
2. backend-python-dev implémente une petite tâche.
3. qa-tester écrit ou complète les tests.
4. security-tech-lead audite la sécurité.
5. devops-engineer intervient pour Docker, scripts ou CI/CD.
6. project-manager-tech valide l’incrément.
```

---

# 11. Étape 8 — Créer les agents

## 11.1 Créer l’agent chef de projet technique

Créer le fichier :

```bash
touch .opencode/agents/project-manager-tech.md
```

Mettre ce contenu :

```md
---
description: Chef de projet technique DevinciWatch.
mode: primary
temperature: 0.2
---

Tu es le chef de projet technique du projet DevinciWatch.

Ta mission est de piloter le développement avec OpenCode.

Tu dois :

- analyser les epics ;
- comprendre les user stories ;
- découper le travail en tâches courtes ;
- choisir le bon agent ;
- éviter la sur-ingénierie ;
- garder un MVP testable ;
- vérifier que les tests sont prévus ;
- demander une revue sécurité avant validation.

Tu dois toujours répondre avec :

1. Objectif.
2. Epic concernée.
3. Fichiers à créer ou modifier.
4. Agent responsable.
5. Critères d’acceptation.
6. Tests attendus.
7. Risques.
8. Prochaine action.

Tu délègues :

- à @backend-python-dev pour le code ;
- à @qa-tester pour les tests ;
- à @devops-engineer pour Docker, scripts et CI/CD ;
- à @security-tech-lead pour l’audit sécurité.

Tu ne dois jamais demander la création complète de DevinciWatch en une seule fois.
Tu dois travailler par petits incréments.
```

---

## 11.2 Créer l’agent développeur backend

Créer le fichier :

```bash
touch .opencode/agents/backend-python-dev.md
```

Mettre ce contenu :

```md
---
description: Développeur backend Python/FastAPI pour DevinciWatch.
mode: subagent
temperature: 0.1
---

Tu es développeur backend Python senior sur DevinciWatch.

Tu travailles principalement dans :

- product/backend/
- product/backend/app/
- product/backend/tests/

Stack cible :

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Celery
- Docker Compose

Modules backend attendus :

- core
- auth
- telemetry
- discovery
- assets
- alerts
- correlation
- reports
- audit

Règles de développement :

- écrire du code simple ;
- utiliser le typage Python ;
- garder les routes FastAPI minces ;
- placer la logique métier dans des services ;
- valider les entrées avec Pydantic ;
- centraliser la configuration ;
- ne jamais exposer de secret ;
- ne pas ajouter de fonctionnalité hors demande ;
- créer des tests associés ;
- ne pas générer de code destructeur.

Avant modification, tu dois préciser :

1. le fichier ciblé ;
2. la raison de la modification ;
3. le lien avec l’epic ou la user story.

Après modification, tu dois préciser :

1. ce qui a été fait ;
2. comment tester ;
3. les limites restantes.
```

---

## 11.3 Créer l’agent testeur QA

Créer le fichier :

```bash
touch .opencode/agents/qa-tester.md
```

Mettre ce contenu :

```md
---
description: Testeur QA DevinciWatch avec pytest.
mode: subagent
temperature: 0.1
---

Tu es testeur QA sur DevinciWatch.

Ta mission :

- transformer les critères d’acceptation en tests ;
- tester les routes FastAPI ;
- tester les erreurs ;
- tester les accès refusés ;
- tester les payloads invalides ;
- tester heartbeat, events, alertes, corrélation et exports ;
- vérifier la non-régression.

Tu travailles dans :

- product/backend/tests/
- product/tests/

Règles :

- utiliser pytest ;
- utiliser TestClient ou httpx pour FastAPI ;
- ne pas appeler OpenAI dans les tests unitaires ;
- ne pas scanner de réseau externe ;
- vérifier les codes HTTP ;
- vérifier les champs JSON attendus ;
- tester au moins un cas valide et un cas invalide.

Ta sortie doit contenir :

1. Tests ajoutés.
2. Exigence couverte.
3. Commande de lancement.
4. Résultat attendu.
5. Limites restantes.
```

---

## 11.4 Créer l’agent DevOps

Créer le fichier :

```bash
touch .opencode/agents/devops-engineer.md
```

Mettre ce contenu :

```md
---
description: DevOps DevinciWatch.
mode: subagent
temperature: 0.1
---

Tu es ingénieur DevOps sur DevinciWatch.

Ta mission :

- rendre le projet lançable localement ;
- préparer Docker Compose ;
- documenter les variables d’environnement ;
- préparer .env.example ;
- préparer les scripts de lancement ;
- préparer la CI/CD ;
- garder le lab reproductible.

Contraintes :

- ne jamais exposer de secret réel ;
- ne pas ajouter de dépendance externe inutile ;
- garder une structure simple ;
- documenter les commandes ;
- éviter les actions destructrices ;
- ne jamais faire de push automatique.

Ta sortie doit contenir :

1. Fichiers créés ou modifiés.
2. Variables nécessaires.
3. Commandes de lancement.
4. Commandes de vérification.
5. Risques opérationnels.
```

---

## 11.5 Créer l’agent Security Tech Lead

Créer le fichier :

```bash
touch .opencode/agents/security-tech-lead.md
```

Mettre ce contenu :

```md
---
description: Security Tech Lead DevinciWatch.
mode: subagent
temperature: 0.1
permission:
  edit: deny
---

Tu es Security Tech Lead sur DevinciWatch.

Tu ne modifies pas le code directement.
Tu audites et tu proposes des corrections.

Tu contrôles :

- secrets exposés ;
- fichiers .env ;
- auth utilisateur ;
- auth agent ;
- séparation routes utilisateur et routes agent ;
- RBAC admin et analyst ;
- validation des payloads ;
- logs sensibles ;
- audit trail ;
- scénarios attacker ;
- réseau Docker borné ;
- permissions OpenCode ;
- dépendances risquées ;
- absence de tests de sécurité.

Tu dois rendre :

1. Risques critiques.
2. Risques moyens.
3. Risques faibles.
4. Fichiers concernés.
5. Corrections recommandées.
6. Priorité de correction.
7. Décision finale : OK, OK avec réserves ou bloquant.
```

---

# 12. Étape 9 — Créer les skills

Les skills sont des instructions réutilisables. OpenCode les charge depuis des dossiers comme `.opencode/skills/<nom>/SKILL.md`. ([OpenCode][6])

## 12.1 Skill DevinciWatch

Créer le fichier :

```bash
touch .opencode/skills/devinciwatch-project/SKILL.md
```

Mettre ce contenu :

```md
---
name: devinciwatch-project
description: Comprendre DevinciWatch, son MVP, ses epics, son architecture SOC et ses contraintes de lab.
compatibility: opencode
---

# Skill DevinciWatch Project

## Contexte

DevinciWatch est une plateforme de cybersurveillance réseau orientée SOC.

Le projet doit démontrer :

- collecte de télémétrie endpoint ;
- ingestion heartbeat ;
- ingestion events ;
- inventaire d’actifs ;
- détection par règles simples ;
- corrélation minimale ;
- alertes actionnables ;
- export CSV et JSON ;
- audit trail ;
- lab Docker reproductible.

## Architecture générale

Le lab repose sur :

- serveur-soc ;
- serveur-endpoint ;
- serveur-attacker.

## Priorités du MVP

Commencer par :

1. socle FastAPI ;
2. endpoint health ;
3. auth skeleton ;
4. heartbeat ;
5. events ;
6. auth agent ;
7. alertes simples ;
8. audit ;
9. Docker Compose.

## Règles

- Ne pas développer tout le projet en une seule fois.
- Toujours travailler epic par epic.
- Toujours relier le code à une user story.
- Toujours prévoir un test.
```

---

## 12.2 Skill FastAPI backend

Créer le fichier :

```bash
touch .opencode/skills/fastapi-backend/SKILL.md
```

Mettre ce contenu :

````md
---
name: fastapi-backend
description: Construire le backend FastAPI DevinciWatch avec routes, schemas, services, tests et configuration.
compatibility: opencode
---

# Skill FastAPI Backend

## Structure cible

```text
product/backend/app/
├── main.py
├── core/
├── auth/
├── telemetry/
├── discovery/
├── assets/
├── alerts/
├── correlation/
├── reports/
└── audit/
````

## Organisation par module

Chaque module peut contenir :

```text
router.py
schemas.py
models.py
service.py
repository.py
```

## Règles

* Les routes doivent rester simples.
* Les services portent la logique métier.
* Les schemas Pydantic valident les entrées.
* Les modèles SQLAlchemy arrivent seulement quand la persistance est nécessaire.
* Les tests accompagnent chaque endpoint.

````

---

## 12.3 Skill tests Python

Créer le fichier :

```bash
touch .opencode/skills/python-testing/SKILL.md
````

Mettre ce contenu :

```md
---
name: python-testing
description: Créer des tests pytest pour DevinciWatch : FastAPI, validation, sécurité, erreurs et recette.
compatibility: opencode
---

# Skill Python Testing

## Tests attendus

- test health ;
- test auth ;
- test RBAC ;
- test auth agent ;
- test payload invalide ;
- test heartbeat ;
- test events ;
- test alertes ;
- test corrélation ;
- test exports ;
- test audit.

## Règles

- Pas d’appel réseau externe.
- Pas d’appel OpenAI dans les tests unitaires.
- Pas de scan réel.
- Tests reproductibles.
- Vérifier les codes HTTP.
- Vérifier les champs JSON.
```

---

## 12.4 Skill DevOps Docker

Créer le fichier :

```bash
touch .opencode/skills/devops-docker/SKILL.md
```

Mettre ce contenu :

```md
---
name: devops-docker
description: Préparer Docker Compose, scripts, .env.example, CI/CD et lab reproductible pour DevinciWatch.
compatibility: opencode
---

# Skill DevOps Docker

## Objectif

Rendre DevinciWatch lançable localement.

## Lab cible

- serveur-soc ;
- serveur-endpoint ;
- serveur-attacker.

## Règles

- Réseau Docker dédié.
- Variables dans .env.example.
- Aucun secret réel.
- Commande unique de lancement.
- Healthcheck disponible.
- Logs consultables.
- Pas de suppression de volume sans validation.
```

---

## 12.5 Skill sécurité

Créer le fichier :

```bash
touch .opencode/skills/cyber-security-review/SKILL.md
```

Mettre ce contenu :

````md
---
name: cyber-security-review
description: Auditer DevinciWatch : secrets, RBAC, auth agent, payloads, audit logs, Docker lab et scénarios cyber.
compatibility: opencode
---

# Skill Cyber Security Review

## Contrôles

- aucun secret versionné ;
- .env ignoré ;
- .env.example sans vraie clé ;
- auth utilisateur prévue ;
- RBAC admin et analyst prévu ;
- auth agent séparée ;
- routes agent séparées ;
- payloads validés ;
- audit trail prévu ;
- logs non sensibles ;
- scénario attacker borné au lab ;
- pas de commande dangereuse.

## Décision attendue

Le résultat d’audit doit être :

```text
OK
OK avec réserves
Bloquant
````

````

---

# 13. Étape 10 — Créer les commandes OpenCode

## 13.1 Commande `/plan-epic`

Créer :

```bash
touch .opencode/commands/plan-epic.md
````

Mettre :

```md
---
description: Analyse une epic DevinciWatch et prépare le plan de développement.
agent: project-manager-tech
---

Analyse l’epic ou la demande suivante :

$ARGUMENTS

Tu dois produire :

1. Epic concernée.
2. User stories liées.
3. Exigences liées.
4. Fichiers à créer ou modifier.
5. Ordre de développement.
6. Agent responsable.
7. Tests attendus.
8. Risques sécurité.
9. Definition of Done.
```

---

## 13.2 Commande `/implement-backend`

Créer :

```bash
touch .opencode/commands/implement-backend.md
```

Mettre :

```md
---
description: Implémente une tâche backend DevinciWatch.
agent: backend-python-dev
---

Implémente uniquement la tâche suivante :

$ARGUMENTS

Contraintes :

- respecter product/backend ;
- respecter FastAPI ;
- utiliser Pydantic pour les entrées ;
- ne pas exposer de secret ;
- ne pas ajouter de fonctionnalité hors demande ;
- préparer les tests attendus ;
- documenter brièvement le changement.
```

---

## 13.3 Commande `/test-feature`

Créer :

```bash
touch .opencode/commands/test-feature.md
```

Mettre :

```md
---
description: Crée ou met à jour les tests pour une fonctionnalité DevinciWatch.
agent: qa-tester
---

Teste la fonctionnalité suivante :

$ARGUMENTS

Tu dois produire :

1. tests unitaires ;
2. tests API si nécessaire ;
3. cas valides ;
4. cas invalides ;
5. tests d’autorisation si nécessaire ;
6. commande pytest ;
7. résultat attendu.
```

---

## 13.4 Commande `/security-review`

Créer :

```bash
touch .opencode/commands/security-review.md
```

Mettre :

```md
---
description: Audit sécurité DevinciWatch.
agent: security-tech-lead
---

Audite la partie suivante :

$ARGUMENTS

Contrôle :

- secrets ;
- auth utilisateur ;
- auth agent ;
- RBAC ;
- validation payload ;
- audit logs ;
- routes sensibles ;
- scénarios cyber ;
- Docker lab ;
- permissions OpenCode.

Rends une décision :

- OK ;
- OK avec réserves ;
- bloquant.
```

---

## 13.5 Commande `/prepare-docker`

Créer :

```bash
touch .opencode/commands/prepare-docker.md
```

Mettre :

```md
---
description: Prépare ou vérifie Docker pour DevinciWatch.
agent: devops-engineer
---

Prépare ou vérifie la partie Docker suivante :

$ARGUMENTS

Tu dois produire :

1. fichiers concernés ;
2. variables d’environnement ;
3. commandes de lancement ;
4. commandes de vérification ;
5. risques ;
6. limites.
```

---

# 14. Étape 11 — Vérifier les fichiers créés

Lancer :

```bash
find .opencode -maxdepth 3 -type f | sort
```

Résultat attendu :

```text
.opencode/agents/backend-python-dev.md
.opencode/agents/devops-engineer.md
.opencode/agents/project-manager-tech.md
.opencode/agents/qa-tester.md
.opencode/agents/security-tech-lead.md
.opencode/commands/implement-backend.md
.opencode/commands/plan-epic.md
.opencode/commands/prepare-docker.md
.opencode/commands/security-review.md
.opencode/commands/test-feature.md
.opencode/skills/cyber-security-review/SKILL.md
.opencode/skills/devinciwatch-project/SKILL.md
.opencode/skills/devops-docker/SKILL.md
.opencode/skills/fastapi-backend/SKILL.md
.opencode/skills/python-testing/SKILL.md
```

Vérifier Git :

```bash
git status
```

---

# 15. Étape 12 — Premier lancement OpenCode

Lancer :

```bash
opencode
```

Dans OpenCode, vérifier le modèle :

```text
/models
```

Puis demander au chef de projet technique :

```text
@project-manager-tech
Analyse EPIC-01 et prépare le plan de développement du socle FastAPI dans product/backend.

Contraintes :
- commencer par GET /health ;
- préparer une configuration minimale ;
- préparer un auth skeleton ;
- ajouter les tests ;
- ne pas créer PostgreSQL maintenant ;
- ne pas créer Redis maintenant ;
- ne pas créer Celery maintenant ;
- ne pas créer le frontend maintenant.
```

Résultat attendu : l’agent doit produire un plan, pas encore du code.

---

# 16. Étape 13 — Premier développement guidé

Demander ensuite :

```text
@backend-python-dev
Crée uniquement le socle FastAPI minimal dans product/backend.

Créer :
- product/backend/pyproject.toml
- product/backend/app/main.py
- product/backend/app/health/router.py
- product/backend/app/core/config.py
- product/backend/app/auth/router.py
- product/backend/tests/test_health.py
- product/backend/README.md
- product/backend/.env.example

Objectif :
- FastAPI démarre ;
- GET /health retourne 200 ;
- pytest passe ;
- aucun appel OpenAI ;
- aucune base de données ;
- aucun Redis ;
- aucun Celery ;
- aucun secret réel.
```

L’étudiant doit valider les fichiers proposés par OpenCode.

---

# 17. Étape 14 — Demander les tests

Dans OpenCode :

```text
@qa-tester
Ajoute ou vérifie les tests pytest pour GET /health.

Le test doit vérifier :
- statut HTTP 200 ;
- champ status ;
- champ service ;
- aucune dépendance externe ;
- aucun appel OpenAI ;
- aucun accès base de données.
```

Ensuite, dans le terminal :

```bash
cd product/backend
python -m pytest
```

Résultat attendu :

```text
tests passed
```

---

# 18. Étape 15 — Demander l’audit sécurité

Dans OpenCode :

```text
@security-tech-lead
Audite le socle backend initial.

Vérifie :
- absence de secret ;
- absence de vraie clé API ;
- .env.example propre ;
- route /health non sensible ;
- structure prête pour auth future ;
- aucune commande dangereuse ;
- aucune dépendance inutile ;
- cohérence avec EPIC-01.

Rends une décision :
OK, OK avec réserves ou bloquant.
```

Si la réponse est :

```text
Bloquant
```

il faut corriger avant de continuer.

---

# 19. Étape 16 — Demander la préparation DevOps

Dans OpenCode :

```text
@devops-engineer
Prépare uniquement l’exécution locale du backend.

Créer ou vérifier :
- README backend ;
- .env.example ;
- commande d’installation ;
- commande de lancement uvicorn ;
- commande de test pytest.

Ne crée pas encore le Docker Compose complet.
```

Commandes attendues :

```bash
cd product/backend
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
python -m pytest
uvicorn app.main:app --reload
```

Sur Windows PowerShell :

```powershell
cd product/backend
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
python -m pytest
uvicorn app.main:app --reload
```

Tester dans un autre terminal :

```bash
curl http://127.0.0.1:8000/health
```

Résultat attendu :

```json
{
  "status": "ok",
  "service": "devinciwatch-api"
}
```

---

# 20. Étape 17 — Faire un commit propre

Revenir à la racine du dépôt :

```bash
cd ../..
```

Vérifier :

```bash
git status
```

Faire un premier commit pour la configuration agentique :

```bash
git add opencode.jsonc AGENTS.md .opencode
git commit -m "chore: add opencode openai agent workflow"
```

Faire un second commit pour le backend initial :

```bash
git add product/backend
git commit -m "feat: add initial FastAPI backend skeleton"
```

---

# 21. Méthode de travail à respecter ensuite

Pour chaque fonctionnalité, l’étudiant doit suivre ce cycle :

```text
1. Planifier
2. Développer
3. Tester
4. Auditer
5. Documenter
6. Commit
```

Exemple pour une prochaine user story :

```text
@project-manager-tech
Analyse US-01.1 Authentification utilisateur et prépare le plan de développement.
```

Puis :

```text
@backend-python-dev
Implémente uniquement le skeleton de POST /auth/login sans base de données.
```

Puis :

```text
@qa-tester
Ajoute les tests pour login valide, login invalide et payload invalide.
```

Puis :

```text
@security-tech-lead
Audite la partie auth : secrets, payloads, erreurs, routes et tests.
```

Puis :

```text
@devops-engineer
Mets à jour le README backend avec les commandes de test et lancement.
```

---

# 22. Règles importantes pour les étudiants

## Mauvaise demande

```text
Crée toute l’application DevinciWatch.
```

Pourquoi c’est mauvais :

```text
Trop large.
Trop risqué.
Difficile à tester.
Difficile à corriger.
```

## Bonne demande

```text
Implémente uniquement GET /health dans product/backend avec un test pytest.
```

Pourquoi c’est bon :

```text
Petit.
Contrôlable.
Testable.
Facile à corriger.
```

---

# 23. Résumé final pour les étudiants

À retenir :

```text
OpenCode utilise OpenAI comme moteur IA.

Les agents OpenCode servent à développer le projet.

Les agents ne sont pas encore intégrés dans DevinciWatch.

On commence par créer une équipe de développement agentique :

- chef de projet technique ;
- développeur backend ;
- testeur ;
- DevOps ;
- security tech lead.

On travaille toujours par petites tâches testables.
```

Workflow final :

```text
@project-manager-tech
   planifie

@backend-python-dev
   développe

@qa-tester
   teste

@security-tech-lead
   audite

@devops-engineer
   prépare l’exécution
```

La phrase clé :

```text
Nous utilisons OpenCode avec OpenAI pour organiser, développer, tester et sécuriser DevinciWatch étape par étape.
```

[1]: https://opencode.ai/docs/agents/?utm_source=chatgpt.com "Agents | OpenCode"
[2]: https://platform.openai.com/docs/quickstart?utm_source=chatgpt.com "Developer quickstart | OpenAI API"
[3]: https://opencode.ai/docs/models/?utm_source=chatgpt.com "Models | OpenCode"
[4]: https://opencode.ai/docs/config/?utm_source=chatgpt.com "Config | OpenCode"
[5]: https://opencode.ai/docs/permissions?utm_source=chatgpt.com "Permissions | OpenCode"
[6]: https://opencode.ai/docs/skills?utm_source=chatgpt.com "Agent Skills | OpenCode"
