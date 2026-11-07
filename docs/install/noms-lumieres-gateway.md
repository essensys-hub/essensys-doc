# Fichier des noms de la gateway (lumières et volets)

La gateway CM5 conserve les noms personnalisés des lumières (voir [Renommer une lumière](../utilisation/renommer-lumiere.md)) et des volets et stores (voir [Renommer un volet ou un store](../utilisation/renommer-volet.md)) dans un fichier JSON unique, `light-names.json`. Le fichier contient deux sections, `lights` et `shutters`.

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

- `name` vaut `null` après une remise au nom d'origine.
- `version` du fichier reste à 1. Une section absente est considérée comme vide.
- Écrire une section **conserve** l'autre section et toute section inconnue.
- L'écriture est atomique (fichier temporaire puis renommage) : le fichier n'est jamais à moitié écrit.
- Aucune nouvelle clé de configuration, aucun nouveau montage : le même fichier, la même clé `light_names.path` et le même répertoire servent aux deux sections. Un simple `docker restart` du conteneur suffit pour déployer la fonction des volets.

## Sauvegarde

Le répertoire `/opt/data/light-names` est sous `/opt/data` : il est sauvegardé avec le reste des données de la gateway. Pour une sauvegarde manuelle, copiez le fichier `light-names.json` ; pour restaurer, remettez-le en place et relancez le backend. La gateway renvoie ensuite ses noms (lumières et volets) au cloud à la synchronisation suivante, et la modification la plus récente l'emporte.

!!! warning "Retour arrière vers la version des lumières seules"
    Une gateway repassée à la version qui ne connaît que les lumières efface la section `shutters` à sa prochaine écriture de nom de lumière. Les noms des volets sont alors rétablis depuis le cloud à la synchronisation suivante, car le cloud arbitre. Avant un retour arrière, copiez `light-names.json`.

## Dépannage : erreur 503 `names_unavailable`

Quand le stockage est absent ou non inscriptible (montage manquant, droits, disque plein), la gateway :

- **lit** normalement, en renvoyant les noms d'origine (lumières et volets) ;
- **refuse l'écriture** d'un nom de lumière ou de volet avec une erreur 503 `{"error":"names_unavailable"}`.

À vérifier dans l'ordre :

1. la clé `light_names.path` est présente dans la configuration du backend ;
2. le répertoire `/opt/data/light-names` existe sur l'hôte et est monté dans le conteneur sur `/var/lib/essensys/names` ;
3. le répertoire est inscriptible par l'utilisateur du conteneur et le disque n'est pas plein ;
4. le conteneur a bien été recréé après l'ajout du montage.
