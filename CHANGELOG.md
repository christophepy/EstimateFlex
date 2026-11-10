# Changelog

Toutes les modifications notables du projet EstimateFlex seront documentées dans ce fichier.

Le format est inspiré de Keep a Changelog :
https://keepachangelog.com/fr/1.1.0/

---

# [1.0.0] - 2026-11-10

Première version publique stable d'EstimateFlex.

## Fonctionnalités

### Projets

- Création de projets.
- Modification de projets.
- Suppression de projets.
- Contrôle de l'unicité des noms de projets.
- Gestion des informations client associées aux estimations.

### Profils

- Gestion des profils de productivité :
  - Junior
  - Senior
  - Expert
- Personnalisation des paramètres d'estimation.
- Sauvegarde et chargement des profils utilisateur.

### Scénarios

- Création de scénarios d'estimation.
- Gestion des scénarios Optimiste, Réaliste et Pessimiste.
- Association des scénarios aux estimations.

### Estimations

- Calcul des charges.
- Calcul des durées.
- Calcul des coûts.
- Prise en compte des paramètres du projet.
- Application des coefficients de complexité.
- Utilisation des profils de productivité.

### Rapports

- Historisation des estimations.
- Consultation détaillée des résultats.
- Renommage des rapports.
- Suppression des rapports.
- Classement des meilleures estimations.

### Export

- Export PDF des estimations.
- Export Excel des estimations.
- Génération automatique des rapports de synthèse.

## Technique

- Architecture modulaire Python.
- Interface graphique PyQt6 multi-onglets.
- Modèles de données basés sur les dataclasses.
- Couche Repository pour l'accès aux données.
- Persistance des données au format JSON.
- Journalisation centralisée (logging).
- Validation des données utilisateur.
- Gestion structurée des erreurs applicatives.

## Stabilisation

- Fiabilisation du moteur d'estimation.
- Amélioration de la gestion des projets, profils, scénarios et rapports.
- Harmonisation du comportement de l'interface utilisateur.
- Optimisation du chargement et de la sauvegarde des données.
- Corrections issues des tests fonctionnels avant publication.

---

## Roadmap V2

### Prévu

- Tableau de bord (Dashboard).
- Statistiques avancées.
- Graphiques d'analyse.
- Gestion avancée des profils.
- Paramètres configurables depuis l'interface.
- Export Word.
- Support SQLite.
- Thèmes personnalisables.
- Internationalisation.

---
