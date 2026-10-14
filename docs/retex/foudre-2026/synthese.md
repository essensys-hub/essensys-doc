---
title: "Foudre du 9 août 2026 : synthèse"
description: "Ce qu'il faut retenir d'un coup de foudre rapporté sur une installation Essensys avec photovoltaïque : les faits, le mécanisme calculé, les questions ouvertes et nos recommandations."
---

# Coup de foudre du 9 août 2026 : ce qu'il faut retenir

!!! abstract "En bref"
    - **Les faits** : depuis un coup de foudre rapporté le 9 août 2026, le boîtier principal n'obtient plus de réponse de ses trois boîtiers auxiliaires.
    - **Le mécanisme calculé** : le câble entre les cartes aurait servi de pont au courant, jusqu'à des composants peu protégés. Un simple blocage, sans dégât, n'est pas exclu ; l'origine et le chemin du courant restent à confirmer.
    - **Mise à jour du 14 octobre** : avec un boîtier principal neuf, le boîtier auxiliaire remplacé répond, les deux autres non. Le câble est sain ; la panne est propre à ces deux cartes.
    - **Peu fréquent, pas impossible** : environ neuf ans sans incident ici, sans statistique ; une fois un chemin ouvert, 11 à 20 ampères suffisent à atteindre les fils de données *(calculé)*.

