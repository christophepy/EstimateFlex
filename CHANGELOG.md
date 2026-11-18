# Changelog

Toutes les modifications notables du projet EstimateFlex sont documentées dans ce fichier.

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

### Exports

- Export PDF des estimations.
- Export Excel des estimations.
- Génération automatique des rapports de synthèse.

## Technique

- Architecture modulaire Python.
- Interface graphique PyQt6 multi-onglets.
- Modèles de données basés sur les dataclasses.
- Couche Repository pour l'accès aux données.
- Persistance des données.
- Journalisation centralisée.
- Validation des données utilisateur.
- Gestion structurée des erreurs applicatives.

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

- Affichage configurable des KPI.
- Affichage configurable des graphiques.
- Masquage dynamique des blocs Dashboard.
- Actualisation automatique après modification des paramètres.

## Amélioré

### Multi-devises

- Conversion automatique des montants selon la devise sélectionnée.
- Mise à jour dynamique des montants affichés dans le Dashboard.
- Mise à jour dynamique des montants affichés dans les Reports.
- Centralisation de la gestion des devises via CurrencyService.

### Interface

- Rechargement immédiat des paramètres sans redémarrage.
- Synchronisation automatique des onglets après modification des paramètres.
- Compatibilité avec les anciens fichiers de configuration.

## Corrigé

- Correction de plusieurs problèmes d'actualisation du Dashboard.
- Correction de l'affichage des devises dans les Reports.
- Correction du rafraîchissement des valeurs après modification des paramètres.
- Correction de compatibilité ascendante du fichier settings.json.

## Tests

- Ajout des tests unitaires des paramètres Dashboard.
- Vérification des valeurs par défaut.
- Vérification de la sérialisation.
- Vérification du chargement des paramètres.

### Résultats

- 136 tests exécutés.
- 136 tests réussis.
- 0 échec.
- 0 erreur.

---

# [2.1b] - 2026-11-17

Version de stabilisation et d'amélioration ergonomique.

## Corrigé

### Exports PDF et Excel

- Correction de l'affichage de la devise en double dans les exports.
- Harmonisation du contenu PDF et Excel.
- Uniformisation des libellés :
  - Charge (heures)
  - Durée (jours)
  - Coût (devise)
  - Facteur de risque
  - Date de génération
- Suppression des unités redondantes dans les valeurs exportées.

### Base de données

- Validation des migrations SQLite.
- Validation de la colonne `currency`.
- Validation de la colonne `estimation_nom`.
- Validation de la compatibilité avec les bases existantes.

## Amélioré

### Interface utilisateur
