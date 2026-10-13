# Ajouter ou remplacer un boîtier principal (BP)

Cette procédure s'applique quand on raccorde un **boîtier principal neuf** (BP, carte SC944D, firmware
`BP_MQX_ETH`) à une [gateway CM5](gateway-cm5.md) : remplacement après une panne, ou première mise en
service d'une armoire.

Elle remplace l'ancienne « Procédure de création de compte Essensys v3 ». Celle-ci renvoyait vers le site
ASP.NET `www.essensys.fr` qui délivrait la clé d'accès à distance, et ce site n'existe plus.

!!! warning "Sécurité"
    Toute intervention dans le coffret se fait **hors tension**, par une personne habilitée. Les contrôles
    de cette page sont en **lecture seule**. Ils ne pilotent pas l'armoire, sauf l'étape 6, qui consiste à
    envoyer une commande d'essai volontairement.

## Ce qui change avec la gateway CM5

### La clé d'accès à distance n'est plus nécessaire

Dans **Réglages → Accès à distance**, l'écran demande une clé de 32 chiffres. Avant la fermeture
d'Essensys, cette clé était obligatoire.

1. Le site générait une clé aléatoire pour chaque compte et en gardait l'empreinte MD5.
2. Le BP envoie, dans chaque requête, un en-tête `Authorization: Basic` calculé à partir de cette clé.
3. Si l'empreinte ne correspondait à aucune machine active, le serveur répondait **401**. Le BP s'arrêtait
   alors à sa première requête (`/api/serverinfos`) et ne demandait jamais ses actions. Le voyant
   **SERVEUR** restait rouge.

Avec la gateway CM5, ce contrôle n'existe plus :

- l'authentification du protocole legacy est désactivée (`auth.enabled: false`) ;
- toutes les actions passent par une **file unique** (`essensys:global:actions`), quelle que soit
  l'identité envoyée par le BP.

**Un BP sans clé fonctionne donc normalement avec le CM5.** Inutile de saisir une clé pour faire
fonctionner l'éclairage, les volets ou les scénarios.

