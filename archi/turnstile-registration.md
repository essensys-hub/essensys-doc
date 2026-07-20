# Inscription publique — Cloudflare Turnstile

Protection anti-spam de l'inscription email/password sur `www.essensys.fr`
(`POST /api/auth/register`).

OpenSpec : `essensys-turnstile-registration-2026-07-036`  
Ops détaillée (support-site) : dépôt `essensys-support-site` → `docs/turnstile-registration.md`

## Compte Cloudflare propriétaire

Le widget Turnstile et les clés de vérification (site key + secret) sont gérés
dans le compte Cloudflare suivant :

| Champ | Valeur |
|-------|--------|
| **Email du compte** | `nicolas.rineau@gmail.com` |
| **Statut** | Email **Verified** (profil Cloudflare → My Profile → Settings) |
| **Membre depuis** | 20 juillet 2024 |

Ce compte détient :

- le site Turnstile (mode **managed**) utilisé pour `/register` ;
- les hostnames autorisés (`www.essensys.fr`, `mon.essensys.fr`, `test.essensys.fr`, etc.) ;
- la **Site Key** (publique, build Vite `VITE_TURNSTILE_SITE_KEY`) ;
- la **Secret Key** (serveur uniquement, `TURNSTILE_SECRET_KEY` via SOPS).

> Toute rotation de clés, ajout de domaine ou changement de mode de widget
> doit être faite **dans ce compte**, puis rejouée dans SOPS / déploiement OVH.
> Ne pas créer un second widget sous un autre compte Cloudflare sans migrer
> explicitement les secrets et le build frontend.

## Flux applicatif

```text
Browser /register
  → widget Turnstile (site key, compte ci-dessus)
  → POST /api/auth/register { …, turnstile_token }
       → rate-limit IP + honeypot
       → siteverify Cloudflare (secret serveur) ──fail──→ 400/403
       → CreateUser
```

| Couche | Dépôt / composant |
|--------|-------------------|
| UI | `essensys-support-site` — `Register.jsx` |
| API prod | `essensys-user-portal-backend` — `identity.Register` |
| Secrets | `essensys-ansible` — `secrets/cloud/essensys.sops.yaml` |

Les créations d'utilisateurs **admin** (User Manager) ne passent pas par Turnstile.
Le protocole legacy IoT (`/api/serverinfos`, `mystatus`, `myactions`, `done`) n'est pas concerné.

## Secrets (rappel)

Dans SOPS cloud, clés acceptées :

- `TURNSTILE_SECRET_KEY` ou `vault_turnstile_secret_key`
- `VITE_TURNSTILE_SITE_KEY` ou `vault_turnstile_site_key`

Jamais de secret en clair dans git. Rotation : dashboard Cloudflare (compte ci-dessus)
→ `sops secrets/cloud/essensys.sops.yaml` → redeploy cloud-backend + SPA.

## Smoke

```bash
# Sans token → doit échouer (aucun compte créé)
curl -sS -X POST https://www.essensys.fr/api/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"bot@example.com","password":"test-pass-1234"}' -w '\n%{http_code}\n'
```

Inscription humaine : `https://www.essensys.fr/register` (widget Turnstile visible).
