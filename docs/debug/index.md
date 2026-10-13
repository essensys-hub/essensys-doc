# Outils de debug

Outils pour comprendre ce qui se passe **dans** l'armoire Essensys quand une commande n'aboutit pas, sans modifier ni le firmware ni la gateway.

!!! danger "Règles communes"
    - Ces outils **observent** : ils n'émettent jamais rien sur le bus et ne pilotent jamais l'armoire.
    - Tout branchement dans le coffret se fait **hors tension**, par une **personne habilitée**.
    - Le 0 V de l'armoire n'est **jamais** relié au PE : l'outil de mesure ne doit pas créer de pont de masse (voir le [retour d'expérience foudre](../retex/foudre-2026/synthese.md)).

| Outil | À quoi il sert | Matériel |
|---|---|---|
| [Espion I2C passif](espion-i2c.md) | Voir les trames échangées entre le boîtier principal (BP) et les boîtiers auxiliaires (BA) : BA absent, trame rejetée, bus bloqué, commande abandonnée | Analyseur logique USB (≈ 10 €), Raspberry Pi sur batterie, petite sonde à fabriquer |

Avant de sortir un outil, commencez par les contrôles en lecture seule de la gateway, décrits dans [Ajouter ou remplacer un BP](../install/ajout-bp.md#procedure) : voyant SERVEUR, journaux du backend, index 12.