??? info "Détails techniques de la clé"
    - **Stockage.** Les 32 chiffres sont rangés deux par octet aux index **922 à 937** de la
      [table d'échange](../architecture/exchange-table.md). Ces index sont en écriture seule : ni l'écran
      ni le serveur ne peuvent relire la clé. Les 8 groupes de tirets de l'écran sont un gabarit fixe et
      ne prouvent pas que la clé est absente.
    - **Persistance.** La clé est copiée dans l'EEPROM SPI du BP (adresses `0x00` à `0x0F`, la puce qui
      contient aussi l'adresse MAC). Elle reste donc **dans l'ancien BP** quand on le remplace.
    - **Prise en compte.** Une clé saisie est enregistrée et appliquée tout de suite, sans redémarrage :
      la boucle principale recalcule l'en-tête (`vd_UpdateCleServeurDansEEPROM`, puis `cryptage()`).
    - **Calcul.** Chaque demi-octet donne un caractère `'0' + n`. On calcule le MD5 des 32 caractères,
      puis on forme « 16 caractères hexa : 16 caractères hexa », encodés en base64. Sur un BP neuf,
      l'EEPROM est vierge (`0xFF`) : la chaîne hachée vaut alors 32 caractères `?`.
    - **Validité.** Le firmware ne teste jamais la clé. Elle sert seulement à l'en-tête d'authentification
      et au déchiffrement de l'ordre d'alarme distant chiffré (`_de67f`), que la gateway n'envoie pas.

    La clé redeviendrait nécessaire dans deux cas : si un serveur contrôlait de nouveau l'empreinte, ou
    si l'on implémentait l'armement distant de l'alarme chiffré. Il faudrait alors saisir la même clé sur
    l'écran et la conserver côté serveur.

### Ce qui reste dans l'ancien BP

Le BP neuf démarre avec la **configuration d'usine**. Ces éléments sont propres à chaque BP et ne
sont pas transférés :

| Élément | Où il est stocké | Conséquence |
|---|---|---|
| Paramètres « sauvegardés » (`RWS`) : plannings de chauffage, modes, scénarios, réveils, temps des lampes et des volets, modes des variateurs, configuration de l'alarme | Flash du BP | À ressaisir sur le BP neuf |
| Code utilisateur de l'alarme | EEPROM du BP | Revient au code par défaut : à changer |
| Clé d'accès à distance | EEPROM du BP | Facultative avec le CM5 (voir plus haut) |
| Adresse MAC | EEPROM du BP (usine) | Nouveau bail DHCP sur le segment armoire |

!!! tip "Relever l'ancienne configuration avant le remplacement"
    Si l'ancien BP fonctionne encore, relevez ses valeurs avant de le déposer, par exemple avec la page
    `/table_ref` de la gateway (voir l'étape 4).

    La synchronisation planifiée vers le cloud (`cloudsync`, profils « Scénarios », « Planning … »,
    « Temps volets ») **lit** l'armoire puis pousse les valeurs reçues vers le cloud. Une fois le BP neuf
    raccordé, elle pousse donc la configuration d'usine. Ne comptez pas sur elle pour restaurer
    l'ancienne configuration.

### La configuration des BA n'est pas renvoyée

Les boîtiers auxiliaires (BA : SC940D pièces de vie, SC942C chambres, SC941C pièces d'eau) gardent leur
propre configuration. Le BP neuf ne la leur renvoie pas au démarrage : il ne transmet un paramètre que
quand sa valeur change.

## Prérequis

- Une gateway CM5 installée selon le [guide Gateway CM5](gateway-cm5.md), avec le segment armoire sur
  `eth1` (DHCP et DNS par dnsmasq, `mon.essensys.fr` résolu vers la gateway).
- Un BP en firmware **099-37**, version de référence. Les versions 095-34 à 097-36 se comportent de la
  même façon pour tout ce qui est décrit ici.
- Un accès SSH à la gateway (utilisateur d'exploitation) et le câble Ethernet du BP raccordé au
  commutateur du segment armoire.

## Procédure

### 1. Poser et raccorder le BP

Coffret consigné : posez le BP, raccordez le bus I2C vers les BA, l'écran, l'alimentation et l'Ethernet
du segment armoire. Respectez les consignes du
[retour d'expérience foudre](../retex/foudre-2026/synthese.md) : Ethernet du BP isolé du PE, et aucun BA
non alimenté raccordé au bus. Remettez sous tension.

### 2. Vérifier le voyant réseau sur l'écran

Allez dans **Réglages → Accès à distance**. La ligne du bas affiche la chaîne
**CABLE › DHCP › DNS › SERVEUR** et l'adresse MAC du BP.

| Étape en rouge | Signification | Que vérifier |
|---|---|---|
| CABLE | Pas de lien Ethernet | Câble, port du commutateur |
| DHCP | Pas d'adresse | dnsmasq sur `eth1`, plage DHCP |
| DNS | `mon.essensys.fr` non résolu | Split-DNS dnsmasq (`gateway_armoire_hostname`) |
| SERVEUR | Pas de réponse valide de la gateway | Conteneurs `essensys-nginx` et `essensys-backend` |

**Tout en vert** signifie que le BP termine tout son dialogue avec la gateway : `serverinfos`,
`mystatus` (réponse 201) et `myactions` (réponse 200). Il n'y a rien d'autre à configurer sur l'écran.

### 3. Vérifier le bail DHCP et les échanges

Sur la gateway :

```bash
grep -i "<mac-du-bp>" /var/lib/misc/dnsmasq.leases
```

La ligne donne l'adresse attribuée au BP dans la plage du segment armoire (`10.0.1.100` à `10.0.1.200`
par défaut).

```bash
docker logs --since 5m essensys-backend 2>&1 | grep -c "Status Update"
```

On attend environ une mise à jour toutes les 2 secondes. La version du firmware apparaît dans ces lignes
(`Status Update (Version: V37, …)`).

### 4. Lire l'état des BA (index 12)

```bash
curl -s http://127.0.0.1:7070/table_ref
```

Cette page est une simple lecture : elle **ne vide pas** la file d'actions. Relevez :

- **index 12** (`Information`, défauts de communication) : bit `0x02` IHM, `0x04` BA PDV, `0x08` BA CHB,
  `0x10` BA PDE. On attend `(index 12 & 0x1C) = 0`, c'est-à-dire aucun BA en défaut ;
- **index 10** : le bit `0x04` signale le mode secouru.

Un BA en défaut n'exécutera aucune commande, même si la gateway la voit acquittée (voir l'étape 6).

### 5. Ressaisir la configuration

1. **Configuration du BP** : plannings, scénarios, temps des lampes et des volets, modes des variateurs,
   réveils, configuration de l'alarme. Utilisez l'écran ou l'interface web de la gateway.
2. **Code de l'alarme** : changez le code par défaut sur l'écran.
3. **Configuration des BA** : pour chaque paramètre (modes des variateurs, temps d'extinction, temps des
   volets), changez la valeur puis remettez-la, pour que le BP la retransmette au BA. Corrigez le mode
   des variateurs si le PIC d'un BA a été remplacé.

### 6. Essai de fonctionnement

Envoyez, depuis l'interface habituelle, **une commande vers chaque BA**, par exemple une lampe des
pièces de vie, une des chambres et une des pièces d'eau. Contrôlez ensuite les journaux :

```bash
docker logs --since 10m essensys-backend 2>&1 | grep -E "admin/inject|Sending Actions: .*\"actions\":\[\{|Action acknowledged"
```

!!! warning "Un acquittement ne prouve pas l'exécution"
    Le BP écrit l'ordre dans sa table d'échange, envoie `POST /api/done/{guid}`, et **seulement ensuite**
    transmet l'ordre au BA par l'I2C. Si le BA ne répond pas, l'ordre est abandonné sans message.
    « Action acknowledged » dans les journaux veut dire que le BP a reçu la commande, pas que la lampe
    s'est allumée. Le contrôle qui fait foi est l'effet constaté, avec l'index 12.

| Observation | Diagnostic |
|---|---|
| `admin/inject`, puis `Sending Actions` avec le GUID, puis `Action acknowledged`, et effet constaté | OK |
| Même séquence, **sans effet**, et index 12 avec le bit du BA visé | BA muet sur l'I2C : bus, alimentation ou carte BA. Voir [Remise en service après surtension](remise-en-service-surtension.md) |
| Pas de `admin/inject` après la commande | La commande n'atteint pas la gateway : session LAN, mode test de l'interface, URL utilisée |
| `Sending Actions` répété avec le même GUID, sans acquittement | Action refusée par le BP : le voyant SERVEUR devrait alors être rouge. Inspecter la file avec `docker exec essensys-redis redis-cli LRANGE essensys:global:actions 0 -1` |

## Dépannage

**« La gateway voit le BP, mais aucune action n'est exécutée. »**
Ce n'est pas la clé d'accès à distance si le voyant SERVEUR est vert. Suivez l'étape 6.

Commencez par une commande vers un BA que l'index 12 donne en bon état. Si elle fonctionne, le problème
vient des BA en défaut, pas du BP ni de la gateway. Pour les relancer ou les diagnostiquer, voir
[Remise en service après surtension](remise-en-service-surtension.md#relancer-les-ba-sans-ouvrir-le-coffret).

**L'écran affiche des tirets vides sur la page Accès à distance.**
C'est normal : la page n'affiche jamais la clé enregistrée.

**Faut-il saisir l'ancienne clé ?**
Non. Si vous l'avez gardée, la ressaisir redonne au BP neuf la même identité MD5 que l'ancien, ce qui
ne sert que si un serveur contrôle de nouveau cette identité. Une erreur de saisie passerait inaperçue,
puisque la clé ne peut pas être relue.

## Références

- [Table d'échange](../architecture/exchange-table.md) (index 10, 12, 590, 605 à 622, 922 à 937)
- [Client legacy](../architecture/legacy-client.md)
- [Gateway CM5](gateway-cm5.md)
- [Remise en service après surtension](remise-en-service-surtension.md)
- [Retour d'expérience foudre du 9 août 2026](../retex/foudre-2026/synthese.md)
- Sources : `client-essensys-legacy` (`Ethernet/Cryptage.c`, `Ethernet/www.c`, `C/EepromAdresseMac.c`,
  `H/TableEchangeDroits.h`) ; `essensys-server-backend` (`internal/middleware/auth.go`,
  `internal/data/redis_store.go`, `internal/api/handlers.go`)
