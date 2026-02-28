# Reference Checklist

## Quick checklist

- [ ] Did code change in one of the 4 Essensys repos?
- [ ] Did I update at least one relevant page in `essensys-raspberry-install/docs`?
- [ ] Did I update `docs/versions.md` (or justify why not)?
- [ ] Did I include a "Doc Sync" block in final response?

## Suggested per-repo documentation targets

### `essensys-server-backend`

- `docs/architecture/backend.md`
- `docs/maintenance/debug.md`
- `docs/maintenance/troubleshooting.md`
- `docs/logs/backend.md`

### `essensys-server-frontend`

- `docs/architecture/frontend.md`
- `docs/acces/local.md`
- `docs/acces/wan.md`

### `essensys-ansible`

- `docs/installation/essensys-installation.md`
- `docs/maintenance/update.md`
- `docs/maintenance/uninstall.md`
- `docs/architecture/nginx.md`
- `docs/architecture/traefik.md`
- `docs/architecture/ports.md`

### `essensys-raspberry-install`

- `docs/installation/*.md`
- `docs/maintenance/*.md`
- `docs/monitor.md`

## Entry template for versions.md

Use concise bullets under the active version details:

- **Docs sync**: mention key behavior changes.
- **Ops impact**: mention install/update/uninstall or routing implications.

Example:

- **Réseau** : suppression de Caddy, stack WAN unifiée sur Traefik.
- **Maintenance** : ajout du script `uninstall.homeassitantsh`.
