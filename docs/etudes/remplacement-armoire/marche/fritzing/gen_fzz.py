#!/usr/bin/env python3
"""Génère les câblages Fritzing des dossiers « Solutions du marché » (essensys-hub/essensys-doc#21).

Chaque câblage décrit, pour une solution, le chemin d'**un poussoir vers une charge** avec les
modules de la solution. Il est lu dans ``specs/<solution>.json`` et produit :

- ``<solution>.fzz`` : croquis Fritzing (pièces dessinées ici et embarquées dans le fichier) ;
- ``<solution>_breadboard.svg`` et ``<solution>_breadboard.png`` : vue exportée par Fritzing.

Usage (depuis ce dossier) : ``python3 gen_fzz.py [solution ...]``. Sans argument, tous les
croquis de ``specs/`` sont produits. L'export demande Fritzing 1.0.x installé
(``/Applications/Fritzing.app``) ; ``--no-export`` ne produit que les ``.fzz``.

Format d'un fichier de spécification : voir ``specs/knx.json`` (blocs rangés en colonnes et en
rangées, broches à gauche et à droite, fils orthogonaux entre deux broches). Les câblages sont des
**principes**, non validés au banc : chaque image le dit.

Unité : px de vue platine, 90 px par pouce. Les pièces sont des boîtiers schématiques, pas les
pièces réelles des fabricants.
"""

from __future__ import annotations

import html
import json
import os
import subprocess
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"
STAMP = (2026, 10, 24, 0, 0, 0)
FRITZING = "/Applications/Fritzing.app/Contents/MacOS/Fritzing"
FS = 1.4   # échelle du texte et des pas de ligne
WS = 1.25  # échelle des largeurs de bloc données par les spécifications
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# couleur et libellé par défaut de chaque type de fil
NETS = {
    "bouton": ("#e0b000", "poussoir : contact sec vers le module d'entrées"),
    "bus": ("#2f6fd0", "bus ou liaison de données"),
    "tbts": ("#d01c1c", "alimentation TBTS (24 V, 12 V ou 5 V)"),
    "0v": ("#202020", "0 V commun"),
    "phase": ("#8a4b1a", "230 V : phase"),
    "neutre": ("#6fa8dc", "230 V : neutre"),
    "ordre": ("#2a9a2a", "ordre : sortie d'un module vers un autre"),
    "reseau": ("#7a3fb0", "réseau local (Ethernet, Wi-Fi)"),
}
KIND_FILL = {
    "poussoir": "#e8e8e4",
    "module": "#dfe7ee",
    "entrees": "#e4efe0",
    "actionneur": "#f1e6d3",
    "controleur": "#d9d2ec",
    "bus": "#cfe0f7",
    "alim": "#f4d4d0",
    "charge": "#fff3c4",
    "passerelle": "#d3ead8",
    "note": "#ffffff",
}


def esc(t: str) -> str:
    return html.escape(str(t), quote=True)


def txt(x, y, s, size=5.2, anchor="start", color="#111", weight="normal"):
    return (f'<text x="{x:.2f}" y="{y:.2f}" font-size="{size}" font-family="{FONT}" fill="{color}" '
            f'font-weight="{weight}" text-anchor="{anchor}">{esc(s)}</text>')


def wrap(text: str, width: int) -> list[str]:
    words, lines, cur = str(text).split(), [], ""
    for w in words:
        if cur and len(cur) + 1 + len(w) > width:
            lines.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        lines.append(cur)
    return lines


