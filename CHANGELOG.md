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

# [2.1a] - 2026-11-16

Évolution du système de paramètres utilisateur et du Dashboard.

## Ajouté

### Paramètres

- Gestion de la devise de travail (EUR, USD, CHF, GBP).
- Gestion du répertoire d'exports configurable.
- Ajout des paramètres d'affichage du Dashboard.
- Persistance des préférences utilisateur.

### Dashboard

- Ajout de l'option « Afficher les KPI Dashboard ».
- Ajout de l'option « Afficher les graphiques Dashboard ».
- Masquage dynamique du bloc « Indicateurs clés ».
- Masquage dynamique du graphique « Estimations par scénario ».
- Masquage dynamique du graphique « Répartition des coûts ».
- Actualisation automatique du Dashboard après modification des paramètres.

## Amélioré

### Multi-devises

- Conversion automatique des montants selon la devise sélectionnée.
- Mise à jour dynamique des montants affichés dans le Dashboard.
- Mise à jour dynamique des montants affichés dans les Reports.
- Centralisation de la gestion des devises via CurrencyService.

### Interface

- Rechargement immédiat des paramètres sans redémarrage de l'application.
- Synchronisation automatique des onglets après modification des paramètres.
- Amélioration de la gestion des paramètres absents pour assurer la compatibilité avec les anciennes versions.

## Corrigé

- Correction de plusieurs problèmes d'actualisation du Dashboard.
- Correction de l'affichage des devises dans les rapports.
- Correction du rafraîchissement des valeurs après changement de paramètres.
- Correction de la compatibilité avec les anciens fichiers settings.json.

## Tests

- Ajout des tests unitaires des paramètres Dashboard.
- Vérification des valeurs par défaut des options d'affichage.
- Vérification de la sérialisation des paramètres Dashboard.
- Vérification du chargement des paramètres Dashboard.
- Vérification de la compatibilité avec les anciens fichiers settings.json.

### Résultats

- 136 tests exécutés.
- 136 tests réussis.
- 0 échec.
- 0 erreur.

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
