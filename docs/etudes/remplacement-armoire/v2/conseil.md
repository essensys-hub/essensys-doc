---
title: "Conseil d'autocritique du 21 octobre 2026"
description: "Verdict du conseil d'autocritique sur les trois études V1 de remplacement de l'armoire ESSENSYS, face à l'exigence de résilience née de la foudre : accords, désaccords, angles morts et recommandation."
---

# Conseil d'autocritique du 21 octobre 2026

Après la foudre du 9 août 2026, une question nouvelle a été posée aux trois études V1 : l'armoire peut-elle rester utilisable si son électronique meurt ? Un conseil d'autocritique a jugé les études sur ce critère et recommandé l'architecture V2 « filaire d'abord, domotique en dérivation ».

## La question

1. **Décision** : quelle architecture retenir pour la V2 de l'armoire ESSENSYS, et que faire de chacune des trois études V1 (Revolution Pi, environ 5 450 € HT ; quatre Arduino Opta, environ 5 600 € HT ; refonte Raspberry Pi et Ethernet, environ 3 160 € HT) ?
2. **Exigence nouvelle** : si le contrôleur meurt ou grille, les 63 boutons muraux doivent continuer à piloter les relais en filaire ; la domotique devient une couche ajoutée.
3. **Contexte** : un BP SC944D et trois BA (PIC16F946) sur un bus I2C non isolé ; 25 éclairages, 15 volets et store, 8 variateurs, fil pilote, alarme, délestage par la TIC. Depuis la foudre, deux BA sur trois sont muets. Dans les trois études V1, chaque bouton passe par un calculateur, sauf les 8 variateurs Eltako. Une seule personne fait l'électronique et le logiciel, à temps partiel, et un électricien pose et valide.
4. **Enjeu** : une maison dont les lumières et les volets restent utilisables quoi qu'il arrive à l'électronique, pour un coût, une place et une charge de travail supportables.

## La méthode

!!! note "Un conseil d'agents d'IA"
    Les six conseillers sont des agents d'IA (Claude), chacun dans un rôle d'expert. Ils ont travaillé séparément sur le même dossier, avec recherche web, puis chacun a critiqué les cinq autres avis, rendus anonymes. Un président de séance a fait la synthèse ci-dessous. Leurs chiffres et leurs références sont des estimations argumentées, pas des devis : un électricien, les fabricants et des essais doivent les confirmer.

| Rôle | Regard |
| --- | --- |
| Électricien tableautier | Pose, normes, place au mur, temps de chantier |
| Automaticien | Logique de commande, priorités, repli des sorties |
| Sûreté de fonctionnement | Modes de panne, causes communes, AMDEC |
| Spécialiste foudre et CEM | Chemins de l'onde, barrières, parafoudres |
| Mainteneur seul | Charge de travail d'une personne, coût sur dix ans, rechanges |
| Avocat du diable | Hypothèses fragiles, solutions écartées trop vite |

## Le verdict

### Où le conseil s'accorde

1. Aucune étude V1 ne tient l'exigence V2. Toutes mettent un calculateur entre le bouton et le relais, sauf les 8 variateurs. Une Revolution Pi morte prive 55 boutons sur 63. L'Opta et la refonte Raspberry Pi gardent la panne d'aujourd'hui : un cerveau mort, une zone morte.
2. Le relais monostable ne retient rien, donc un logiciel doit tenir l'état. Il faut un organe bistable que le bouton commande seul.
3. Le découpage par zone n'arrête pas les causes communes : même code, même bloc 24 V, même foudre.
4. Il faut une source de commande par zone, séparée de celle de la domotique.
5. La domotique se branche en parallèle et ne bloque jamais un bouton. Le contrôleur devient secondaire.
6. Fil pilote sans signal, radiateurs en confort : le repli est bon.
7. On garde des V1 le répartiteur, les blocs de phase, les jonctions IDC et le plan de bornage.
8. On migre zone par zone, sans logiciel.

### Où le conseil s'oppose

**Télérupteur électromécanique ou électronique.** L'Électricien, la Sûreté et le Spécialiste foudre veulent des télérupteurs à levier : état gardé sans tension, manœuvre à la main, pas de semi-conducteur face à l'onde. L'Automaticien et l'Avocat du diable préfèrent des Eltako : 0,11 mA par entrée contre 230 mA par bobine, 18 mm par circuit, entrées centrales pour la domotique. Rien de ce qui les départage n'est mesuré : courant admis par les lignes murales et les jonctions IDC (1 A), place au mur, tenue aux chocs.

