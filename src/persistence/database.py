# src/persistence/database.py

import sqlite3
import sys
from pathlib import Path

DATABASE_NAME = "estimateflex.db"


def get_database_path() -> Path:

    if getattr(sys, "frozen", False):
        root = Path(sys.executable).parent
    else:
        root = Path(__file__).resolve().parents[2]

    db_dir = root / "data"
    db_dir.mkdir(parents=True, exist_ok=True)

    return db_dir / DATABASE_NAME


def get_connection():

    conn = sqlite3.connect(get_database_path())

    conn.row_factory = sqlite3.Row

    return conn


def test_connection() -> bool:
    try:
        with get_connection() as conn:
            conn.execute("SELECT 1")
        return True

    except sqlite3.Error:
        return False


class Database:

    def initialize(self) -> None:

        conn = get_connection()

        cursor = conn.cursor()

        # =====================================================
        # PROFILES
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS profiles(
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nom TEXT NOT NULL UNIQUE,
                description TEXT,

                taux_journalier REAL DEFAULT 650.0,
                heures_par_jour REAL DEFAULT 7.0,
                facteur_productivite REAL DEFAULT 1.0,

                heure_par_ligne REAL DEFAULT 0.40,
                heure_par_support REAL DEFAULT 0.20,
                heure_par_vanne REAL DEFAULT 0.10,
                heure_par_boite_a_ressort REAL DEFAULT 0.20,
                heure_compensateur REAL DEFAULT 1.00,
                heure_par_bride REAL DEFAULT 0.10,
                heure_par_equipement REAL DEFAULT 0.10
            )
            """)

        # =====================================================
        # PROFILS PAR DEFAUT
        # =====================================================

        cursor.execute("""
            INSERT OR IGNORE INTO profiles(
                nom,
                description,
                taux_journalier,
                heures_par_jour,
                facteur_productivite
            )
            VALUES(
                'Junior',
                'Ingénieur débutant',
                500,
                7,
                0.80
            )
            """)

        cursor.execute("""
            INSERT OR IGNORE INTO profiles(
                nom,
                description,
                taux_journalier,
                heures_par_jour,
                facteur_productivite
            )
            VALUES(
                'Senior',
                'Ingénieur expérimenté',
                800,
                7,
                1.00
            )
            """)

        cursor.execute("""
            INSERT OR IGNORE INTO profiles(
                nom,
                description,
                taux_journalier,
                heures_par_jour,
                facteur_productivite
            )
            VALUES(
                'Expert',
                'Référent technique',
                1200,
                7,
                1.20
            )
            """)

        # =====================================================
        # SCENARIOS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS scenarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nom TEXT NOT NULL UNIQUE,
                description TEXT,

                facteur_productivite REAL DEFAULT 1.0,
                facteur_risque REAL DEFAULT 1.0,
                facteur_disponibilite REAL DEFAULT 1.0,

                actif INTEGER DEFAULT 1
            )
            """)

        # =====================================================
        # SCENARIOS PAR DEFAUT
        # =====================================================

        cursor.execute("""
            INSERT OR IGNORE INTO scenarios(
                nom,
                description,
                facteur_productivite,
                facteur_risque,
                facteur_disponibilite,
                actif
            )
            VALUES(
                'Optimiste',
                'Scenario favorable',
                1.10,
                0.90,
                1.00,
                1
            )
            """)

        cursor.execute("""
            INSERT OR IGNORE INTO scenarios(
                nom,
                description,
                facteur_productivite,
                facteur_risque,
                facteur_disponibilite,
                actif
            )
            VALUES(
                'Réaliste',
                'Scenario de référence',
                1.00,
                1.00,
                1.00,
                1
            )
            """)

        cursor.execute("""
            INSERT OR IGNORE INTO scenarios(
                nom,
                description,
                facteur_productivite,
                facteur_risque,
                facteur_disponibilite,
                actif
            )
            VALUES(
                'Pessimiste',
                'Scenario prudent',
                0.90,
                1.20,
                0.80,
                1
            )
            """)

        # =====================================================
        # ESTIMATIONS
        # =====================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS estimations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,

                estimation_nom TEXT,

                project_nom TEXT,
                profile_nom TEXT,
                scenario_nom TEXT,

                estimated_hours REAL,
                estimated_days REAL,
                estimated_cost REAL,

                risk_factor REAL,

                created_at TEXT
            )
            """)

        # =====================================================
        # MIGRATIONS
        # =====================================================

        cursor.execute("PRAGMA table_info(estimations)")

        columns = [row["name"] for row in cursor.fetchall()]

        if "estimation_nom" not in columns:

            cursor.execute("""
                ALTER TABLE estimations
                ADD COLUMN estimation_nom TEXT
                """)

            cursor.execute("""
                UPDATE estimations
                SET estimation_nom =
                    project_nom || '_' || scenario_nom
                WHERE estimation_nom IS NULL
                   OR estimation_nom = ''
                """)

        conn.commit()
        conn.close()


# Initialisation automatique de la base
_database = Database()
_database.initialize()
