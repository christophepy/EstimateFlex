# 🚀 EstimateFlex V2 \- Roadmap

## Vision

Après la validation de la V1, l'objectif de la V2 est de transformer EstimateFlex en un véritable outil professionnel d'aide au chiffrage et au pilotage des études d'ingénierie.

L'accent sera mis sur :

- la personnalisation ;
- l'analyse des données ;
- la productivité utilisateur ;
- la préparation des futures évolutions (SQLite, Web).

---

# ✅ Héritage V1

## Profils

- Création de profils personnalisés
- Modification de profils
- Suppression de profils
- Gestion des profils standards (Junior, Senior, Expert)
- Validation métier de base

## Projets

- Création de projets
- Modification de projets
- Suppression de projets
- Persistance JSON
- Contrôle d'unicité des projets

## Scénarios

- Création de scénarios
- Modification de scénarios
- Suppression de scénarios
- Gestion des hypothèses de calcul

## Estimations

- Calcul automatique des charges
- Calcul automatique des coûts
- Gestion du risque
- Génération des résultats

## Rapports

- Historique complet des estimations
- Consultation du détail d'une estimation
- Ouverture d'une estimation existante
- Renommage d'une estimation
- Suppression d'une estimation
- Export PDF
- Export Excel
- Ouverture directe du dossier des exports
- Rafraîchissement de la liste
- Tri des colonnes

## Dashboard

- Vue synthétique des estimations
- Indicateurs globaux
- Classements principaux
- Analyse des coûts
- Analyse des charges

## Qualité logicielle

- Architecture modulaire
- Typage Python
- Ruff ✅
- MyPy ✅
- Pylint ≈ 9.8/10 ✅

---

# V2.1 \- Paramètres de l'application

## Objectif

Centraliser les préférences utilisateur.

## Nouveau menu

Outils → Paramètres

## Paramètres généraux

- Devise par défaut
- Répertoire d'exports

## Paramètres d'affichage

- Afficher les KPI Dashboard
- Afficher les graphiques Dashboard

## Bénéfices

- Personnalisation de l'application
- Centralisation de la configuration
- Préparation du Dashboard avancé V2.2

---

# V2.2 \- Dashboard avancé

## Objectif

Faire du Dashboard un véritable outil de pilotage.

## KPI

- Total projets
- Total scénarios
- Total estimations
- Total heures
- Total jours
- Total coûts

## Statistiques

- Top clients
- Top projets
- Top profils
- Répartition des risques

## Visualisations

- Graphiques de coûts
- Graphiques de charges
- Évolution des estimations

---

# V2.3 \- Rapports avancés

## Recherche

- Recherche globale
- Filtre par projet
- Filtre par client
- Filtre par scénario
- Filtre par profil
- Filtre par date

## Analyse

- Comparaison d'estimations
- Comparaison de versions
- Historique amélioré

## Exports

- Mise en page PDF enrichie
- Graphiques dans Excel
- Export CSV

---

# V2.4 \- Gestion avancée des profils

## Fonctionnalités

- Bouton "Dupliquer" dans l'interface
- Profil par défaut
- Import profil JSON
- Export profil JSON

## Validation renforcée

- Contrôle des bornes de productivité
- Contrôle des taux journaliers
- Contrôle des incohérences de configuration

---

# V2.5 \- Gestion avancée des projets

## Fonctionnalités

- Duplication de projet
- Archivage de projet
- Désarchivage
- Recherche multicritère

## Historique

- Date de création
- Date de modification
- Nombre d'estimations associées

---

# V2.6 \- Migration SQLite

## Objectif

Remplacer progressivement le stockage JSON.

## Fonctionnalités

- Base SQLite locale
- Migration automatique JSON → SQLite
- Repositories compatibles SQLite

## Avantages

- Performances
- Recherches avancées
- Évolutivité
- Préparation de la version Web

---

# V2.7 \- Refactoring et qualité

## UI

- Mutualisation des styles Qt
- Mutualisation des composants réutilisables

## Architecture

- Découpage des écrans complexes
- Réduction des duplications
- Amélioration des services

## Tests

- Tests unitaires
- Tests des calculs
- Tests des exports

---

# V3 \- Vision long terme

## Plateforme

- PostgreSQL
- Multi\-utilisateurs
- Gestion des rôles
- Authentification

## Connectivité

- API REST
- Version Web
- Synchronisation Cloud

## Reporting

- Indicateurs entreprise
- Portefeuille projets
- Charge globale BE

---

# Priorité recommandée

1. Paramètres de l'application
2. Dashboard avancé
3. Rapports avancés
4. Gestion avancée des profils
5. Gestion avancée des projets
6. SQLite
7. Version Web

---

## État actuel

✅ V1 stable

✅ Ruff : OK

✅ MyPy : OK

✅ Pylint : ~9.8/10

✅ Prêt pour le démarrage du développement V2