**Volets.** L'Électricien et l'Automaticien veulent deux relais en chaîne de priorité. Le premier accepte la commande maintenue ; le second ajoute un module électronique EGS12Z pour l'appui court. Le montage « marche + sens » de la Sûreté peut renvoyer un instant le moteur en montée au relâchement.

**Source de commande.** Cinq conseillers prennent un 24 V continu de classe II, le Spécialiste foudre un transformateur 50 Hz, sans électronique. Or le 24 V alternatif est interdit en volumes 1 et 2, et en 12 V alternatif une bobine tire environ 0,54 A.

**Réparer les BA d'abord.** L'Avocat du diable le veut : quelques euros de pièces, et un retour arrière. Les quatre autres refusent de réinvestir dans le bus I2C, sans vérifier que les zones sont mortes.

**Contrôleur.** Trois conseillers retiennent la Revolution Pi. Le Mainteneur la juge surdimensionnée et propose un serveur d'E/S léger, piloté par la passerelle.

**Vitesse contre couverture.** Le Mainteneur veut poser dès novembre, la Sûreté et le Spécialiste foudre après des essais, qui décalent le plan sans le changer.

### Les angles morts révélés par la critique croisée

- **Le délestage** (critiques 1, 4 et 5). Contrôleur mort, radiateurs en confort, rien ne déleste. Un soir de grand froid, le disjoncteur de branchement saute et toute la maison s'éteint, filaire compris. Cinq rapports le notent sans le retenir.
- **L'assurance** (critiques 2 à 6). Aucun avis ne parle de l'expertise d'assurance, ni de garder intacts les BA muets pour elle. Un certificat de foudroiement aiderait à trancher l'origine, toujours ouverte.
- **La foudre, oubliée par le Mainteneur** (six critiques sur six). Il fait poser des Eltako en pièces d'eau sans attestation d'isolement ni essai de choc.
- **Le coffret photovoltaïque** (critiques 3 à 6). Le retex le place à quelques centimètres à droite, là où les trois études ajoutent leurs coffrets.
- **La prémisse des zones mortes** (critiques 5 et 6). Dans l'armoire, le retex n'établit qu'une diode détruite et aucune mesure sur les deux BA. Muet sur le bus ne veut pas dire sans boutons.
- **Les failles des solutions.** Un contact de domotique soudé bloque le télérupteur. Chez l'Automaticien, perdre le 24 V d'une zone éteint ses lumières. Sans attestation d'Eltako, 63 relais de couplage, environ 1 200 €, effacent l'avantage de prix de l'Avocat.
- **Le contrôleur faux ou piraté** (critique 3). Un ordre arrêt au fil pilote, en janvier, coupe le chauffage.

### La recommandation

Retenir l'armoire « filaire d'abord, domotique en dérivation » de l'Électricien, avec les règles d'insertion de l'Automaticien et les frontières du Spécialiste foudre. On renonce à la parité avec le BP, double clic et appui long compris.

