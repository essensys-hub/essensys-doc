# Reference Essensys (detail)

## Flux simplifie

1. Producteur d'ordre:
   - Web: `POST /api/admin/inject`
   - MCP: outil `send_order` (ou equivalent)
2. Stockage:
   - Redis list `essensys:global:actions`
3. Consommateur:
   - BP_MQX_ETH: `GET /api/myactions`
4. Ack:
   - `GET /api/done/{guid}`

## Indices importants

- `590`: trigger scenario.
- `605..622`: bloc scenario complet lu par firmware.
- `613`: index frequemment utilise pour bitmask lumiere (selon mapping projet).

## Symptomatique classique

### Cas

- Le web actionne correctement.
- MCP "envoie", mais rien ne se passe physiquement.

### Explication habituelle

Le payload MCP n'inclut pas le bloc complet `590 + 605..622`.

### Resolution

Normaliser dans MCP avant push Redis:

- Ajouter `590=1` si absent.
- Ajouter tout `605..622` avec valeur `0` par defaut.
- Conserver les indices explicitement demandes.

## Checklist de verification

- `essensys-backend` actif.
- Redis joignable.
- `LLEN essensys:global:actions` evolue apres injection.
- `GET /api/myactions` retourne les actions.
- Logs backend montrent consommation et ack.
