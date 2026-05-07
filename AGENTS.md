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