class Part:
    def __init__(self, mid, title, w, h, body, pins, label="X"):
        self.mid, self.title, self.w, self.h, self.body, self.label = mid, title, w, h, body, label
        self.pins = list(pins)  # (nom, x, y)

    def pin(self, name):
        for n, x, y in self.pins:
            if n == name:
                return x, y
        raise KeyError(name)

    def cid(self, name):
        return "connector%d" % [n for n, _, _ in self.pins].index(name)

    def files(self):
        conns = ""
        for i, (n, _, _) in enumerate(self.pins):
            conns += (f'<connector id="connector{i}" name="{esc(n)}" type="male"><description>{esc(n)}</description><views>'
                      f'<breadboardView><p layer="breadboard" svgId="connector{i}pin"/></breadboardView>'
                      f'<schematicView><p layer="schematic" svgId="connector{i}pin"/></schematicView>'
                      f'<pcbView><p layer="copper0" svgId="connector{i}pin"/><p layer="copper1" svgId="connector{i}pin"/></pcbView>'
                      f'</views></connector>')
        fzp = (f'<?xml version="1.0" encoding="UTF-8"?>\n<module fritzingVersion="1.0.2" moduleId="{self.mid}"><version>1</version>'
               f'<title>{esc(self.title)}</title><label>{esc(self.label)}</label><author>Essensys</author>'
               f'<properties><property name="family">essensys-marche</property></properties><description>{esc(self.title)}</description>'
               f'<views><iconView><layers image="breadboard/{self.mid}_bb.svg"><layer layerId="icon"/></layers></iconView>'
               f'<breadboardView><layers image="breadboard/{self.mid}_bb.svg"><layer layerId="breadboard"/></layers></breadboardView>'
               f'<schematicView><layers image="schematic/{self.mid}_sch.svg"><layer layerId="schematic"/></layers></schematicView>'
               f'<pcbView><layers image="pcb/{self.mid}_pcb.svg"><layer layerId="copper0"/><layer layerId="copper1"/></layers></pcbView>'
               f'</views><connectors>{conns}</connectors></module>\n')
        head = f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w / 90:.5f}in" height="{self.h / 90:.5f}in" viewBox="0 0 {self.w} {self.h}">'
        hidden = "".join(f'<rect id="connector{i}pin" x="{x - 1.5:.2f}" y="{y - 1.5:.2f}" width="3" height="3" fill="none" stroke="none"/>'
                         for i, (_, x, y) in enumerate(self.pins))
        return {
            f"part.{self.mid}.fzp": fzp,
            f"svg.breadboard.{self.mid}_bb.svg": f'{head}<g id="breadboard">{self.body}{hidden}</g></svg>',
            f"svg.schematic.{self.mid}_sch.svg": f'{head}<g id="schematic">{hidden}</g></svg>',
            f"svg.pcb.{self.mid}_pcb.svg": f'{head}<g id="copper0"><g id="copper1">{hidden}</g></g></svg>',
        }


def icon(kind: str, w: float) -> str:
    """Petit pictogramme en haut à droite du bloc."""
    x = w - 22
    if kind == "poussoir":
        return (f'<circle cx="{x + 8}" cy="14" r="7" fill="#9a9a9a" stroke="#555" stroke-width="0.8"/>'
                f'<circle cx="{x + 8}" cy="14" r="4" fill="#d0d0d0" stroke="#777" stroke-width="0.6"/>')
    if kind == "charge":
        return (f'<circle cx="{x + 8}" cy="14" r="7" fill="#ffe680" stroke="#b08a00" stroke-width="0.8"/>'
                f'<path d="M{x + 4} 14 q4 -6 8 0" fill="none" stroke="#b08a00" stroke-width="0.8"/>')
    if kind == "alim":
        return (f'<rect x="{x}" y="7" width="16" height="14" rx="2" fill="#fff" stroke="#a33" stroke-width="0.8"/>'
                + txt(x + 8, 17, "V", 7, "middle", "#a33", "bold"))
    if kind in ("bus", "controleur", "passerelle"):
        return (f'<rect x="{x}" y="8" width="16" height="12" rx="1.5" fill="#fff" stroke="#556" stroke-width="0.8"/>'
                f'<line x1="{x + 3}" y1="12" x2="{x + 13}" y2="12" stroke="#556" stroke-width="0.8"/>'
                f'<line x1="{x + 3}" y1="16" x2="{x + 13}" y2="16" stroke="#556" stroke-width="0.8"/>')
    return ""


