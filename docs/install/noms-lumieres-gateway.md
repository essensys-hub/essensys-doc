# Fichier des noms de la gateway (lumières et volets)

La gateway CM5 conserve les noms personnalisés des lumières (voir [Renommer une lumière](../utilisation/renommer-lumiere.md)) et des volets et stores (voir [Renommer un volet ou un store](../utilisation/renommer-volet.md)) dans un fichier JSON unique, `light-names.json`. Le fichier contient quatre sections : les noms (`lights`, `shutters`) et la disposition des objets, c'est-à-dire les objets masqués et leur ordre (`lights_layout`, `shutters_layout`, voir [Masquer et ordonner les lumières et les volets](../utilisation/masquer-ordonner-objets.md)).

## Emplacement

| Où | Chemin |
| --- | --- |
| Hôte CM5 | `/opt/data/light-names` |
| Conteneur backend | `/var/lib/essensys/names` (fichier `light-names.json`) |

Le chemin est donné au backend par la clé de configuration `light_names.path`. Le répertoire de l'hôte est monté en écriture dans le conteneur ; le reste de la configuration reste en lecture seule.

!!! warning "Recréer le conteneur"
    Ajouter ou changer ce montage demande de **recréer** le conteneur backend. Un simple `docker restart` ne suffit pas.

## Format

```json
{"version":1,"lights":{"dressing":{"name":"WC 3","version":2,"updated_at":"2026-11-07T10:15:30.123Z","updated_by":"nicolas@example.org"}}}
```

Avec les noms de volets, le fichier a une seconde section `shutters`, à côté de `lights` :

```json
{"version":1,"lights":{"dressing":{"name":"WC 3","version":2,"updated_at":"2026-11-07T10:15:30.123Z","updated_by":"nicolas@example.org"}},"shutters":{"volet1salon":{"name":"Volet baie vitrée","version":1,"updated_at":"2026-11-07T10:20:00.000Z","updated_by":"nicolas@example.org"}}}
```

Avec la disposition des objets, le fichier a deux sections de plus, `lights_layout` et `shutters_layout`. Ce sont des **objets** (un document par genre), pas des tables d'entrées :

```json
{"version":1,"lights":{},"shutters":{},"lights_layout":{"order":["salon","entree"],"disabled":["wc2"],"version":3,"updated_at":"2026-11-07T10:15:30.123Z","updated_by":"admin-local"},"shutters_layout":{"order":[],"disabled":["voletbureau"],"version":1,"updated_at":"2026-11-07T10:30:00.000Z","updated_by":"admin-local"}}
```

- `order` : identifiants dans l'ordre voulu (peut être incomplet ou vide : les identifiants absents sont ajoutés à la fin, dans l'ordre d'origine). `disabled` : identifiants masqués.
- Une section de disposition absente, ou de `version` 0, signifie : ordre d'origine, rien de masqué.
- Les identifiants inconnus sont ignorés.

- `name` vaut `null` après une remise au nom d'origine.
- `version` du fichier reste à 1. Une section absente est considérée comme vide.
- Écrire une section **conserve** l'autre section et toute section inconnue.
- L'écriture est atomique (fichier temporaire puis renommage) : le fichier n'est jamais à moitié écrit.
- Aucune nouvelle clé de configuration, aucun nouveau montage : le même fichier, la même clé `light_names.path` et le même répertoire servent aux quatre sections. Les sections de disposition utilisent aussi ce fichier et cette clé : un simple `docker restart` du conteneur suffit pour déployer la fonction des volets et celle de la disposition.

## Sauvegarde

Le répertoire `/opt/data/light-names` est sous `/opt/data` : il est sauvegardé avec le reste des données de la gateway. Pour une sauvegarde manuelle, copiez le fichier `light-names.json` ; pour restaurer, remettez-le en place et relancez le backend. La gateway renvoie ensuite ses noms et ses dispositions (lumières et volets) au cloud à la synchronisation suivante, et la modification la plus récente l'emporte.

!!! warning "Gateway restée à une version plus ancienne"
    Une gateway qui ne connaît que les noms de lumières (version de la fonction « Renommer une lumière »), ou les noms de lumières et de volets, efface les sections qu'elle ne connaît pas (`shutters`, `lights_layout`, `shutters_layout`) à sa prochaine écriture. Les noms et les dispositions sont alors rétablis depuis le cloud à la synchronisation suivante, car le cloud arbitre. Avant un retour arrière, copiez `light-names.json`.

## Ordre de déploiement

1. Le **cloud** d'abord (nouvelle table et nouvelles routes de disposition) : un cloud qui répond 404 aux routes de disposition ne perturbe pas une gateway déjà à jour.
2. La **gateway** ensuite, puis un `docker restart` du conteneur backend : aucun nouveau montage ni nouvelle clé de configuration.
3. Les portails et les applications en dernier.

## Dépannage : erreur 503 `names_unavailable`

Quand le stockage est absent ou non inscriptible (montage manquant, droits, disque plein), la gateway :

- **lit** normalement, en renvoyant les noms d'origine et la disposition par défaut (rien de masqué, ordre d'origine) ;
- **refuse l'écriture** d'un nom ou d'une disposition (lumières et volets) avec une erreur 503 `{"error":"names_unavailable"}`.

À vérifier dans l'ordre :

1. la clé `light_names.path` est présente dans la configuration du backend ;
2. le répertoire `/opt/data/light-names` existe sur l'hôte et est monté dans le conteneur sur `/var/lib/essensys/names` ;
3. le répertoire est inscriptible par l'utilisateur du conteneur et le disque n'est pas plein ;
4. le conteneur a bien été recréé après l'ajout du montage.