**Le principe**
- **Éclairages.** Un télérupteur électromécanique à levier par circuit, dont le poussoir attaque la bobine 24 V continu. Fiche Finder série 20 vérifiée : 4 kV entre bobine et contacts, impulsion jusqu'à 1 h, isolation renforcée non déclarée. Sans attestation, un relais 38.51 commande un télérupteur à bobine 230 V : environ 1 000 € et 0,3 m de plus (Électricien).
- **Volets et store.** Deux relais en chaîne, la montée ou la rentrée prioritaire. Commande maintenue sans contrôleur, appui court avec. Un automatisme vent autonome rentre le store.
- **Variateurs.** Les EUD12D, entrée locale sur la source de zone, réglés en PRI 1 ou 5. Sans attestation d'Eltako, un relais de couplage chacun, environ 150 € en tout.
- **Fil pilote.** Relais au repos, donc confort, et un commutateur Auto, Confort, Hors-gel par zone. Aucun ordre arrêt depuis la domotique.
- **Cumulus.** Contacteur jour/nuit manuel sur le contact heures creuses du Linky, si l'abonnement en a. Autres sorties : relais au repos, repli voulu.
- **Alarme.** Reste dans la domotique, sur batterie : essai de capacité annuel, remplacement vers 4 ans (Sûreté).
- **Commande.** Un 24 V continu de classe II par zone (EN 61558-2-16), trois disjoncteurs, fusible de 1 A, une rechange. Ordres groupés séquencés : 25 bobines ensemble tirent 5,75 A.
- **Domotique.** Un îlot à part, dont le 0 V ne touche ni le filaire ni le PE. Contacts secs en parallèle des boutons, jamais sur une entrée prioritaire. Leur commun passe par un relais de garde à chien de garde matériel et une borne sectionnable par zone. État lu à travers 4 kV au moins, jamais réimposé.
- **Délestage.** Bilan de puissance. S'il dépasse l'abonnement, un délesteur autonome dans le filaire, environ 250 € (Mainteneur).
- **Foudre, avant mai 2027.** Parafoudre de tête contrôlé, type 1+2 si l'analyse de risque le demande. Rien dans les coffrets. Parafoudre côté charge sur les départs extérieurs, barrière isolée sur les lignes extérieures, coffrets à 30 à 50 cm des câbles photovoltaïques.
- **Réception.** Contrôleur coupé, réseau débranché, une sortie collée, les 63 boutons commandent leur charge. Isolement mesuré chaque année et après chaque orage proche.
- **Ordre.** Chambres et pièces d'eau sans réparer leurs BA, puis pièces de vie, puis domotique.

**Les trois études**
- **Revolution Pi : transformer.** La Connect 5 reste candidate pour la couche, achetée en dernier, et ses 38.51 servent au couplage. Abandonner les boutons sur les DIO.
- **Arduino Opta : abandonner.** Le zonage n'arrête pas les causes communes, et ses entrées non isolées reprennent la topologie du 9 août. Garder le fusible par zone.
- **Raspberry Pi et Ethernet : abandonner les cartes** à relais soudés et à 230 V. Garder l'isolement des entrées, le monostable devenu relais de garde, le battement de cœur.

**Ordres de grandeur**
- **Matériel.** 3 600 à 5 100 € HT selon la couche domotique, dans la fourchette des V1 (Mainteneur). Environ 1 000 € de plus sans attestation.
- **Électricien.** 6 à 8,5 jours, 2 400 à 3 400 € HT, sans devis (Mainteneur). Chambres et pièces d'eau : environ 2 000 € HT et 3 à 4 jours (Électricien).
- **Place.** 1,6 à 2,1 m de rail, donc un second coffret (Électricien).
- **Logiciel.** Aucun sur le chemin du bouton, puis 5 à 11 semaines-personne de domotique (Mainteneur), contre 11 à 28 avant la bascule en V1.

**Les préalables qui peuvent tout changer**
- **La place.** Sans second coffret possible loin du coffret photovoltaïque, passer aux Eltako, environ 0,9 m de rail (Avocat), si Eltako atteste l'isolement de ses entrées.
- **Le courant.** Si les lignes murales ne tiennent pas 230 mA, le poussoir commande un 38.51.
- **L'essai de choc.** Au banc, 2 puis 4 kV sur une ligne de bouton, avant de commander en série : 1 000 à 1 800 € en laboratoire (retex).
- **L'état des BA.** Appuyer sur un bouton de chambre, filmer dix secondes la LED DL1. Si les boutons marchent, rien ne presse.
- **L'assurance.** Garder intacts les BA déposés, tant qu'une expertise est possible.

### La première chose à faire

Faire venir l'électricien une journée pour le relevé, avant toute commande : volumes des salles d'eau, résistance et isolement de chaque ligne de bouton, place autour du coffret photovoltaïque, bilan de puissance, parafoudre de tête et terre. Ce relevé tranche la place, le courant et la tension de commande.

## La suite

- L'architecture retenue : [étude V2 « filaire d'abord, domotique en dérivation »](filaire-d-abord.md).
- Ce que chaque étude V1 change, garde ou abandonne : [autocritique des études V1](autocritique-v1.md).
- La réponse à l'exigence, en une page : [Répondre à l'exigence de résilience](../../resilience.md).
