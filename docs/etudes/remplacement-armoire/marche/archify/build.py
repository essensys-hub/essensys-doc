#!/usr/bin/env python3
"""Construit un schéma Archify des dossiers « Solutions du marché » (essensys-hub/essensys-doc#21).

Usage, depuis la racine du dépôt essensys-doc :

    ARCHIFY_DIR=/chemin/vers/archify/archify python3 docs/etudes/remplacement-armoire/marche/archify/build.py <nom> [<nom> ...]

``<nom>`` est le nom d'un fichier ``<nom>.architecture.json`` de ce dossier (par exemple
``knx-seule``). Le script ajoute au candidat les traductions françaises de l'interface
(``traductions-fr.json``) et le chemin de sortie, lance ``finalize`` d'Archify (dépôt
https://github.com/tt-a1i/archify, licence MIT), puis capture le rendu clair à 2048 px dans
``<nom>.png``. Le JSON du dossier reste la source versionnée ; le HTML et le PNG en sont issus.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REL = "docs/etudes/remplacement-armoire/marche/archify"


def run(args, cwd):
    return subprocess.run(args, cwd=cwd, capture_output=True, text=True)


def build(name: str, archify: str, root: str) -> int:
    src = os.path.join(HERE, name + ".architecture.json")
    with open(src, encoding="utf-8") as fh:
        cand = json.load(fh)
    with open(os.path.join(HERE, "traductions-fr.json"), encoding="utf-8") as fh:
        tr = json.load(fh)
    meta = cand.setdefault("meta", {})
    meta["locale"] = "fr"
    meta["translations"] = tr
    meta["output"] = f"{REL}/{name}.html"
    meta.setdefault("quality_profile", "showcase")
    work = tempfile.mkdtemp(prefix="archify-build-")
    try:
        tmp = os.path.join(work, name + ".json")
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(cand, fh, ensure_ascii=False, indent=2)
        out = os.path.join(root, meta["output"])
        r = run(["node", os.path.join(archify, "bin", "archify.mjs"), "finalize", "architecture", tmp, out,
                 "--quality", "showcase", "--out-dir", os.path.join(work, "finalize"), "--json"], root)
        sys.stdout.write(r.stdout[-3000:])
        sys.stderr.write(r.stderr[-1500:])
        if r.returncode != 0:
            return r.returncode
        r = run(["node", os.path.join(archify, "bin", "archify.mjs"), "visual-check", out, "--summary",
                 "--out-dir", os.path.join(work, "visual")], root)
        shot = None
        try:
            info = json.loads(r.stdout)
            cands = [p for p in json.dumps(info).split('"') if p.endswith(".png") and "light" in p.lower() and "2048" in p]
            shot = cands[0] if cands else None
        except Exception:
            pass
        if not shot:
            for dp, _, fs in os.walk(os.path.join(work, "visual")):
                for f in fs:
                    if f.endswith(".png") and "light" in f.lower() and "2048" in f:
                        shot = os.path.join(dp, f)
        if not shot:
            print("capture introuvable pour", name)
            return 2
        shutil.copyfile(shot, os.path.join(HERE, name + ".png"))
        for ext in (".delivery.json",):
            p = out[:-5] + ext
            if os.path.exists(p):
                os.remove(p)
        print("ok", name)
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


def main(argv):
    archify = os.environ.get("ARCHIFY_DIR")
    if not archify or not os.path.exists(os.path.join(archify, "bin", "archify.mjs")):
        raise SystemExit("ARCHIFY_DIR doit pointer vers le dossier archify/archify (bin/archify.mjs).")
    root = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))
    rc = 0
    for name in argv:
        rc = max(rc, build(name, archify, root))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