def make_block(spec_slug: str, b: dict) -> Part:
    kind = b.get("kind", "module")
    w = float(b.get("width", 190)) * WS
    left, right = b.get("left", []), b.get("right", [])
    title_lines = wrap(b["label"], int(w / (4.4 * FS)))
    sub_lines = wrap(b.get("sublabel", ""), int((w - 8) / (3.1 * FS))) if b.get("sublabel") else []
    note_lines = [ln for n in b.get("notes", []) for ln in wrap(n, int((w - 8) / (3.0 * FS)))]
    top = 10 + 9 * FS * len(title_lines) + 6.2 * FS * len(sub_lines) + 4
    rows = max(len(left), len(right))
    pins_h = 9 * FS * rows
    h = top + pins_h + (6.0 * FS * len(note_lines) + 4 if note_lines else 0) + 6
    fill = KIND_FILL.get(kind, "#dfe7ee")
    body = (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="5" fill="{fill}" stroke="#667" stroke-width="0.9"/>'
            + icon(kind, w))
    y = 8 + 7.2 * FS
    for ln in title_lines:
        body += txt(8, y, ln, 7.2 * FS, weight="bold")
        y += 9 * FS
    for ln in sub_lines:
        body += txt(8, y - 1.5, ln, 4.7 * FS, color="#445")
        y += 6.2 * FS
    pins = []
    py = top + 4 * FS
    for i in range(rows):
        if i < len(left):
            body += txt(6, py + 1.6, left[i], 4.9 * FS)
            pins.append((f"L:{left[i]}", 0.0, py))
            body += f'<circle cx="0" cy="{py}" r="2.2" fill="#c8a24a" stroke="#8a6a20" stroke-width="0.5"/>'
        if i < len(right):
            body += txt(w - 6, py + 1.6, right[i], 4.9 * FS, "end")
            pins.append((f"R:{right[i]}", w, py))
            body += f'<circle cx="{w}" cy="{py}" r="2.2" fill="#c8a24a" stroke="#8a6a20" stroke-width="0.5"/>'
        py += 9 * FS
    ny = top + pins_h + 4 * FS
    for ln in note_lines:
        body += txt(8, ny, ln, 4.4 * FS, color="#744")
        ny += 6.0 * FS
    return Part(f"essensys_marche_{spec_slug}_{b['id']}", b["label"], w, h, body, pins, b["id"][:8].upper())


def caption_part(spec_slug, mid, lines, w, size=5.6, color="#333", bold_first=False, fill=None):
    h = 6 + 8.2 * FS * len(lines)
    body = ""
    if fill:
        body += f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="4" fill="{fill}" stroke="#999" stroke-width="0.6"/>'
    y = 4 + 5.6 * FS
    for i, ln in enumerate(lines):
        body += txt(5 if fill else 0, y, ln, (size + (1.8 if (bold_first and i == 0) else 0)) * FS, color=color,
                    weight="bold" if (bold_first and i == 0) else "normal")
        y += (8.2 + (1.5 if (bold_first and i == 0) else 0)) * FS
    return Part(f"essensys_marche_{spec_slug}_{mid}", mid, w, h + 2, body, [], "TX")


def legend_part(spec_slug, nets_used, w=330):
    h = 8 + 9 * FS * (len(nets_used) + 1)
    body = (f'<rect x="0.5" y="0.5" width="{w - 1}" height="{h - 1}" rx="4" fill="#ffffff" stroke="#999" stroke-width="0.6"/>'
            + txt(5, 5 + 6.4 * FS, "Légende des fils", 6.4 * FS, weight="bold"))
    y = 8 + 9 * FS * 2 - 3
    for n in nets_used:
        color, label = NETS[n]
        body += f'<line x1="5" y1="{y - 1.8}" x2="28" y2="{y - 1.8}" stroke="{color}" stroke-width="2.6" stroke-linecap="round"/>'
        body += txt(34, y, label, 4.9 * FS)
        y += 9 * FS
    return Part(f"essensys_marche_{spec_slug}_legende", "Légende", w, h, body, [], "LG")


