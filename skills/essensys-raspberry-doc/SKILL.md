---
name: essensys-raspberry-doc
description: Enforces documentation sync for Essensys repositories. Use when code changes touch essensys-raspberry-install, essensys-server-backend, essensys-server-frontend, or essensys-ansible, and update docs in essensys-raspberry-install/docs plus versions.md changelog entry.
---

# Essensys Raspberry Doc Sync

## Goal

Keep `essensys-raspberry-install/docs` aligned with code changes across:

- `essensys-raspberry-install`
- `essensys-server-backend`
- `essensys-server-frontend`
- `essensys-ansible`

Default behavior is strong: do doc updates before closing work, unless there is a clear reason and it is explicitly documented.

## Mandatory workflow

1. Identify impacted repo(s) and changed behavior.
2. Update existing relevant doc pages in `essensys-raspberry-install/docs`.
3. Add/update a version note in `essensys-raspberry-install/docs/versions.md`.
4. In final response, include a short **Doc Sync** section listing updated doc files.

## Mapping rules

- Backend/MCP/API/Redis changes -> `docs/architecture/backend.md`, `docs/maintenance/debug.md`, `docs/maintenance/troubleshooting.md`
- Frontend/UI changes -> `docs/architecture/frontend.md`, `docs/acces/local.md`, `docs/acces/wan.md`
- Nginx/Traefik/ports/routing/auth changes -> `docs/architecture/nginx.md`, `docs/architecture/traefik.md`, `docs/architecture/ports.md`, `docs/acces/*.md`
- Installer/update/uninstall/ops scripts -> `docs/installation/*.md`, `docs/maintenance/update.md`, `docs/maintenance/uninstall.md`
- Monitoring/service changes -> `docs/monitor.md`, `docs/logs/*.md`, `docs/maintenance/debug.md`

Always prefer updating existing pages over creating new files.

## Version entry policy

When changes are user-visible or operational:

- Update `docs/versions.md` table row for current version or add a new row.
- Add a short bullet list in the related "Détails de la Version ..." section.

If no version bump is decided yet, still add a concise note under the current active version details.

## Exception policy

If no doc change is needed:

1. Explain why in one sentence.
2. Add a "No doc impact" line in the final response.

Do not skip this explanation.

## Final response format

Add this block at the end:

```markdown
## Doc Sync
- Updated: `path/to/doc1.md`, `path/to/doc2.md`
- Version note: `essensys-raspberry-install/docs/versions.md` (updated|not needed + reason)
```

## Additional resource

- Detailed checklist: [reference.md](reference.md)
