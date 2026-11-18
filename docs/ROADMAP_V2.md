# 🚀 EstimateFlex V2 \- Roadmap Révisée

## Vision

EstimateFlex doit évoluer d'un outil de chiffrage vers une plateforme complète d'estimation, d'analyse et de pilotage des études d'ingénierie.

Les objectifs principaux sont :

- Fiabilité des estimations
- Productivité des chargés d'affaires
- Analyse décisionnelle
- Qualité logicielle
- Préparation de la future version Web

---

# ✅ Versions réalisées

## V1

### Fonctionnalités

- Gestion des profils
- Gestion des projets
- Gestion des scénarios
- Calcul des estimations
- Gestion du risque
- Historique des estimations
- Exports PDF
- Exports Excel

### Qualité

- Architecture modulaire
- Typage Python
- Ruff
- MyPy
- Pylint

---

## ✅ V2.1a \- Paramètres applicatifs

### Nouveautés

Menu :

Outils → Paramètres

### Paramètres généraux

- Devise par défaut
- Répertoire d'export

### Paramètres Dashboard

- Afficher les KPI
- Afficher les graphiques

### Améliorations

- Service des paramètres
- Persistance centralisée
- Gestion multi\-devises
- Exports pilotés par configuration

### Statut

✅ Publiée et taguée GitHub (v2.1a)

---

# ✅ V2.1b \- Stabilisation et ergonomie

## Objectif

Finaliser l'expérience utilisateur et fiabiliser la version avant le développement du Dashboard avancé.

### Interface utilisateur

- Simplification de la fenêtre Paramètres.
- Suppression des options non utilisées :
    - Thème
    - Taille de police
- Conservation des options Dashboard :
    - Afficher les KPI
    - Afficher les graphiques

### Navigation

- Réorganisation des onglets métier :
    1. Projets
    2. Profils
    3. Scénarios
    4. Estimation
    5. Reports
    6. Dashboard

### Menus

- Simplification de la barre de menus.
- Conservation des menus :
    - Outils
    - Aide

### Exports

- Harmonisation des exports PDF et Excel.
- Suppression de l'affichage des devises en double.
- Uniformisation des intitulés.
- Uniformisation du format des nombres et des dates.

### Multi\-devises

- Validation du fonctionnement :
    - EUR
    - USD
    - CHF
    - GBP

### Base de données

- Validation des migrations SQLite.
- Validation du schéma d'estimations.
- Validation des redémarrages multiples.

### Maintenance

- Nettoyage du dépôt Git.
- Suppression des artefacts techniques générés.
- Mise à jour du .gitignore.
- Mise à jour du CHANGELOG.

### Statut

✅ Version stabilisée

✅ Prête pour le développement V2.2



---

# V2.2 \- Dashboard avancé

## Objectif

Transformer le Dashboard en outil de pilotage.

### KPI

- Nombre de projets
- Nombre de scénarios
- Nombre d'estimations
- Total heures
- Total jours
- Total coûts
- Coût moyen
- Charge moyenne

### Statistiques

- Top clients
- Top projets
- Top profils
- Répartition des risques
- Répartition des devises

### Visualisations

- Évolution des coûts
- Évolution des charges
- Répartition des profils
- Répartition des risques
- Tendances temporelles

### Paramétrage

Pilotage via les options ajoutées en V2.1a.

---

# V2.3 \- Rapports avancés

## Recherche

- Recherche globale
- Filtre client
- Filtre projet
- Filtre scénario
- Filtre profil
- Filtre période

## Analyse

- Comparaison d'estimations
- Comparaison de scénarios
- Historique enrichi

## Gestion financière

- Gestion des devises par projet
- Historisation des taux de change
- Conservation du taux utilisé lors de la création d'une estimation
- Recalcul optionnel avec le taux courant
- Analyse des écarts de change

## Exports

- PDF enrichis
- Graphiques Excel
- Export CSV
- Export JSON

---

# V2.4 \- Profils avancés

## Fonctionnalités

- Duplication d'un profil
- Import JSON
- Export JSON
- Profil favori
- Profil par défaut

## Validation

- Contrôle TJM
- Contrôle productivité
- Vérification des incohérences

---

# V2.5 \- Projets avancés

## Fonctionnalités

- Duplication projet
- Archivage
- Désarchivage
- Recherche multicritère

## Historique

- Date de création
- Date de modification
- Nombre d'estimations associées

---

# V2.6 \- Base de données

## Objectif

Consolider le socle de données.

### Fonctionnalités

- Migration complète SQLite
- Migrations automatiques
- Optimisation requêtes
- Sauvegarde base

### Bénéfices

- Meilleures performances
- Recherches rapides
- Fondation des futures fonctionnalités

---

# V2.7 \- Refactoring et qualité

## Architecture

- Réduction des dépendances
- Mutualisation des composants UI
- Découpage des écrans volumineux

## Couverture de tests

- Calculs
- Repositories
- Services
- Exports
- Interface utilisateur

## Objectif

Couverture cible ≥ 80 %

---

# V3 \- EstimateFlex Platform

## Web

- API REST
- Frontend Web
- Déploiement Cloud

## Collaboration

- Multi\-utilisateurs
- Gestion des rôles
- Gestion des permissions

## Base de données

- PostgreSQL

## Reporting

- Tableaux de bord entreprise
- Portefeuille projets
- Plan de charge BE
- Indicateurs de performance

---

# Priorité recommandée

1. V2.1b \- Stabilisation
2. V2.2 \- Dashboard avancé
3. V2.3 \- Rapports avancés
4. V2.4 \- Profils avancés
5. V2.5 \- Projets avancés
6. V2.6 \- Consolidation SQLite
7. V2.7 \- Qualité et refactoring
8. V3 \- Plateforme Web

---

# État actuel

✅ V1 stable

✅ V2.1a publiée

✅ GitHub synchronisé

✅ Gestion des paramètres opérationnelle

✅ Gestion multi\-devises opérationnelle

✅ Dashboard configurable

✅ Dépôt nettoyé

🚀 Prêt pour la phase V2.1b puis V2.2
