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
