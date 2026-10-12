# Protection contre les surtensions

Règles d'installation du coffret domotique Essensys (BP SC944D et BA SC940D, SC941C, SC942C), issues du [retour d'expérience foudre 2026](../retex/foudre-2026/synthese.md). Elles complètent les guides d'installation de la passerelle et s'appliquent à toute installation neuve et à toute intervention sur le parc.

!!! warning "Règles PE et parafoudre à valider par un électricien"
    Les règles qui touchent au conducteur de protection (PE), à la terre et aux parafoudres sont des **recommandations** : elles doivent être validées par un électricien avant application, au regard de la NF C 15-100 et de l'installation concernée. Les travaux sur le tableau électrique relèvent de l'électricien, et ceux sur une installation photovoltaïque de l'installateur PV.

Chaque règle renvoie à l'exigence correspondante de la capacité **`aux-box-interconnect`** du change OpenSpec `i2c-surge-protection-2026-10-007` (dépôt `essensys-board-SC944D`).

## Principe

Le BP et chaque BA forment des îlots TBTS distincts, sans liaison au PE. Le câble de bus qui les relie sert de pont : lors d'un événement, un courant d'équilibrage le traverse et détruit les interfaces I2C. Les règles visent à **réduire l'impédance entre les 0 V des cartes**, à **ne jamais relier la TBT au PE**, et à **isoler tout port qui sort du coffret** vers un équipement relié au PE.

## Tableau électrique et environnement du coffret

