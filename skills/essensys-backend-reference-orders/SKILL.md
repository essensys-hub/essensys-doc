---
name: essensys-backend-reference-orders
description: Explains Essensys backend flow, reference table indices, and how to send valid orders via MCP/API/Redis. Use when discussing backend architecture, index mapping (590 and 605..622), or why web orders work while MCP orders fail.
---

# Essensys Backend, Table de Reference, et Ordres

## Objectif

Fournir une explication fiable du flux d'ordre Essensys:

1. MCP/API injecte une action.
2. L'action est stockee dans Redis (`essensys:global:actions`).
3. Le client BP_MQX_ETH recupere via `GET /api/myactions`.
4. Le firmware applique les indices table d'echange puis acquitte via `/api/done/{guid}`.

## Quand utiliser ce skill

- Question sur architecture backend Essensys.
- Question sur table de reference / indices.
- Debug "Web OK, MCP KO".
- Besoin d'expliquer format d'ordre valide.

## Regles essentielles a rappeler

### 1) Un ordre lumiere/volet ne doit pas etre partiel

Pour les commandes scenario/lumieres/volets:

- Inclure `590` (declenchement scenario) si absent.
- Inclure tous les indices `605..622`.
- Mettre a `0` les indices non utilises.

Sinon le comportement peut etre ignore ou non deterministe cote firmware.

### 2) `613=64` seul peut etre insuffisant

`613` est une valeur de configuration scenario (bitmask), pas toujours un "execute immediat" autonome.

### 3) Le web passe par la logique backend complete

`POST /api/admin/inject` -> `ActionService.AddAction()` -> generation bloc complet (`590 + 605..622`).

Si MCP pousse direct Redis sans cette normalisation, resultat different du web.

## Procedure de diagnostic rapide

1. Verifier services:
   - `systemctl is-active essensys-backend essensys-mcp`
2. Verifier queue Redis:
   - `redis-cli LLEN essensys:global:actions`
   - `redis-cli LRANGE essensys:global:actions 0 2`
3. Verifier reponse backend:
   - `curl -s http://127.0.0.1:7070/api/myactions`
4. Comparer payload web vs payload MCP.

## Format de reponse attendu par ce skill

Quand on t'interroge, repondre en 3 blocs:

1. **Cause** (1-3 lignes)
2. **Preuve technique** (indices/flux exact)
3. **Correctif** (payload ou patch concret)

## Exemples d'ordre

### Allumer chevet petite chambre 3 (compatible legacy)

```json
{
  "guid": "example-guid",
  "params": [
    {"k":590,"v":"1"},
    {"k":605,"v":"0"},
    {"k":606,"v":"0"},
    {"k":607,"v":"0"},
    {"k":608,"v":"0"},
    {"k":609,"v":"0"},
    {"k":610,"v":"0"},
    {"k":611,"v":"0"},
    {"k":612,"v":"0"},
    {"k":613,"v":"64"},
    {"k":614,"v":"0"},
    {"k":615,"v":"0"},
    {"k":616,"v":"0"},
    {"k":617,"v":"0"},
    {"k":618,"v":"0"},
    {"k":619,"v":"0"},
    {"k":620,"v":"0"},
    {"k":621,"v":"0"},
    {"k":622,"v":"0"}
  ]
}
```

## Ressources

- Reference detaillee: [reference.md](reference.md)