**Statut (14 octobre 2026)** : le boîtier principal et un boîtier auxiliaire ont été remplacés, et le code des cartes a été analysé. Les mesures sur les deux autres boîtiers restent à faire ([où en est-on ?](#suivi)). *Constaté* : vu sur place, sur photo, sur les schémas ou dans le code ; *calculé* : à confirmer par une mesure ; *hypothèse* : piste à vérifier.

??? info "Vocabulaire"
    - **BP, BA** : boîtier principal, boîtiers auxiliaires (les BA commandent les pièces).
    - **Bus** : câble à quatre fils reliant le BP aux BA.
    - **Microcontrôleur** : le petit processeur de chaque carte.
    - **0 V** : le « zéro » électrique d'une carte, isolé de la terre.
    - **Parafoudre** : il dérive les surtensions vers la terre ; celui de tête est au tableau principal.

## Ce qui s'est passé { #recit }

Les quatre cartes, dans un même coffret, sont reliées en chaîne par trois câbles d'environ 33 cm. Le coffret de protection photovoltaïque est tout proche, et la supervision de l'onduleur partage le switch réseau du BP *(constaté)*.

Le 9 août vers 16 h 20, la supervision photovoltaïque tombe à 0 W *(constaté)*. L'occupant rapporte un orage, un coup de foudre et le déclenchement du disjoncteur de branchement. Cet arrêt est attendu : l'onduleur s'arrête sans réseau.

Depuis, le BP n'obtient plus de réponse des trois BA *(constaté)*, mais semble fonctionner : voyant allumé, lien réseau actif *(constaté sur photo)*. Le parafoudre photovoltaïque côté courant alternatif a ses fenêtres noires (sens à confirmer avec la notice), depuis une date inconnue *(constaté)*.

<div class="grid" markdown>

<figure markdown="span">
  ![Coffret électrique ouvert contenant quatre cartes blanches empilées. Les trois cartes du haut portent des rangées de relais verts et des borniers aux fils colorés. La carte du bas a une prise réseau avec un cordon orange. Un mètre pliant noir est posé en travers et le long de la porte.](img/coffret-domotique.jpg){ width="340" loading=lazy }
  <figcaption>Le coffret domotique ouvert : les trois BA en haut, le BP en bas avec son cordon réseau orange. À ne pas reproduire : on n'introduit rien dans un coffret ouvert sous tension.</figcaption>
</figure>

<figure markdown="span">
  ![Vue d'ensemble d'un local technique : deux tableaux électriques à étiquettes floutées à gauche, une grande armoire blanche fermée marquée essensys au centre, et à droite un petit coffret de protection photovoltaïque à sections « courant continu » et « courant alternatif », devant un mur bleu.](img/implantation-coffrets.jpg){ width="340" loading=lazy }
  <figcaption>Les tableaux électriques à gauche, le coffret domotique au centre, le coffret de protection photovoltaïque à droite, à quelques centimètres. Étiquettes floutées, plaques et logos masqués.</figcaption>
</figure>

</div>

## L'analyse { #analyse }

### 1. Le bus fait office de pont { #pont }

Chaque carte est un îlot relié à la maison par ses propres câbles ; seul le bus relie les îlots entre eux *(constaté)*. Si un choc extérieur fait monter le niveau électrique d'un îlot, un courant d'équilibrage traverse le bus. Au-delà de 6 à 8 V d'écart, il emprunte aussi les fils de données *(calculé)*.

<figure markdown="span">
  ![Deux scènes. Au calme, quatre cartes (BP SC944D, BA SC942C, SC941C, SC940D) sont au même niveau, reliées par des arches violettes (le câble du bus) et par des câbles qui descendent vers la maison. Pendant le choc, les cartes sont nommées îlots A à D : l'îlot A, à gauche, pris pour exemple, est surélevé et frappé par un éclair arrivant par ses câbles. Des flèches rouges traversent les ponts puis ressortent par les câbles des autres îlots. Un zoom montre les 4 fils du bus : 0 V, SDA, SCL (en pointillés rouges au-delà du seuil) et +15 V.](schemas/iles-et-pont.svg){ loading=lazy }
  <figcaption>Quatre îlots reliés par un pont. L'îlot touché est un exemple : on ne sait pas encore laquelle des quatre cartes l'a été.</figcaption>
</figure>

### 2. Le microcontrôleur encaisse avant la protection { #maillon-faible }

Sur les BA, le microcontrôleur absorbe le courant dès 5,5 V, avant la diode qui protège les fils de données (6,4 V), et aucune résistance ne le limite (0 Ω, *constaté*) : il peut recevoir 50 à 100 fois ce qu'il supporte *(calculé)*. Avec 47 Ω, la diode prendrait l'essentiel du choc : le microcontrôleur survivrait probablement, sans garantie.

<figure markdown="span">
  ![À gauche, une échelle de tension dilatée : 0 à 5 V en fonctionnement normal, la diode interne du microcontrôleur qui conduit dès 5,5 V, la TVS dès 6,4 V. À droite, deux circuits simplifiés : câble, TVS vers la masse, R1, puis le microcontrôleur PIC16F946 et sa diode interne vers +5 V. Aujourd'hui (R1 = 0 Ω), une grosse flèche rouge entre dans le microcontrôleur : 1 à 2 A, 50 à 100 fois son maximum. Avec 47 Ω, la grosse flèche part dans la TVS et un filet de ≈ 20 à 140 mA va vers le microcontrôleur.](schemas/maillon-faible.svg){ loading=lazy }
  <figcaption>Qui encaisse le choc ? Aujourd'hui, le microcontrôleur. Avec 47 Ω, la diode de protection.</figcaption>
</figure>

### 3. Une seule ligne bloquée fait taire les trois BA { #bus-bloque }

Les trois BA partagent les mêmes fils de données *(constaté)* : une seule ligne bloquée les rend tous muets *(calculé)*. Causes possibles : un composant endommagé, un BA privé d'alimentation, ou un simple verrouillage, que les BA ne lèvent pas seuls *(constaté dans le code)*. Muets ne veut pas dire détruits.

Premier test, gratuit, après le contrôle de sécurité de l'électricien : un cycle complet d'alimentation des BA. S'ils répondent, la panne n'était qu'un blocage.

## Où en est-on ? { #suivi }

*Mise à jour du 14 octobre 2026.*

- **Deux cartes neuves** *(constaté)*. Le boîtier principal (BP) et le BA des pièces de vie, placé en bout de chaîne, ont été remplacés. C'est le premier BP posé depuis la fermeture de la société Essensys. Il dialogue avec une passerelle locale qui remplace l'ancien serveur.
- **Le BA neuf répond, les deux anciens non** *(constaté)*. L'éclairage de l'entrée fonctionne. Les BA des chambres et des pièces d'eau restent muets.
- **Le câble est sain** *(déduit)*. Le BA neuf est au bout de la chaîne : ses signaux et son alimentation traversent les deux autres BA. La panne est donc propre à ces deux cartes, et non au bus.
- **Ce n'est pas un problème d'appairage** *(constaté dans le code)*. Les cartes ne se « reconnaissent » pas : le BP appelle chaque BA à une adresse fixe, et un BA répond dès qu'il est alimenté et en état de marche. La clé d'accès à distance, vide sur un BP neuf, n'y est pour rien.
- **Un ordre « reçu » n'est pas un ordre exécuté** *(constaté dans le code)*. Le BP confirme l'ordre à la passerelle avant de l'envoyer aux BA. L'application peut donc afficher une commande comme passée alors que rien ne s'est allumé.
- **Deux causes restent possibles** *(hypothèse)* :
  - le plus probable, les deux anciens BA ont été abîmés par le même courant que la carte remplacée ;
  - moins probable, ils utilisent une très ancienne version de leur programme, incompatible avec celle du BP.
- **Prochaines vérifications** :
  - la petite LED de chaque BA : éteinte, figée ou clignotante ;
  - le code d'erreur lu sur la console de diagnostic du BP ;
  - l'[espion I2C passif](../../debug/espion-i2c.md), en cours de fabrication, qui écoute le bus sans y toucher ;
  - l'essai d'isolement des deux cartes, avant toute remise en service.

Le détail est dans l'[analyse experte](analyse-experte.md#suivi).

## À confirmer { #a-confirmer }

Si les historiques ont expiré, l'origine pourrait rester incertaine.

| Question | Aujourd'hui | Pour trancher |
|---|---|---|
| **L'origine** | Hypothèses non classées : réseau électrique ; photovoltaïque puis Ethernet (suppose une étincelle à travers les isolants des ports, sinon 0,3 à 1,7 A seulement, *calculé*) ; surtension temporaire, ou défaut de l'onduleur ou du parafoudre photovoltaïque ; événements indépendants | Journaux de l'onduleur, du switch et de la supervision |
| **Le chemin** | Isolant franchi ou boucle refermée : non identifié | Essais d'isolement, traces sur les ports Ethernet |
| **La carte en cause** | Le BA neuf en bout de chaîne répond : le bus est sain. Les BA des chambres et des pièces d'eau restent muets *(constaté, 14 octobre)* | LED de chaque BA, console de diagnostic du BP, espion I2C, mesures à l'établi |
| **L'isolement des BA** | 230 V à environ 2 à 3 mm de la très basse tension (estimation sur plan) : conformité à vérifier | Essai d'isolement de chaque carte, fichiers de fabrication |

<figure markdown="span">
  ![Plan simplifié d'une maison. À gauche, l'arrivée du réseau électrique, puis le tableau avec son parafoudre de type 2 (voyant vert). Au centre, le coffret domotique avec ses quatre cartes reliées par le bus. À droite, les panneaux, l'onduleur hybride et le coffret PV, dont le parafoudre AC est au noir. En bas, le dongle de supervision (ne répond plus) et le switch réseau, relié au port Ethernet du BP. Quatre pastilles ambre numérotées marquent les portes. Quatre fiches détaillent les arguments pour et contre, et ce qu'il faut vérifier. En pied de figure : constaté, la supervision du PV à 0 W, le déclenchement du disjoncteur étant rapporté par l'occupant ; autres pistes également ouvertes, surtension temporaire, défaut de l'onduleur ou du parafoudre AC, indices sans lien.](schemas/portes-d-entree.svg){ loading=lazy }
  <figcaption>Les portes d'entrée possibles vers les cartes. Ce sont des hypothèses à départager : aucune n'est établie.</figcaption>
</figure>

## Ce que nous faisons { #actions }

### Court terme, sur ce site { #court-terme }

- **Sécurité et diagnostic** par un électricien : une carte mal isolée n'est pas remise en service.
- **Cartes renforcées** : résistances de 47 Ω et alimentation des BA protégée.
- **Bus en étoile** (cartes reliées à un point central par des câbles courts, au lieu de la chaîne) : il faut 4 à 6 fois plus de courant pour atteindre les fils de données *(calculé)*.

<figure markdown="span">
  ![Graphique en barres horizontales sur un axe de 0 à 200 A. « Aujourd'hui » : 11 A pour un choc raide et 20 A pour l'onde 8/20. « Avec l'étoile 0 V » : 50 à 65 A et 80 à 120 A. Une pastille verte indique « 4 à 6 fois plus de marge ». Les notes expliquent pourquoi l'événement est peu fréquent (il faut un chemin, pas encore identifié sur le site ; environ 9 ans sans incident, aucune statistique) et pourquoi il n'est pas impossible (un coup de foudre se compte en milliers d'ampères ; un parafoudre de type 2 de tableau est prévu pour 5 000 A nominaux).](schemas/rare-mais-pas-impossible.svg){ loading=lazy }
  <figcaption>Le courant entre les cartes au-delà duquel le choc atteint les fils de données : 11 à 20 A aujourd'hui, 50 à 120 A avec le bus en étoile (« étoile 0 V » sur le schéma). Valeurs calculées, à confirmer au banc.</figcaption>
</figure>

### Long terme, pour toutes les installations { #long-terme }

- **Carte d'interconnexion** : cartes au même niveau électrique, câbles sortant du coffret protégés ou isolés.
- **Module d'isolement** pour un BA dans un autre coffret ou bâtiment.
- **Logiciel** : déblocage automatique du bus, alerte quand un BA se tait.
- **Essais sur banc** pour mesurer les seuils calculés.

## Recommandations pour toute installation { #recommandations }

- **Parafoudre de tête contrôlé** : au-delà du voyant vert, l'électricien vérifie la partie neutre-terre, sans voyant, et la terre.
- **Câbles photovoltaïques éloignés du coffret domotique** : 30 à 50 cm au moins, ou goulotte métallique reliée à la terre aux deux bouts.
- **Ethernet du BP isolé** (fibre optique ou isolateur), jamais de parafoudre relié à la terre. L'onduleur et les équipements extérieurs reliés à la terre rejoignent le switch du BP en Wi-Fi ou en fibre, jamais en cuivre.
- **Très basse tension et 230 V séparés** : bus et fils des boutons jamais dans une goulotte 230 V, ni près des bornes de phase. Le 0 V des cartes n'est jamais relié à la terre : on perdrait la très basse tension de sécurité exigée près des baignoires et des douches.
- **Après un orage** : ne touchez ni aux cartes ni au bus, qui peuvent être au potentiel du 230 V. Couper le disjoncteur ne suffit pas toujours (batterie du BP, sortie de secours de l'onduleur) : la mise hors tension revient à une personne habilitée. Côté photovoltaïque, seul l'installateur intervient : les panneaux restent sous tension le jour.
- **Conserver les traces** : photos des coffrets et des voyants, heure de l'orage, journaux et captures (vite effacés), modules déposés.

## Pour aller plus loin { #aller-plus-loin }

L'[analyse experte](analyse-experte.md) détaille les calculs, les [hypothèses](analyse-experte.md#hypotheses), le [diagnostic](analyse-experte.md#diagnostic) et les [protections](analyse-experte.md#court-terme).