| Règle | Exigence `aux-box-interconnect` |
|---|---|
| **Parafoudre de tête** présent et contrôlé (déconnecteur fermé, cartouche en état), alimenté en amont des différentiels 30 mA. Type 1 si le bâtiment a un paratonnerre ; type 2 au minimum si la NF C 15-100 l'impose (alimentation aérienne, densité de foudroiement). **Règle des 50 cm** : longueur totale des conducteurs de raccordement du parafoudre (phase/neutre + PE) ≤ 50 cm. | *Ports qui sortent du coffret* |
| **Valeur de terre** mesurée et notée dans le dossier de l'installation ; elle respecte la condition de la NF C 15-100 en régime TT pour le différentiel de tête (R × IΔn ≤ 50 V). Une seule terre : si une annexe a sa propre prise de terre, interconnecter les terres. Liaison équipotentielle principale vérifiée. | *Aucune liaison au PE et repérage du 0 V* |
| **Câbles photovoltaïques**, onduleur et batterie à **30-50 cm au moins** du coffret domotique ; jamais le long du coffret. | *Câblage du bus dans un coffret* |
| **Équipements reliés au PE** (onduleur, borne de recharge, équipement extérieur) : liaison réseau en Wi-Fi ou en fibre, **jamais en cuivre sur le commutateur du BP**. | *Isolement galvanique de l'Ethernet du BP* |
| **Ethernet du BP** isolé galvaniquement (fibre avec convertisseur alimenté depuis l'îlot TBTS du BP, ou isolateur ≥ 4 kV eff. 60 s). **Aucun parafoudre RJ45 relié au PE** sur le port du BP ; l'écran d'un câble blindé n'est pas raccordé côté BP. Le cordon sort directement du coffret, loin des nappes. | *Isolement galvanique de l'Ethernet du BP* |
| **Départs 230 V extérieurs** commutés par le BP ou un BA (terrasse, annexe, arrosage, pompe à chaleur extérieure) : parafoudre de **type 3** conforme NF EN 61643-11 (voyant, déconnecteur thermique), coordonné avec le parafoudre de tête, **au départ dans le tableau** ou côté charge — **jamais dans le coffret domotique**. | *Ports qui sortent du coffret* |
| **Jamais de varistance ni de parafoudre ajouté dans le coffret domotique**, en plus des composants d'origine des cartes. Une varistance nue n'est pas un parafoudre : en fin de vie elle passe en court-circuit avec risque d'incendie, et elle ferait entrer le courant de choc à quelques centimètres de la TBT. | *Ports qui sortent du coffret* |
| **Lignes TBT qui sortent du bâtiment** (capteurs pluie/vent, sirène extérieure) : isolées galvaniquement (≥ 4 kV eff. 60 s, interface à relais ou optocoupleur), ou protégées par un dispositif dont la fin de vie ne relie pas le 0 V au PE. Pas d'éclateur à gaz entre 0 V et terre. | *Ports qui sortent du coffret* |

## Dans le coffret domotique

| Règle | Exigence `aux-box-interconnect` |
|---|---|
| **Aucune borne ni aucun raccordement PE dans le coffret.** Un conducteur PE n'est jamais raccordé à un élément TBT. | *Aucune liaison au PE et repérage du 0 V* |
| **PE de passage** d'un départ 230 V qui traverse le coffret : gainé avec les conducteurs de son circuit, dans les goulottes 230 V, séparé de la TBT. | *Aucune liaison au PE et repérage du 0 V* |
| **Repérage du 0 V** : tout conducteur, tresse ou plan qui renforce le 0 V est isolé, **jamais vert-jaune ni bleu clair**, et porte à chaque extrémité le repère « 0 V TBTS – NE PAS RELIER À LA TERRE ». Un renfort de 0 V suit le câble de bus sur toute sa longueur, plaqué contre lui. | *Aucune liaison au PE et repérage du 0 V* |
| **TBT et 230 V jamais dans une même goulotte.** Le câble de bus et les nappes d'entrées sont tenus à distance des bornes de phase, sous manchon isolant là où ils les longent (les isolants d'un câble catégorie 5e ne sont pas prévus pour côtoyer le 230 V). | *Câblage du bus dans un coffret* |
| **Câble de bus** : câble souple, serti à l'outil, contacts Micro Mate-n-Lok complets ; **chaque liaison mesure au plus 0,5 m** ; SCL n'est pas torsadée avec le +15 V. Au-delà de 0,5 m, le BA est considéré comme déporté (voir ci-dessous). | *Câblage du bus dans un coffret* |
| **Liaison 0 V équipotentielle** entre BP et BA : carte **N2 « étoile 0 V »** (BP J31 et chaque BA en étoile autour d'un plan 0 V, avec cavalier, PTC et TVS par port), dépôt [essensys-i2c-etoile-0v](https://github.com/essensys-hub/essensys-i2c-etoile-0v). À défaut, renfort 0 V (N1) le long du câble de bus. Écart statique de 0 V entre J31-3 du BP et J1-3 de chaque BA ≤ 0,05 V à consommation maximale. | *0 V équipotentiels à basse impédance dans un coffret* |
| **Déconnexion d'un BA** : avec la carte N2, un cavalier par port ouvre SDA, SCL et +15 V d'un BA en une seule manœuvre, le 0 V restant relié ; avec le renfort N1, on retire le câble de bus du BA. | *Déconnexion individuelle d'un BA* |
| **+15 V des BA** : chaque BA est alimenté par une sortie protégée par son propre limiteur réarmable (PTC) suivi de son propre écrêteur (carte N2). | *Distribution protégée du +15 V* |

## BA déporté : module d'isolement (MIB)

Un BA est **déporté** s'il est installé hors du coffret du BP, ou si sa liaison de bus dépasse **0,5 m**. Il est alors raccordé par un **module d'isolement (MIB)** qui isole ensemble les données et l'alimentation (barrière renforcée ≥ 4 kV eff., ≥ 8 mm sur le module).

- Câble qualifié : **3 m au plus**, AWG20. Au-delà, tampon de bus qualifié sur banc, ou attente de la génération 3.
- Sur un bus qui porte un MIB, les écrêteurs de ligne du BP (D33/D34) sont remplacés par des modèles de 50 pF au plus, et aucun BA non isolé ne garde ses écrêteurs d'origine.

Exigence : *Module d'isolement pour BA déportés*.

## Règles BREAKING

!!! danger "À appliquer sur tout le parc"
    1. **Un BA non alimenté ne reste pas raccordé au bus.** Il se réalimente par ses lignes I2C et bloque tout le bus : son câble est retiré des deux côtés jusqu'à sa réparation. Exigence : *Déconnexion individuelle d'un BA*.
    2. **Un BA préparé pour un MIB n'est jamais raccordé directement au bus.** Ses écrêteurs de ligne sont déposés ; son connecteur côté isolé est d'une autre série que celui du bus, et son second connecteur de chaînage est neutralisé et étiqueté « ne pas raccorder sans module ». Exigence : *Module d'isolement pour BA déportés*.
    3. **Aucun build non qualifié n'est flashé** : BP uniquement en `.S19` 099-37, BA uniquement en `.hex` v1.7 de leur type (voir la [procédure de remise en service](remise-en-service-surtension.md#reparation-et-programmation)).

## Restrictions d'usage des cartes révision D

Les distances entre conducteurs 230 V et TBT des cartes révision D (notamment J1/J2 du BA face au relais K1 ou à la varistance VR1) ne sont **pas démontrées** : elles sont estimées à 2-3 mm, en dessous des 6 mm visés. En attendant le relevé sur les fichiers de fabrication (tâche 2.11 du change) :

- chaque BA passe l'**essai d'isolement à 500 V** et l'**inspection à la loupe** de la zone J1/J2 – K1 avant toute remise en service, en particulier le **SC941C**, qui dessert les pièces d'eau ;
- une carte retouchée dont la distance relevée est inférieure à 6 mm ne revient en service qu'avec une mesure compensatoire documentée (barrière isolante, vernis) ;
- les restrictions définitives issues du relevé seront ajoutées ici.

Exigence associée : *Câblage du bus dans un coffret* (câble de bus et nappes tenus à distance des bornes de phase).

## Mise en service : liste de contrôle

- [ ] Parafoudre de tête contrôlé, règle des 50 cm respectée, valeur de terre notée (électricien).
- [ ] Aucun équipement relié au PE en cuivre sur le commutateur du BP ; Ethernet du BP isolé.
- [ ] Aucune borne PE dans le coffret ; PE de passage gainé ; renforts 0 V isolés, colorés et repérés.
- [ ] Aucune goulotte mixte TBT / 230 V ; manchons posés le long des bornes de phase.
- [ ] Liaisons de bus ≤ 0,5 m ; carte N2 (ou N1) posée ; ΔVg ≤ 0,05 V.
- [ ] Câbles PV à 30-50 cm au moins du coffret.
- [ ] Départs 230 V extérieurs protégés hors du coffret ; aucune varistance ajoutée dans le coffret.
- [ ] BA déporté : MIB en place, câble ≤ 3 m AWG20.
- [ ] Photos de l'installation archivées avec le ticket.
