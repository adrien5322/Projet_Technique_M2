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
