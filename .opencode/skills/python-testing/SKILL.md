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
