#!/usr/bin/env bash
# Prepare vendored install pages and architecture symlinks for MkDocs build.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ARCH="$ROOT/docs/architecture"
INSTALL="$ROOT/docs/install"

mkdir -p "$ARCH" "$INSTALL" "$INSTALL/img"
rm -f "$INSTALL/gateway-cm5.md" "$INSTALL/https-local.md" "$INSTALL/raspberry-index.md"

link_arch() {
  local name="$1"
  local dest_name="${2:-$1}"
  local src="$ROOT/archi/$name"
  if [[ -f "$src" ]]; then
    ln -sfn "../../archi/$name" "$ARCH/$dest_name"
  fi
}

link_arch index.md overview.md
for f in "$ROOT/archi"/*.md; do
  base="$(basename "$f")"
  [[ "$base" == "index.md" ]] && continue
  link_arch "$base"
done
if [[ -d "$ROOT/archi/img" ]]; then
  ln -sfn "../../archi/img" "$ARCH/img"
fi
mkdir -p "$ROOT/docs/new_feature"
for f in errata-table-echange.md firmware-v2-local-fullstatus.md; do
  if [[ -f "$ROOT/new_feature/$f" ]]; then
    ln -sfn "../../new_feature/$f" "$ROOT/docs/new_feature/$f"
  fi
done

copy_with_banner() {
  local src="$1"
  local dest="$2"
  local label="$3"
  if [[ ! -f "$src" ]]; then
    return 1
  fi
  {
    echo "> **Source canonique** : \`$label\`"
    echo
    cat "$src"
  } > "$dest"
  return 0
}

fix_ansible_doc_links() {
  local file="$1"
  python3 - "$file" << 'PY'
import re, sys
path = sys.argv[1]
base = "https://github.com/essensys-hub/essensys-ansible/blob/main/docs"
text = open(path, encoding="utf-8").read()
pattern = r"\]\((tls-local-domain\.md|playbooks\.md|ports-reference\.md|nginx-vs-caddy\.md|roles\.md|guide-utilisateur-https-local\.md)(#[^)]*)?\)"
text = re.sub(pattern, lambda m: f"]({base}/{m.group(1)}{m.group(2) or ''})", text)
open(path, "w", encoding="utf-8").write(text)
PY
}

resolve_src() {
  local relpath="$1"
  for base in "$ROOT/../essensys-ansible" "$ROOT/vendor/essensys-ansible" "$ROOT/vendor/ansible"; do
    if [[ -f "$base/$relpath" ]]; then
      echo "$base/$relpath"
      return 0
    fi
  done
  return 1
}

resolve_ansible_root() {
  for base in "$ROOT/../essensys-ansible" "$ROOT/vendor/essensys-ansible" "$ROOT/vendor/ansible"; do
    if [[ -d "$base/docs" ]]; then
      echo "$base"
      return 0
    fi
  done
  return 1
}

ANSIBLE_ROOT="$(resolve_ansible_root || true)"
if [[ -z "$ANSIBLE_ROOT" ]]; then
  echo "ERROR: essensys-ansible not found" >&2
  exit 1
fi

if [[ -d "$ANSIBLE_ROOT/docs/img" ]]; then
  rsync -a "$ANSIBLE_ROOT/docs/img/" "$INSTALL/img/"
fi

GW="$ANSIBLE_ROOT/docs/install-gateway.md"
HTTPS="$ANSIBLE_ROOT/docs/guide-utilisateur-https-local.md"

copy_with_banner "$GW" "$INSTALL/gateway-cm5.md" "essensys-ansible/docs/install-gateway.md"
fix_ansible_doc_links "$INSTALL/gateway-cm5.md"

copy_with_banner "$HTTPS" "$INSTALL/https-local.md" "essensys-ansible/docs/guide-utilisateur-https-local.md"
fix_ansible_doc_links "$INSTALL/https-local.md"

cat > "$INSTALL/raspberry-pi.md" << 'EOF'
# Installation Raspberry Pi (classique)

Installation Essensys sur **Raspberry Pi 4** (profil mono-NIC, stack Docker Compose).

## Documentation complete

La documentation detaillee (OS, reseau, WAN, logs, maintenance) est publiee sur
**GitHub Pages** :

**[essensys-raspberry-install](https://essensys-hub.github.io/essensys-raspberry-install/)**

## Gateway CM5 (double NIC)

Pour une installation **CM5 gateway** (eth0 WAN + eth1 armoire), voir
[Installation gateway CM5](gateway-cm5.md).

## Source canonique

Depot `essensys-hub/essensys-raspberry-install` — playbook Ansible :
[install.raspberrypi.yml](https://github.com/essensys-hub/essensys-ansible/blob/main/docs/playbooks.md#installation-raspberry-pi-classique).
EOF

echo "prepare-docs: OK ($ARCH, $INSTALL)"
