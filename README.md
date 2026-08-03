# McGill — Éditeur de trajectoires d'aéronefs

Application de bureau (PySide6) permettant de concevoir visuellement des scénarios de trafic aérien sur un aéroport donné : tracé de trajectoires, définition de conflits (intersections, poursuite/lead-follow) et export au format XML pour être rejoués ou utilisés dans une simulation.

## Fonctionnalités

- **Chargement d'un aéroport réel** à partir de son code OACI (ICAO), lu depuis un fichier `apt.dat` (format X-Plane) : pistes, nœuds et segments de taxiways.
- **Visualisation interactive de la carte** de l'aéroport (zoom à la molette, déplacement au clic-glisser).
- **Création d'aéronefs et de trajectoires** : ajout de points de passage (waypoints) au clic droit, gestion de la vitesse par segment.
- **Définition de conflits entre aéronefs** :
  - *Intersection* : point de croisement avec un décalage temporel/spatial (offset).
  - *Lead-follow* : un aéronef en suit un autre avec un ralentissement sur une portion du trajet.
- **Sauvegarde / chargement de scénarios** au format XML :
  - `Save` écrase le fichier courant.
  - `Save as` permet d'enregistrer sous un nouveau nom.
  - `Load file` recharge un scénario existant.
- **Confirmation à la fermeture** : une boîte de dialogue propose de sauvegarder (écraser ou enregistrer sous), d'ignorer les modifications, ou d'annuler la fermeture.

## Structure du projet

```
McGill/
├── main.py                # Point d'entrée : demande le code OACI, lance l'interface
├── Interface.py            # Fenêtre principale (liste des aéronefs, boutons save/load)
├── Map.py                  # Widget de carte : rendu, interactions souris, lecture XML
├── WriteXML.py              # Écriture des scénarios au format XML
├── Aircraft.py              # Modèle de données d'un aéronef (trajectoire, conflits, follow)
├── AircraftItem.py          # Carte UI représentant un aéronef dans la liste
├── Airport.py               # Lecture du fichier apt.dat et modélisation de l'aéroport
├── CoordConverter.py        # Conversions entre coordonnées géo / UTM / écran
├── Runway.py                 # Modèle de piste
├── TaxiwayNode.py            # Modèle de nœud de taxiway
├── TaxiwaySegment.py         # Modèle de segment de taxiway
├── ScenarioDialog.py         # (optionnel) Boîte de dialogue de choix de scénario prédéfini
├── apt.dat                   # Base de données d'aéroports (format X-Plane)
├── scenarios/                # Exemples de scénarios XML prêts à charger
└── images/                   # Icônes utilisées pour l'affichage (positions AI / utilisateur)
```

## Prérequis

- Python 3.8+
- Dépendances Python :
  - [`PySide6`](https://pypi.org/project/PySide6/)
  - [`geopy`](https://pypi.org/project/geopy/)
  - [`utm`](https://pypi.org/project/utm/)

Installation :

```bash
pip install PySide6 geopy utm
```

## Utilisation

1. Lancer l'application :

   ```bash
   python main.py
   ```

2. Entrer le **code OACI** de l'aéroport souhaité (par exemple `CYUL` pour Montréal-Trudeau) lorsque l'invite s'affiche dans le terminal. L'aéroport doit être présent dans `apt.dat`.

3. Dans l'interface :
   - Cliquer sur **`+`** pour créer un nouvel aéronef, puis **clic droit** sur la carte pour ajouter des points de trajectoire.
   - Cliquer sur **`OK`** pour terminer la trajectoire en cours.
   - Utiliser les boutons **`Intersection`** et **`Follow`** sur une carte d'aéronef pour définir des conflits.
   - **`Save`** / **`Save as`** pour exporter le scénario en XML, **`Load file`** pour en recharger un.

## Format des fichiers XML générés

Chaque scénario est structuré ainsi :

```xml
<aircraft>
  <ac id="1">
    <waypoints>
      <waypoint lat="..." lon="..." speed="..."/>
      ...
    </waypoints>
    <conflict type="intersection">
      <location lat="..." lon="..."/>
      <offset dist="..."/>
    </conflict>
    <conflict type="lead-follow">
      <location lat="..." lon="..."/>
      <offset dist="..."/>
      <slow-down dist="..." reduc="..."/>
      <end-position lat="..." lon="..."/>
    </conflict>
  </ac>
  ...
</aircraft>
```

## Licence

Distribué sous licence MIT — voir le fichier [LICENSE](LICENSE).
