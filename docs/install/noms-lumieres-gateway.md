# Fichier des noms de lumières de la gateway

La gateway CM5 conserve les noms personnalisés des lumières (voir [Renommer une lumière](../utilisation/renommer-lumiere.md)) dans un fichier JSON unique, `light-names.json`.

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

`name` vaut `null` après une remise au nom d'origine. L'écriture est atomique (fichier temporaire puis renommage) : le fichier n'est jamais à moitié écrit.

## Sauvegarde

Le répertoire `/opt/data/light-names` est sous `/opt/data` : il est sauvegardé avec le reste des données de la gateway. Pour une sauvegarde manuelle, copiez le fichier `light-names.json` ; pour restaurer, remettez-le en place et relancez le backend. La gateway renvoie ensuite ses noms au cloud à la synchronisation suivante, et la modification la plus récente l'emporte.

## Dépannage : erreur 503 `names_unavailable`

Quand le stockage est absent ou non inscriptible (montage manquant, droits, disque plein), la gateway :

- **lit** normalement, en renvoyant les noms d'origine ;
- **refuse l'écriture** avec une erreur 503 `{"error":"names_unavailable"}`.

À vérifier dans l'ordre :

1. la clé `light_names.path` est présente dans la configuration du backend ;
2. le répertoire `/opt/data/light-names` existe sur l'hôte et est monté dans le conteneur sur `/var/lib/essensys/names` ;
3. le répertoire est inscriptible par l'utilisateur du conteneur et le disque n'est pas plein ;
4. le conteneur a bien été recréé après l'ajout du montage.
