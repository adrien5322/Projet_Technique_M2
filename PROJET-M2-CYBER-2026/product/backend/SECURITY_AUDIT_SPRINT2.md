# DAR-Cyber - Rapport d'Audit Sécurité Sprint 2

**Date**: 07/05/2026  
**Auditeur**: Security Tech Lead  
**Portée**: Backend FastAPI (`/product/backend/`)

---

## Tableau de statut par EPIC

| EPIC | Statut | Commentaire |
|------|--------|-------------|
| EPIC-01 (Events) | ✅ OK | Auth agent/user correcte, validation Pydantic OK |
| EPIC-02 (Discovery) | ⚠️ Réserves | IP validée mais body dict au lieu de schema |
| EPIC-03 (Alerts) | ✅ OK | RBAC cohérent, audit trail présent |
| EPIC-04 (Audit) | 🔴 **Bloquant** | POST /audit/log sans auth (critique) |
| EPIC-05 (Reports) | ✅ OK | RBAC respecté sur tous les exports |

---

## Liste des problèmes détectés

| # | Problème | Sévérité | Fichier concerné | Recommandation |
|---|----------|----------|------------------|----------------|
| 1 | **POST /audit/log sans authentification** | 🔴 Critique | `app/audit/routes.py:53-84` | Ajouter `verify_agent_secret` ou auth JWT. Endpoint accessible à tous pour écrire des logs arbitraires (user_id forgeable) |
| 2 | **Comparaison AGENT_SECRET avec `!=` au lieu de `hmac.compare_digest`** | 🔴 Critique | `app/auth/dependencies.py:62,93` | Vulnérable aux timing attacks. Utiliser `hmac.compare_digest(x_agent_secret, settings.AGENT_SECRET)` |
| 3 | **Body dict au lieu de schema Pydantic pour POST /discovery/scan** | 🟡 Moyen | `app/discovery/routes.py:28-63` | Utiliser un schema `IPRangeScanRequest` avec validation au lieu de `body: dict` |
| 4 | **Pas de rate limiting sur les endpoints publics** | 🟡 Moyen | Tous les routes | Ajouter un middleware de rate limiting (ex: slowapi) pour prévenir le bruteforce/DoS |
| 5 | **CORS permissif en dev, à vérifier en prod** | 🟢 Faible | `app/config.py:34` | S'assurer que `CORS_ORIGINS` est restreint en production via variable d'env |
| 6 | **Pas de validation de longueur sur les payloads** | 🟡 Moyen | Global | Ajouter des limites de taille (ex: `raw_data` dans events) pour éviter les payloads massifs |
| 7 | **Logs d'audit : user_id accepté dans le payload POST /audit/log** | 🔴 Critique | `app/audit/routes.py:81` | Si auth ajoutée, récupérer `user_id` depuis le token, pas depuis le payload |
| 8 | **Pas de tests de sécurité dédiés (pentest simulé)** | 🟡 Moyen | `/tests/` | Ajouter des tests pour les scénarios : injection, bruteforce, RBAC bypass |
| 9 | **HOST=0.0.0.0 par défaut** | 🟢 Faible | `app/config.py:16` | S'assurer que c'est intentionnel (Docker) et restreint par le reverse proxy en prod |
| 10 | **Pas de validation du Content-Type sur les endpoints agents** | 🟡 Moyen | `app/auth/dependencies.py` | Vérifier que les agents envoient `application/json` pour éviter les content-type attacks |

---

## Détails des points critiques

### 1. POST /audit/log sans auth (🔴 Bloquant)
```python
# app/audit/routes.py - Actuellement SANS auth
@router.post("/log", ...)
async def create_audit_log(
    log_data: AuditLogCreate,
    db: Session = Depends(get_db),
    request: Request = None,
) -> AuditLogResponse:
    """Crée un log d'audit sans authentification"""
```
**Risque**: N'importe qui peut injecter des logs arbitraires, forger `user_id`, remplir la DB.  
**Correction**: 
```python
async def create_audit_log(
    log_data: AuditLogCreate,
    db: Session = Depends(get_db),
    _: bool = Depends(verify_agent_secret),  # Ajouter cette ligne
    request: Request = None,
) -> AuditLogResponse:
```

### 2. Comparaison AGENT_SECRET (🔴 Critique)
```python
# app/auth/dependencies.py - Actuel (lignes 62 et 93)
if x_agent_secret != settings.AGENT_SECRET:  # Timing attack possible
```
**Correction**:
```python
import hmac
# ...
if not hmac.compare_digest(x_agent_secret or "", settings.AGENT_SECRET):
    raise HTTPException(status_code=401, detail="Invalid agent secret")
```

---

## Verdict global

### 🔴 **BLOQUANT** - Corrections requises avant mise en production

**Justification**:
1. L'endpoint `POST /api/v1/audit/log` est **totalement exposé** sans authentification. C'est une faille critique permettant l'injection de logs arbitraires.
2. La comparaison du `AGENT_SECRET` avec `!=` expose à des **timing attacks**, permettant une énumération du secret.

**Actions immédiates**:
- [ ] Ajouter `Depends(verify_agent_secret)` sur `POST /audit/log`
- [ ] Remplacer `!=` par `hmac.compare_digest` dans `dependencies.py`
- [ ] Créer un schema Pydantic pour `POST /discovery/scan` au lieu de `dict`

**Une fois ces 3 points corrigés**: Statut passe à ✅ **OK avec réserves** (pour les points moyens/faibles à traiter en post-Sprint2).

---

*Rapport généré par Security Tech Lead - DAR-Cyber*
