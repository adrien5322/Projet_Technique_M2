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
