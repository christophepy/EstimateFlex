# src/persistence/profile_repository.py

"""
Repository de gestion des profils utilisateurs.
"""

from src.models.user_profile import UserProfile
from src.persistence.database import get_connection


class ProfileRepository:
    """
    CRUD des profils utilisateurs.
    """

    @staticmethod
    def create(profile: UserProfile) -> int:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            INSERT INTO profiles(
                nom,
                description,
                taux_journalier,
                heures_par_jour,
                facteur_productivite,
                heure_par_ligne,
                heure_par_support,
                heure_par_vanne,
                heure_par_boite_a_ressort,
                heure_compensateur,
                heure_par_bride,
                heure_par_equipement
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                profile.nom,
                profile.description,
                profile.taux_journalier,
                profile.heures_par_jour,
                profile.facteur_productivite,
                profile.heure_par_ligne,
                profile.heure_par_support,
                profile.heure_par_vanne,
                profile.heure_par_boite_a_ressort,
                profile.heure_compensateur,
                profile.heure_par_bride,
                profile.heure_par_equipement,
            ),
        )

        conn.commit()

        profile_id = cursor.lastrowid

        conn.close()

        return profile_id

    @staticmethod
    def get_by_id(profile_id: int) -> UserProfile | None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM profiles
            WHERE id = ?
            """,
            (profile_id,),
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return UserProfile(
            id=row["id"],
            nom=row["nom"],
            description=row["description"],
            taux_journalier=row["taux_journalier"],
            heures_par_jour=row["heures_par_jour"],
            facteur_productivite=row["facteur_productivite"],
            heure_par_ligne=row["heure_par_ligne"],
            heure_par_support=row["heure_par_support"],
            heure_par_vanne=row["heure_par_vanne"],
            heure_par_boite_a_ressort=row["heure_par_boite_a_ressort"],
            heure_compensateur=row["heure_compensateur"],
            heure_par_bride=row["heure_par_bride"],
            heure_par_equipement=row["heure_par_equipement"],
        )

    @staticmethod
    def get_all() -> list[UserProfile]:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM profiles
            ORDER BY nom
            """)

        rows = cursor.fetchall()

        conn.close()

        profiles = []

        for row in rows:

            profiles.append(
                UserProfile(
                    id=row["id"],
                    nom=row["nom"],
                    description=row["description"],
                    taux_journalier=row["taux_journalier"],
                    heures_par_jour=row["heures_par_jour"],
                    facteur_productivite=row["facteur_productivite"],
                    heure_par_ligne=row["heure_par_ligne"],
                    heure_par_support=row["heure_par_support"],
                    heure_par_vanne=row["heure_par_vanne"],
                    heure_par_boite_a_ressort=row["heure_par_boite_a_ressort"],
                    heure_compensateur=row["heure_compensateur"],
                    heure_par_bride=row["heure_par_bride"],
                    heure_par_equipement=row["heure_par_equipement"],
                )
            )

        return profiles

    @staticmethod
    def update(profile: UserProfile) -> bool:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE profiles
            SET
                nom = ?,
                description = ?,
                taux_journalier = ?,
                heures_par_jour = ?,
                facteur_productivite = ?,
                heure_par_ligne = ?,
                heure_par_support = ?,
                heure_par_vanne = ?,
                heure_par_boite_a_ressort = ?,
                heure_compensateur = ?,
                heure_par_bride = ?,
                heure_par_equipement = ?
            WHERE id = ?
            """,
            (
                profile.nom,
                profile.description,
                profile.taux_journalier,
                profile.heures_par_jour,
                profile.facteur_productivite,
                profile.heure_par_ligne,
                profile.heure_par_support,
                profile.heure_par_vanne,
                profile.heure_par_boite_a_ressort,
                profile.heure_compensateur,
                profile.heure_par_bride,
                profile.heure_par_equipement,
                profile.id,
            ),
        )

        conn.commit()

        updated = cursor.rowcount > 0

        conn.close()

        return updated

    @staticmethod
    def delete(profile_id: int) -> bool:

        profile = ProfileRepository.get_by_id(profile_id)

        if profile is None:
            return False

        if profile.nom in {
            "Junior",
            "Senior",
            "Expert",
        }:
            raise ValueError("Les profils système ne peuvent pas être supprimés.")

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            DELETE FROM profiles
            WHERE id = ?
            """,
            (profile_id,),
        )

        conn.commit()

        deleted = cursor.rowcount > 0

        conn.close()

        return deleted

    @staticmethod
    def count() -> int:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) AS total
            FROM profiles
            """)

        total = cursor.fetchone()["total"]

        conn.close()

        return total

    @staticmethod
    def get_by_name(nom: str) -> UserProfile | None:

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM profiles
            WHERE nom = ?
            """,
            (nom,),
        )

        row = cursor.fetchone()

        conn.close()

        if row is None:
            return None

        return UserProfile(
            id=row["id"],
            nom=row["nom"],
            description=row["description"],
            taux_journalier=row["taux_journalier"],
            heures_par_jour=row["heures_par_jour"],
            facteur_productivite=row["facteur_productivite"],
            heure_par_ligne=row["heure_par_ligne"],
            heure_par_support=row["heure_par_support"],
            heure_par_vanne=row["heure_par_vanne"],
            heure_par_boite_a_ressort=row["heure_par_boite_a_ressort"],
            heure_compensateur=row["heure_compensateur"],
            heure_par_bride=row["heure_par_bride"],
            heure_par_equipement=row["heure_par_equipement"],
        )