class Sketch:
    def __init__(self, name):
        self.name, self.instances, self.parts, self.idx, self.pos = name, [], {}, {}, {}
        self.wires = []
        self.n = 1000

    def add(self, key, part, x, y, z=2.5):
        self.n += 1
        self.idx[key], self.parts[key], self.pos[key] = self.n, part, (x, y)
        self.instances.append(f'<instance moduleIdRef="{part.mid}" modelIndex="{self.n}" path="{part.mid}.fzp"><title>{esc(key)}</title>'
                              f'<views><breadboardView layer="breadboard"><geometry z="{z}" x="{x:.3f}" y="{y:.3f}"/></breadboardView></views></instance>')

    def at(self, key, pin):
        x, y = self.pos[key]
        px, py = self.parts[key].pin(pin)
        return (round(x + px, 3), round(y + py, 3))

    def route(self, net, a, pts, b):
        self.wires.append((net, a, list(pts), b))

    def build(self, target):
        segs = []
        for w, (net, a, pts, b) in enumerate(self.wires):
            path = [self.at(*a)] + pts + [self.at(*b)]
            keys = [("P",) + tuple(a)] + [("B", w, k) for k in range(len(pts))] + [("P",) + tuple(b)]
            for k in range(len(path) - 1):
                segs.append((net, path[k], path[k + 1], keys[k], keys[k + 1]))
        ends = {}
        for s, seg in enumerate(segs):
            for side in (0, 1):
                ends.setdefault(seg[3 + side], []).append((s, side))
        out = []
        for s, (net, p1, p2, ka, kb) in enumerate(segs):
            conns = []
            for side, key in ((0, ka), (1, kb)):
                c = []
                if key[0] == "P":
                    part = self.parts[key[1]]
                    c.append(f'<connect connectorId="{part.cid(key[2])}" modelIndex="{self.idx[key[1]]}" layer="breadboard"/>')
                for (o, oside) in ends[key]:
                    if (o, oside) != (s, side):
                        c.append(f'<connect connectorId="connector{oside}" modelIndex="{5000 + o}" layer="breadboardWire"/>')
                conns.append(f'<connector connectorId="connector{side}" layer="breadboardWire"><geometry x="0" y="0"/><connects>{"".join(c)}</connects></connector>')
            out.append(f'<instance moduleIdRef="WireModuleID" modelIndex="{5000 + s}" path=":/resources/parts/core/wire.fzp"><title>Fil {net} {s}</title><views>'
                       f'<breadboardView layer="breadboardWire"><geometry z="3.5" x="{p1[0]:.3f}" y="{p1[1]:.3f}" x1="0" y1="0" '
                       f'x2="{p2[0] - p1[0]:.3f}" y2="{p2[1] - p1[1]:.3f}" wireFlags="64"/>'
                       f'<wireExtras mils="13" color="{NETS[net][0]}" opacity="1" banded="0"/><connectors>{"".join(conns)}</connectors>'
                       f'</breadboardView></views></instance>')
        fz = ('<?xml version="1.0" encoding="UTF-8"?>\n<module fritzingVersion="1.0.2"><views>'
              '<view name="breadboardView" backgroundColor="#ffffff" gridSize="0.1in" showGrid="0" alignToGrid="1" viewFromBelow="0"/>'
              '<view name="schematicView" backgroundColor="#ffffff" gridSize="0.1in" showGrid="1" alignToGrid="1" viewFromBelow="0"/>'
              '<view name="pcbView" backgroundColor="#333333" gridSize="0.05in" showGrid="1" alignToGrid="1" viewFromBelow="0"/>'
              '</views><instances>\n' + "\n".join(self.instances + out) + "\n</instances></module>\n")
        with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as z:
            z.writestr(zipfile.ZipInfo(self.name + ".fz", date_time=STAMP), fz)
            seen = set()
            for part in self.parts.values():
                if part.mid in seen:
                    continue
                seen.add(part.mid)
                for k, v in sorted(part.files().items()):
                    z.writestr(zipfile.ZipInfo(k, date_time=STAMP), v)
        return len(segs)


def build_sketch(slug: str, spec: dict) -> tuple[Sketch, list[str]]:
    sk = Sketch(slug)
    blocks = {b["id"]: b for b in spec["blocks"]}
    parts = {i: make_block(slug, b) for i, b in blocks.items()}
    ncols = 1 + max(b["col"] for b in blocks.values())
    nrows = 1 + max(b["row"] for b in blocks.values())
    colw = [max([parts[i].w for i, b in blocks.items() if b["col"] == c] or [0]) for c in range(ncols)]
    rowh = [max([parts[i].h for i, b in blocks.items() if b["row"] == r] or [0]) for r in range(nrows)]
    gap_x, gap_y, x0, y0 = 120, 34, 30, 90
    colx = [x0 + sum(colw[:c]) + gap_x * c for c in range(ncols)]
    rowy = [y0 + sum(rowh[:r]) + gap_y * r for r in range(nrows)]
    for i, b in blocks.items():
        sk.add(i, parts[i], colx[b["col"]], rowy[b["row"]], z=2.5)
    width = colx[-1] + colw[-1] + 30
    height = rowy[-1] + rowh[-1]
    sk.add("titre", caption_part(slug, "titre", [spec["title"], spec["subtitle"]], max(width - 30, 420), 5.4, "#222", True), x0, 6, z=4)
    lane = {}
    used = []
    for net, a, b in spec["wires"]:
        (ka, pa), (kb, pb) = a.split(".", 1), b.split(".", 1)
        # un fil part toujours de la broche de droite d'un bloc vers la broche de gauche d'un autre,
        # sauf liaison dans la même colonne ou vers la gauche (broches de même côté)
        sa = "R:" + pa if ("R:" + pa) in [p[0] for p in parts[ka].pins] else "L:" + pa
        sb = "L:" + pb if ("L:" + pb) in [p[0] for p in parts[kb].pins] else "R:" + pb
        pta, ptb = sk.at(ka, sa), sk.at(kb, sb)
        ca, cb = blocks[ka]["col"], blocks[kb]["col"]
        if ca < cb:
            if cb - ca > 1:
                # colonnes sautées : le fil longe la rangée de départ et monte juste avant la cible
                k = lane.setdefault(("d", cb), 0)
                lane[("d", cb)] = k + 1
                mx = colx[cb] - 14 - 9 * k
            else:
                k = lane.setdefault(ca, 0)
                lane[ca] = k + 1
                mx = colx[ca] + colw[ca] + 18 + 9 * k
                if mx > colx[cb] - 14:
                    mx = colx[cb] - 14
            pts = [(mx, pta[1]), (mx, ptb[1])]
        else:
            # liaison arrière ou verticale : contourne par le bas du dessin
            k = lane.setdefault(("b", ca), 0)
            lane[("b", ca)] = k + 1
            by = height + y0 + 14 + 9 * k
            side = 16 if sa.startswith("R:") else -16
            pts = [(pta[0] + side, pta[1]), (pta[0] + side, by), (ptb[0] - 16 if sb.startswith("L:") else ptb[0] + 16, by),
                   (ptb[0] - 16 if sb.startswith("L:") else ptb[0] + 16, ptb[1])]
        sk.route(net, (ka, sa), pts, (kb, sb))
        if net not in used:
            used.append(net)
    nback = sum(1 for k in lane if isinstance(k, tuple) and k[0] == "b")
    ly = height + 30 + 9 * nback
    sk.add("legende", legend_part(slug, used), x0, ly, z=4)
    notes = spec.get("notes", []) + ["Principe de câblage, non validé au banc. Estimations d'octobre 2026 à confirmer par un électricien, des devis, les fabricants et des essais."]
    lines = [ln for n in notes for ln in wrap(n, 150)]
    sk.add("reserve", caption_part(slug, "reserve", lines, max(width - 420, 380), 5.0, "#744", False, "#fff8f0"), x0 + 360, ly, z=4)
    return sk, used


def export(slug: str) -> None:
    """Exporte la vue platine par Fritzing puis le PNG par Chrome sans interface."""
    tmp = os.path.join(HERE, ".export-" + slug)
    os.makedirs(tmp, exist_ok=True)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.replace(os.path.join(HERE, slug + ".fzz"), os.path.join(tmp, slug + ".fzz"))
    try:
        subprocess.run([FRITZING, "-svg", tmp], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180, check=False)
    finally:
        os.replace(os.path.join(tmp, slug + ".fzz"), os.path.join(HERE, slug + ".fzz"))
    svg = os.path.join(tmp, slug + "_breadboard.svg")
    if not os.path.exists(svg):
        raise SystemExit(f"export Fritzing absent pour {slug}")
    os.replace(svg, os.path.join(HERE, slug + "_breadboard.svg"))
    import re
    with open(os.path.join(HERE, slug + "_breadboard.svg"), encoding="utf-8") as fh:
        head = fh.read(2000)
    mw = re.search(r'width="([\d.]+)in"', head)
    mh = re.search(r'height="([\d.]+)in"', head)
    # Fritzing exporte en pouces : 96 px CSS par pouce
    w = int(float(mw.group(1)) * 96) + 4 if mw else 1600
    h = int(float(mh.group(1)) * 96) + 4 if mh else 900
    png = os.path.join(HERE, slug + "_breadboard.png")
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    f"--window-size={w},{h}", f"--screenshot={png}", "file://" + os.path.join(HERE, slug + "_breadboard.svg")],
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120, check=False)
    for f in os.listdir(tmp):
        os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)


def main(argv):
    do_export = "--no-export" not in argv
    slugs = [a for a in argv if not a.startswith("--")]
    if not slugs:
        slugs = sorted(f[:-5] for f in os.listdir(os.path.join(HERE, "specs")) if f.endswith(".json"))
    for slug in slugs:
        with open(os.path.join(HERE, "specs", slug + ".json"), encoding="utf-8") as fh:
            spec = json.load(fh)
        sk, used = build_sketch(slug, spec)
        n = sk.build(os.path.join(HERE, slug + ".fzz"))
        print("ok", slug + ".fzz", n, "segments", used)
        if do_export:
            export(slug)
            print("  export", slug + "_breadboard.svg/.png")


if __name__ == "__main__":
    main(sys.argv[1:])
